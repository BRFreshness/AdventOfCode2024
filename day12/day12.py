
import numpy as np


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


class Region:
    def __init__(self, field: Field, loc: tuple):
        self.field = field
        self.start_loc = loc
        self.locations = [loc]
        self.crop_type = self.field[loc]
        self.perimeter = 0
        self.area = 1

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

    def __str__(self):
        return f"{self.crop_type}: {self.area} * {self.perimeter} = {self.area * self.perimeter}"

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
    print(field)
    field.scan_for_regions()
    field.print_regions()

if __name__ == "__main__":
    main("input.txt")