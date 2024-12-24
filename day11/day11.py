# import threading
import multiprocessing as mp
from icecream import ic
import time

class BlinkResult:
    def __init__(self, keep_list: bool = False):
        self.stone_list = []
        self.count = 0
        self.keep_list = keep_list
        self.solutions = {}

    def add_stone(self, stone: int):
        if self.keep_list:
            self.stone_list.append(stone)
        self.count += 1

    def add_solution(self, stone: int, depth: int, solution: int):
        self.solutions[(stone, depth)] =  solution

    def check_solution(self, stone: int, depth: int) -> int:
        if (stone, depth) in self.solutions:
            return self.solutions[(stone, depth)]
        return -1

def apply_rules(stone: int) -> list[int]:
    # ----------------------- rule #1 ----------------
    if stone == 0:
        return [1]
    # ----------------------- rule #2 ----------------
    str_stone = str(stone)
    length = len(str_stone)
    if length % 2 == 0:
        width = length//2
        left = int(str_stone[:width])
        right = int(str_stone[width:])
        return [left, right]
    # ----------------------- rule #3 ----------------
    return [stone * 2024]

def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
         new_stones.extend(apply_rules(stone))
    return new_stones

def apply_rules_depth_first(stone:int, depth: int, result: BlinkResult):
    if depth == 0:
        result.add_stone(stone)
        return
    depth -= 1
    new_stones = apply_rules(stone)
    for stone in new_stones:
        apply_rules_depth_first(stone, depth, result)

def blink_depth_first(stones: list[int], depth: int, result: BlinkResult):
    # start = time.time()
    # last_time = start
    # now = 0
    for i, stone in enumerate(stones):
        apply_rules_depth_first(stone, depth, result)
        # now = time.time()
        # elapsed = f"{now - last_time:.2f}s"
        # last_time = now
        # ic(i, result.count, elapsed)
    # total_time = f"{now - start:.2f}s"
    # ic(total_time)

def main():
    part = "part2"
    with open("input.txt") as f:
        line = f.readline()
        stones = [int(x) for x in line.strip().split(" ")]
    print(f"{len(stones)} stones: {stones}")

    # --------------------------------
    # part 1
    # --------------------------------
    if part == "part1":
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
    else:
        depth_target = 25
        result = BlinkResult(keep_list=False)
        blink_depth_first(stones, depth_target, result)
        print(f"{result.count=}")



if __name__ == "__main__":
    main()

