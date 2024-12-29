# from icecream import ic

class BlinkResult:
    def __init__(self, stones: list[int], depth: int, keep_list: bool = False):
        self.stones = stones
        self.depth = depth
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

    def _apply_rules_depth_first(self, stone: int, count: int, depth: int) -> int:
        if depth == self.depth:
            self.add_stone(stone)
            return count
        depth += 1
        new_stones = apply_rules(stone)
        count += len(new_stones) - 1
        for stone in new_stones:
            count += self._apply_rules_depth_first(stone, count, depth)
        return count

    def blink_depth_first(self):
        count = 0
        for stone in self.stones:
            count += self._apply_rules_depth_first(stone, 1,0)
        print(f"my count: {count}")

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

def main():
    with open("sample.txt") as f:
        line = f.readline()
        stones = [int(x) for x in line.strip().split(" ")]
    print(f"{len(stones)} stones: {stones}")

    # --------------------------------
    # part 2
    # --------------------------------
    depth_target = 2

    final_string = []
    solutions = {}
    for i, stone in enumerate(stones.copy()):
        new_stones = []
        depth = depth_target
        if (stone, depth) in solutions:
            # new_stones.extend(solutions[(stone, depth)])
            new_stones = solutions[(stone, depth)].copy()


        for depth in range(1, depth_target + 1):
            if (stone, depth) in solutions:
                stones = solutions[(stone, depth)]
            else:
                stones = blink(stones)
                solutions[(stone, depth)] = stones
            final_string.extend(stones)

if __name__ == "__main__":
    main()

