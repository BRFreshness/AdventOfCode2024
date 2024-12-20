import numpy as np
import re
from icecream import ic

ic.lineWrapWidth = 200

def search_word(line: list[str], word: str) -> int:
    line_str = "".join(line)
    pattern = re.compile(word)
    count = len(re.findall(pattern, line_str))
    pattern = re.compile(word[::-1])
    return count + len(re.findall(pattern, line_str))


def search(grid: np.array, word: str):
    width = grid.shape[0]
    height = grid.shape[1]

    count = 0

    for index in range(height):
        count += search_word(grid[index,:], word)

    for index in range(width):
        count += search_word(grid[:, index], word)

    flip_grid = np.fliplr(grid)
    for gr in (grid, flip_grid):
        width = gr.shape[0]
        height = gr.shape[1]
        for index in range(-(height-len(word)), width-len(word)+1):
            diag = [ str(element) for element in np.diagonal(gr, index) ]
            count += search_word(diag, word)
            # ic(diag)

    print(f"Total '{word}' found in grid: {count}")

def search_2d(grid: np.array, word: str):
    count = 0
    for _ in range(4):
        # print_grid(grid)
        count += search_2d_word(grid, word)
        grid = np.rot90(grid)
    print(f"Total 2d '{word}' found in grid: {count}")

def search_2d_word(grid: np.array, word: str) -> int:
    grid_size = grid.shape[0]
    target_size = int(np.sqrt(len(word)))
    if target_size != np.sqrt(len(word)):
        raise RuntimeError("Search target grid size is not a power of 2")
    if grid_size < target_size:
        raise RuntimeError("Grid size is smaller than search target size")
    if grid.shape[0] != grid.shape[1]:
        raise RuntimeError(f"Grid shape is not square: {grid.shape}")
    count = 0

    for row in range(grid_size - target_size + 1):
        for col in range(grid_size - target_size + 1):
            gr = grid[row:row+target_size, col:col+target_size]
            text = "".join(list(gr.flatten()))
            if re.match(word, text):
                count += 1
    return count

def print_grid(grid: np.array):
    for index in range(grid.shape[0]):
        left = "[ " if index == 0 else "  "
        right = " ]" if index == grid.shape[0]-1 else ""
        print(left + ("".join(grid[index,:])) + right)

def main():
    lines = []
    with open('input.txt') as f:
    # with open('sample.txt') as f:
        for line in f:
            letters = list(line.strip())
            lines.append(letters)
    grid = np.array(lines)
    print(grid)
    print(f"{grid.shape=}")

    search(grid, "XMAS")
    search_2d(grid, "M.S.A.M.S")


if __name__ == "__main__":
    main()
