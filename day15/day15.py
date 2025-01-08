import numpy as np

moves: list[tuple] = []

def print_map(m: np.array, hdr: str = None):
    if hdr:
        print(hdr)
    for line in m:
        print("".join(line))
    print()


def move_robot(m: np.array, cmd: str):
    global moves
    # find waldo (the robot). Assume there is exactly one robot
    items = np.where(m == "@")
    if len(items[0]) == 1:
        robot = (int(items[0][0]), int(items[1][0]))
    elif len(items[0]) == 0:
        raise RuntimeError("Can't find robot '@' symbol")
    else:
        raise RuntimeError("More than one robot '@' symbol found")

    # dictionary to translate a command into a direction
    direction = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
    if cmd not in direction:
        raise RuntimeError(f"Invalid robot motion command: '{cmd}'")

    def calc_next(cur_loc: tuple) -> tuple:
        return cur_loc[0] + direction[cmd][0], cur_loc[1] + direction[cmd][1]

    moves.clear()
    moves.append(robot)

    def add_move(loc: tuple):
        global moves
        if loc not in moves:
            moves.append(loc)

    def check(loc: tuple) -> bool:
        if m[loc] == ".":
            return True
        if m[loc] == "#":
            return False
        if m[loc] == "O":
            add_move(loc)
            return check(calc_next(loc))
        if m[loc] == "[" or m[loc] == "]":
            add_move(loc)
            left_right = -1 if m[loc] == "]" else 1
            adjacent = (loc[0], loc[1] + left_right)
            if cmd == "^" or cmd == "v":
                add_move(adjacent)
                return check(calc_next(loc)) & check(calc_next(adjacent))
            else:
                return check(calc_next(loc))
        raise RuntimeError(f"Unknown map cell '{m[loc]} at {loc}'")

    if check(calc_next(robot)):
        # sort the moves to avoid glitches when moving
        axes = 0 if cmd == "^" or cmd == "v" else 1
        reverse = False if cmd == "^" or cmd == "<" else True
        moves.sort(key=lambda x: x[axes], reverse=reverse)
        for move in moves:
            m[calc_next(move)] = m[move]
            m[move] = "."

def gps_sum(m: np.array):
    total = 0
    items = np.where((m == "O") | (m == "["))
    if len(items[0]) == 0:
        raise RuntimeError("Can't find inventory 'O' or '[' symbols")
    for loc in zip(*items):
        item_loc = (int(loc[0]), int(loc[1]))
        total += item_loc[0] * 100 + item_loc[1]
    print(f"GPS sum: {total}")


def main(filename: str, part: str = "part1", debug = False):
    map_lines = []
    directions = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                if line[0] == "#":
                    map_lines.append(list(line))
                else:
                    directions.extend(list(line))

    if part == "part2":
        conversion = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@."
        }
        for row, line in enumerate(map_lines):
            map_lines[row] = list("".join([conversion[c] for c in line]))
    warehouse = np.array(map_lines)

    print_map(warehouse)
    print()

    for i, command in enumerate(directions):
        hdr = f"cmd {i+1}/{len(directions)}: {command}"
        # print(hdr)
        move_robot(warehouse, command)
        if debug:
            print_map(warehouse, hdr)

    if not debug:
        print_map(warehouse)
        print()

    gps_sum(warehouse)


if __name__ == "__main__":
    # main("sample3.txt", "part2")
    # main("sample2.txt", "part2",  )
    main(filename="input.txt", part="part2", debug=False)
