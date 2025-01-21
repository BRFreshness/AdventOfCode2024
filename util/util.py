from enum import Enum

class Headings(Enum):
    def __init__(self, y: int, x: int):
        self._value_ = (y, x)
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    @property
    def x(self):
        return self._value_[1]

    @property
    def y(self):
        return self._value_[0]

    def __lt__(self, other):
        return self._value_[0] < other._value_[0]

    def add(self, loc: tuple) -> tuple:
        return self._value_[0] + loc[0], self._value_[1] + loc[1]

    def rotate(self, cw: bool = True) -> Enum:
        if self == Headings.NORTH:
            return Headings.EAST if cw else Headings.WEST
        elif self == Headings.EAST:
            return Headings.SOUTH if cw else Headings.NORTH
        elif self == Headings.SOUTH:
            return Headings.WEST if cw else Headings.EAST
        elif self == Headings.WEST:
            return Headings.NORTH if cw else Headings.SOUTH

    def cw(self) -> Enum:
        return self.rotate(cw=True)

    def ccw(self) -> Enum:
        return self.rotate(cw=False)

    def rot180(self) -> Enum:
        r1 = self.rotate(cw=False)
        return r1.rotate(cw=False)

    def rotations(self, loc: tuple, new_loc: tuple, degrees = False) -> tuple[int, "Headings"]:
        heading = self.__copy__()
        rot = 0
        while heading.add(loc) != new_loc:
            if rot > 3:
                raise RuntimeError(f"{loc} and {new_loc} are not adjacent")
            heading = heading.rotate()
            rot += 1
        if rot == 3:
            rot = -1
        if degrees:
            return rot * 90, heading
        else:
            return abs(rot), heading

def adjacent_to(loc: tuple) -> list[tuple]:
    return [h.add(loc) for h in Headings]

if __name__ == "__main__":
    loc = (4, 4)
    adj = adjacent_to(loc)
    print(adj)
    print()
    adj.append((7,7))

    for h in Headings:
        print(f"\nfrom {loc} heading {h.name}")
        for new_loc in adj:
            try:
                r, new_h = h.rotations(loc, new_loc, True)
                result = f"rotate {r} degrees"
            except:
                result = "not adjacent"
                new_h = h
            print(f"  --> {new_loc} : {new_h.name} {result}")

