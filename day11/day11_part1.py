# from icecream import ic

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

def main(filename:str):
    with open(filename) as f:
        line = f.readline()
        stones = [int(x) for x in line.strip().split(" ")]
    print("-----------------------------------------------")
    print(f"{filename}: {stones}")

    # --------------------------------
    # part 1
    # --------------------------------
    for i in range(25):
        stones = blink(stones)
        if i < 6:
            print(i+1, len(stones), stones)
        if i > 25:
            print(f"{i=}...")
    print(f"{len(stones)=}")


if __name__ == "__main__":
    main("sample.txt")
    main("input.txt")

