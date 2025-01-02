
import numpy as np
from borders import *

class Field:
    def __init__(self, field: np.array):
        self.field = field
        self.region_map = np.full(field.shape, fill_value=None)
        self.rows = field.shape[0]
        self.columns = field.shape[1]
        self.regions = []

    def scan_for_regions(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.find_region((row, col))

    def find_region(self, loc: tuple):
        if self.region_map[loc] is not None:
            return None
        region = Region(self, loc)
        region.expand()
        region.compute_perimeter()
        self.regions.append(region)

    def __getitem__(self, loc: tuple):
        return self.field[loc]

    def __str__(self):
        return str(self.field)

    def print_regions(self):
        fence_cost = 0
        for region in self.regions:
            print(region)
            fence_cost += region.area * region.perimeter
        print(f"Total fence cost: {fence_cost}")

    def orthogonal_cells(self, loc: tuple) -> list[tuple]:
        cells = []
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_loc = (loc[0] + direction[0], loc[1] + direction[1])
            if new_loc[0] in range(self.rows) and new_loc[1] in range(self.columns):
                cells.append(new_loc)
        return cells

    def print_fences(self):
        # full map is defined as an interleaved map of the field and the fences.
        field = self.field
        full_height = self.rows * 2 + 1
        full_width = self.columns * 2 + 1
        full_map = np.full(shape=(full_height, full_width), fill_value=" ")
        for row in range(full_height):
            for col in range(full_width):

                # add outside perimeter fence
                if row == 0:
                    if col == 0:
                        full_map[row][col] = LightBorders.TOP_LEFT
                    elif col == full_width - 1:
                        full_map[row][col] = LightBorders.TOP_RIGHT
                    else:
                        full_map[row][col] = LightBorders.HORIZ
                elif row == full_height - 1:
                    if col == 0:
                        full_map[row][col] = LightBorders.BOTTOM_LEFT
                    elif col == full_width - 1:
                        full_map[row][col] = LightBorders.BOTTOM_RIGHT
                    else:
                        full_map[row][col] = LightBorders.HORIZ
                else:
                    if col == 0 or col == full_width - 1:
                        full_map[row][col] = LightBorders.VERT

                # Field crop cells live in the odd indices of full_map. copy those over as we also scan
                # for crop transitions and draw in the horizontal and vertical fences between crops
                if row % 2 and col % 2:
                    # work out the field map location and the next cells to the east and south
                    loc = (row // 2, col // 2)
                    east = (row // 2, col // 2 + 1)
                    south = (row // 2 + 1, col // 2)
                    full_map[row][col] = field[loc]
                    # when the crop changes as we scan across the field add a fence symbol in between plots
                    if east[1] in range(self.columns):
                        if field[east] != field[loc]:
                            full_map[row][col + 1] = LightBorders.VERT
                    if south[0] in range(self.rows):
                        if field[south] != field[loc]:
                            full_map[row + 1][col] = LightBorders.HORIZ

        # join the gaps at corners and junctions by figuring out if a fence exists at the cardinal points
        # special case for the edges of the map
        for row in range(full_height):
            for col in range(full_width):
                # fences live in the even indices of full_map
                if row % 2 == 0 and col % 2 == 0:
                    north = False if row == 0 else full_map[row - 1][col] != " "
                    south = False if row == full_height - 1 else full_map[row + 1][col] != " "
                    west = False if col == 0 else full_map[row][col - 1] != " "
                    east = False if col == full_width - 1 else full_map[row][col + 1] != " "
                    full_map[row][col] = map_joiner(north, east, south, west, LightBorders)

        for row in range(full_map.shape[0]):
            print("".join(full_map[row, :]))

class Region:
    def __init__(self, field: Field, loc: tuple):
        self.field = field
        self.start_loc = loc
        self.locations = [loc]
        self.crop_type = self.field[loc]
        self.perimeter = 0
        self.area = 1
        self.sides = []

    def expand(self, loc: tuple | None = None):
        if loc is None:
            loc = self.start_loc
        for new_loc in self.field.orthogonal_cells(loc):
            if new_loc in self.locations:
                continue
            if self.field.region_map[new_loc] is None and self.crop_type == self.field[new_loc]:
                self.locations.append(new_loc)
                self.area += 1
                self.field.region_map[new_loc] = self
                self.expand(new_loc)

    def compute_perimeter(self):
        self.perimeter = 0
        for loc in self.locations:
            # add perimeter for edge locations
            if loc[0] == 0 or loc[0] == self.field.rows - 1:
                self.perimeter += 1
            if loc[1] == 0 or loc[1] == self.field.columns - 1:
                self.perimeter += 1
            for adjacent in self.field.orthogonal_cells(loc):
                if self.field[adjacent] != self.crop_type:
                    self.perimeter += 1

    def find_sides(self):
        self.sides = []
        vert_edges = np.full(shape=(self.field.rows, self.field.columns+1), fill_value=None)
        horiz_edges = np.full(shape=(self.field.rows+1, self.field.columns), fill_value=None)
        for loc in self.locations:
            north = (loc[0]-1, loc[1])
            south = (loc[0]+1, loc[1])
            west = (loc[0], loc[1]-1)
            east = (loc[0], loc[1]+1)



    def __str__(self):
        return f"{self.crop_type}: {self.area} * {self.perimeter} = {self.area * self.perimeter} ".ljust(22) + \
               f"{self.area} * {len(self.sides)} = {self.area*len(self.sides)}"

class Side:
    """
    Contiguous series of edges between cells of differing regions on a map
    The in-side is defined as the side matching the region crop
    The out-side is the opposite. It is either outside the map or in a different region.
    In deriving contiguous sides, we must watch that the in-side remains consistent
    """
    def __init__(self, region: Region, loc: tuple, adjacent: tuple):
        self.field = region.field
        self.region = region
        self.edges = []


def main(filename: str):
    with open(filename) as f:
        crop_types = {}
        rows = []
        for line in f:
            row = list(line.strip())
            if len(row) > 0:
                rows.append(row)
                for crop in row:
                    if crop not in crop_types:
                        crop_types[crop] = 1
                    else:
                        crop_types[crop] += 1
        field = Field(np.array(rows))
    # print(field)
    field.scan_for_regions()
    # field.print_regions()
    field.print_fences()


if __name__ == "__main__":
    # main("sample.txt")
    main("input.txt")