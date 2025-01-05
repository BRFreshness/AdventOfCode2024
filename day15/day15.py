import numpy as np
from icecream import ic

def print_map(m: np.array):
    for line in m:
        print("".join(line))

def move_robot(m: np.array, command: str):
    items = np.where(m == "@")
    if len(items[0]) > 0:
        robot = (int(items[0][0]), int(items[1][0]))
    else:
        raise RuntimeError("Can't find robot '@' symbol")
    direction = {
        "^": (-1, 0),
        "v": (1, 0),
        ">": (0, 1),
        "<": (0, -1),
    }
    if command not in direction:
        raise RuntimeError(f"Invalid command: '{command}'")


    locations = [robot]
    next_loc = (robot[0] + direction[command][0], robot[1] + direction[command][1])
    while m[next_loc] != "#":
        if m[next_loc] == ".":
            while len(locations) > 0:
                prev_loc = locations.pop()
                m[next_loc] = m[prev_loc]
                m[prev_loc] = "."
                next_loc = prev_loc
            break
        else:
            locations.append(next_loc)
            next_loc = (next_loc[0] + direction[command][0], next_loc[1] + direction[command][1])

def gps_sum(m: np.array):
    sum = 0
    items = np.where(m == "O")
    if len(items[0]) == 0:
        raise RuntimeError("Can't find inventory 'O' symbol")
    for loc in zip(*items):
        item_loc = (int(loc[0]), int(loc[1]))
        sum += item_loc[0] * 100 + item_loc[1]
    print(f"GPS sum: {sum}")

def main(filename: str):
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
    warehouse = np.array(map_lines)
    print_map(warehouse)

    for command in directions:
        move_robot(warehouse, command)
    print_map(warehouse)

    gps_sum(warehouse)


if __name__ == "__main__":
    # main("sample1.txt")
    # main("sample2.txt")
    main("input.txt")
