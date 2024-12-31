from blink import *

# --------------------------------
# part 1
# --------------------------------
def part1(stones: list[int]):
    for i in range(25):
        stones = blink(stones)
        if i < 6:
            print(i+1, len(stones), stones)
        if i > 25:
            print(f"{i=}...")
    print(f"{len(stones)=}")

# --------------------------------
# part 2
# --------------------------------
def part2(stones: list[int]):
    depth_target = 75
    print(count_each_stone(stones, depth_target))

def main(filename: str):
    with open(filename) as f:
        line = f.readline()
        stones = [int(x) for x in line.strip().split(" ")]
    print("-----------------------------------------------")
    print(f"{filename}: {stones}")

    # part1(stones)
    part2(stones)

if __name__ == "__main__":
    main("sample.txt")
    main("input.txt")

