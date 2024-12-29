import random
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
    new_stones = []
    depth_target = 25
    for i, stone in enumerate(stones.copy()):
        new_stones.extend(blink_single_stone(stone, depth_target))
        print()
    print(f"{len(new_stones)=}")
    print(f"{len(global_solutions)=}")
    for stone in stones:
        for _ in range(3):
            i = random.randint(1, 10)
            print(f"{(stone,i)} => {global_solutions[(stone,i)]}")


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
    # main("input.txt")

