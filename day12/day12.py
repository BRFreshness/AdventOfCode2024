
import operator
import numpy as np
from borders import *
from util import adjacent_to


class Field:
    def __init__(self, field: np.array):
        self.field = field
        self.region_map = np.full(field.shape, fill_value=None)
        self.rows = field.shape[0]
        self.columns = field.shape[1]
        self.regions = []
        self.full_map = None

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
        m = self.field if self.full_map is None else self.full_map
        data = []
        for row in range(m.shape[0]):
            data.append("".join(m[row, :]))
        return "\n".join(data) + "\n"

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

    def draw_fences(self, btype: type[LightBorders] | type[HeavyBorders] | type[DoubleBorders] = LightBorders):
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
                        full_map[row][col] = btype.TOP_LEFT
                    elif col == full_width - 1:
                        full_map[row][col] = btype.TOP_RIGHT
                    else:
                        full_map[row][col] = btype.HORIZ
                elif row == full_height - 1:
                    if col == 0:
                        full_map[row][col] = btype.BOTTOM_LEFT
                    elif col == full_width - 1:
                        full_map[row][col] = btype.BOTTOM_RIGHT
                    else:
                        full_map[row][col] = btype.HORIZ
                else:
                    if col == 0 or col == full_width - 1:
                        full_map[row][col] = btype.VERT

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
                            full_map[row][col + 1] = btype.VERT
                    if south[0] in range(self.rows):
                        if field[south] != field[loc]:
                            full_map[row + 1][col] = btype.HORIZ

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
                    full_map[row][col] = map_joiner(north, east, south, west, btype)
        self.full_map = full_map

    def find_sides(self):
        if self.full_map is None:
            self.draw_fences()
        for region in self.regions:
            region.find_sides()

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
        for loc in self.locations:
            # convert to full_map location coordinates
            full_loc = (loc[0] * 2 + 1, loc[1] * 2 + 1)
            for adjacent in adjacent_to(full_loc):
                if self.field.full_map[adjacent] != " ":
                    side = Side(self, full_loc, adjacent)
                    if len(side.edges) > 0:
                        flag = True
                        for check_side in self.sides:
                            if side.edges[0] == check_side.edges[0]:
                                flag = False
                        if flag:
                            self.sides.append(side)

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
        self.full_map = region.field.full_map
        self.region = region
        self.edges = []
        self.extend_side(loc, adjacent)

    def extend_side(self, loc: tuple, adjacent: tuple):
        def check_limits(loc: tuple) -> bool:
            return loc[0] not in range(self.full_map.shape[0]) or loc[1] not in range(self.full_map.shape[1])

        for delta in [((loc[1] - adjacent[1]) *  2, (loc[0] - adjacent[0]) *  2),
                      ((loc[1] - adjacent[1]) * -2, (loc[0] - adjacent[0]) * -2)]:
            check_loc = loc
            check_adj = adjacent
            while self.full_map[check_loc] == self.region.crop_type and \
                  self.full_map[check_adj] != " " and self.add_edge(check_loc, check_adj):
                check_loc = (check_loc[0] + delta[0], check_loc[1] + delta[1])
                check_adj = (check_adj[0] + delta[0], check_adj[1] + delta[1])
                if check_limits(check_loc) or check_limits(check_adj):
                    break

    def add_edge(self, loc: tuple, adjacent: tuple) -> bool:
        if self.full_map[loc] != self.full_map[adjacent]:
            edge = adjacent #(loc[0] + adjacent[0] + 1, loc[1] + adjacent[1] + 1)
            if edge not in self.edges:
                self.edges.append(edge)
            self.edges.sort(key=operator.itemgetter(0,1))
            return True
        return False


    def __str__(self):
        return f"{self.edges}"


def main(filename: str):
    with open(filename) as f:
        rows = []
        for line in f:
            row = list(line.strip())
            if len(row) > 0:
                rows.append(row)
        field = Field(np.array(rows))
    field.scan_for_regions()
    field.draw_fences()
    field.find_sides()
    field.print_regions()
    print(field)
    price = 0
    for region in field.regions:
        price += len(region.sides) * region.area

    print(f"Total price: {price}")


if __name__ == "__main__":
    # main("sample.txt")
    main("input.txt")