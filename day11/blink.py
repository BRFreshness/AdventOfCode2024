
# ---------- for part 1 ---------------

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


# ---------- for part 2 ---------------

solutions = {}

def count_each_stone(stones: list[int], depth: int) -> int:
    count = 0
    for stone in stones:
        count += count_descendants(stone, depth)
    return count

def count_descendants(stone: int, depth: int) -> int:
    global solutions
    if (stone, depth) not in solutions:
        solutions[(stone, depth)] = recursive_count_descendants(stone, depth)
    return solutions[(stone, depth)]

def recursive_count_descendants(stone: int, depth: int) -> int:
    if depth == 0:
        return 1
    return count_each_stone(apply_rules(stone), depth - 1)
