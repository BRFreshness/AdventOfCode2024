from enum import StrEnum

class LightBorders(StrEnum):
    HORIZ = "\u2500"
    VERT = "\u2502"
    TOP_LEFT = "\u250c"
    TOP_RIGHT = "\u2510"
    BOTTOM_LEFT = "\u2514"
    BOTTOM_RIGHT = "\u2518"
    HORIZ_UP = "\u2534"
    HORIZ_DOWN = "\u252c"
    VERT_RIGHT = "\u2524"
    VERT_LEFT = "\u251c"
    CROSS = "\u253c"

class HeavyBorders(StrEnum):
    HORIZ = "\u2501"
    VERT = "\u2503"
    TOP_LEFT = "\u250f"
    TOP_RIGHT = "\u2513"
    BOTTOM_LEFT = "\u2517"
    BOTTOM_RIGHT = "\u251b"
    HORIZ_UP = "\u253b"
    HORIZ_DOWN = "\u2533"
    VERT_RIGHT = "\u252b"
    VERT_LEFT = "\u2523"
    CROSS = "\u254b"

class DoubleBorders(StrEnum):
    HORIZ = "\u2550"
    VERT = "\u2551"
    TOP_LEFT = "\u2554"
    TOP_RIGHT = "\u2557"
    BOTTOM_LEFT = "\u255a"
    BOTTOM_RIGHT = "\u255d"
    HORIZ_UP = "\u2569"
    HORIZ_DOWN = "\u2566"
    VERT_RIGHT = "\u2563"
    VERT_LEFT = "\u2560"
    CROSS = "\u256c"

# noinspection PyUnresolvedReferences
def map_joiner(north: bool, east: bool, south: bool, west: bool, btype: type[StrEnum] = LightBorders) -> str:
    char_map = {
        #north  east   south  west
        (False, False, False, False): " ",
        (False, False, False, True ): "w",
        (False, False, True,  False): "s",
        (False, False, True,  True ): btype.TOP_RIGHT,
        (False, True,  False, False): "e",
        (False, True,  False, True ): btype.HORIZ,
        (False, True,  True,  False): btype.TOP_LEFT,
        (False, True,  True,  True ): btype.HORIZ_DOWN,
        (True,  False, False, False): "n",
        (True,  False, False, True ): btype.BOTTOM_RIGHT,
        (True,  False, True,  False): btype.VERT,
        (True,  False, True,  True ): btype.VERT_RIGHT,
        (True,  True,  False, False): btype.BOTTOM_LEFT,
        (True,  True,  False, True ): btype.HORIZ_UP,
        (True,  True,  True,  False): btype.VERT_LEFT,
        (True,  True,  True,  True ): btype.CROSS,
    }
    return char_map.get((north, east, south, west))

# noinspection PyUnresolvedReferences
def _print_test_box(btype: type[StrEnum] = LightBorders):
    extra = 5
    if len(btype.__name__) % 2:
        extra += 1
    name = str(btype.__name__).center(len(btype.__name__) + extra)
    name_width = len(name)
    left = name_width//2
    right = name_width - left
    print(btype.TOP_LEFT + btype.HORIZ * left + btype.HORIZ_DOWN + btype.HORIZ * right + btype.TOP_RIGHT)
    print(btype.VERT_LEFT + btype.HORIZ * left + btype.CROSS + btype.HORIZ * right + btype.VERT_RIGHT)
    print(btype.VERT_LEFT + btype.HORIZ * left + btype.HORIZ_UP + btype.HORIZ * right + btype.VERT_RIGHT)
    print(btype.VERT + name + " " + btype.VERT)
    print(btype.BOTTOM_LEFT + btype.HORIZ * (name_width+1) + btype.BOTTOM_RIGHT)

if __name__ == '__main__':
    _print_test_box(LightBorders)
    _print_test_box(HeavyBorders)
    _print_test_box(DoubleBorders)