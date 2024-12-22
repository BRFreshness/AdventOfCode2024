import numpy as np
from icecream import ic
from rich.panel import Panel
from rich.console import Console
from itertools import combinations

console = Console(stderr=True)
console.width = 200
ic.lineWrapWidth = 200

debug = False

def print_map(input_map: np.ndarray):
    lines = []
    for line in input_map:
        lines.append("".join(list(line)))
    panel = Panel("\n".join(lines), expand=False)
    console.print(panel)
    antinodes = count_antinodes(input_map)
    ic(antinodes)

def count_antinodes(course: np.array) -> int:
    antinodes = 0
    for row in course:
        antinodes += list(row).count("#")
    return antinodes

def main():
    m = []
    frequencies = {}
    with open('input.txt') as f:
        for row, line in enumerate(f):
            l = list(line.strip())
            m.append(l)
            for col, char in enumerate(l):
                if char != ".":
                    if char not in frequencies:
                        frequencies[char] = []
                    frequencies[char].append((row,col))
    area_map = np.array(m)
    print_map(area_map)
    single_antinode = False
    for frequency in frequencies:
        antinode_map = np.full(area_map.shape, " ")
        for node in frequencies[frequency]:
            antinode_map[*node] = frequency
            if not single_antinode and len(frequencies[frequency]) > 1:
                area_map[*node] = "#"
        if debug:
            ic(frequency, frequencies[frequency])
        for nodeA, nodeB in combinations(frequencies[frequency], 2):
            diff_y = nodeA[0] - nodeB[0]
            diff_x = nodeA[1] - nodeB[1]
            index = 0
            while True:
                index += 1
                antinode = (nodeA[0] + diff_y * index, nodeA[1] + diff_x * index)
                in_range = True
                if antinode[0] in range(area_map.shape[0]) and antinode[1] in range(area_map.shape[1]):
                    area_map[*antinode] = "#"
                    antinode_map[*antinode] = "#"
                if antinode[0] not in range(area_map.shape[0]) and antinode[1] not in range(area_map.shape[1]):
                    in_range = False
                antinode = (nodeB[0] - diff_y * index, nodeB[1] - diff_x * index)
                if antinode[0] in range(area_map.shape[0]) and antinode[1] in range(area_map.shape[1]):
                    area_map[*antinode] = "#"
                    antinode_map[*antinode] = "#"
                else:
                    if not in_range:
                        if antinode[0] not in range(area_map.shape[0]) and antinode[1] not in range(area_map.shape[1]):
                            break
                if single_antinode:
                    break
        if debug:
            print_map(antinode_map)
    print_map(area_map)

if __name__ == "__main__":
    main()
