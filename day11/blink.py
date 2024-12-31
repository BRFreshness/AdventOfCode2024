
global_solutions = {}

class Blink:
    def __init__(self, stones: list[int], depth: int, keep_list: bool = False):
        self.stones = stones
        self.depth = depth
        self.stone_list = []
        self.count = 0
        self.keep_list = keep_list
        self.solutions = {}
        self.debug = False

    def clear(self):
        self.stone_list = []
        self.count = 0
        self.solutions = {}

    def run(self):
        self.clear()
        for stone in self.stones:
            self.apply_rules(stone, count=1, depth=0)
            if self.debug:
                print()

    def add_stone(self, stone: int):
        if self.keep_list:
            self.stone_list.append(stone)
        self.count += 1

    def apply_rules(self, stone: int, count: int, depth: int) -> int:
        if depth == self.depth:
            self.add_stone(stone)
            return count
        depth += 1
        if (stone, depth) in self.solutions:
            new_stones = self.solutions[(stone, depth)]
            if self.debug:
                print(".", end="")
        else:
            new_stones = apply_rules(stone)
            self.solutions[(stone, depth)] = new_stones.copy()
            if self.debug:
                print("+", end="")
        count += len(new_stones) - 1
        for stone in new_stones:
            count += self.apply_rules(stone, count, depth)
        return count

    def print(self):
        print(f"depth={self.depth} count={self.count}", end="")
        if self.keep_list:
            print(f" len={len(self.stone_list)} stone_list[0:25]={self.stone_list[0:25]}")
        else:
            print()


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




