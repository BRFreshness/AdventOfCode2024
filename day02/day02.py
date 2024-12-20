from icecream import ic

# ic.disable()
ic.lineWrapWidth = 200

def check_levels(levels: list[int], verbose: bool = False) -> bool:
    if verbose:
        ic(levels)
    a = levels[0]
    b = levels[1]
    initial_direction = a-b
    if not initial_direction:
        if verbose:
            ic(initial_direction, a, b)
        return False
    for index in range(len(levels)-1):
        a = levels[index]
        b = levels[index+1]
        direction = a-b
        if direction * initial_direction <= 0:
            if verbose:
                ic(initial_direction, direction, index, a, b)
            return False
        if abs(direction) > 3:
            if verbose:
                ic(initial_direction, direction, index, a, b)
            return False
    return True

def recheck_levels(levels: list[int]) -> bool:
    for index in range(len(levels)):
        skipped_levels = levels[:index] + levels[index+1:]
        ic(levels, index, skipped_levels)
        if check_levels(skipped_levels):
            ic("PASS")
            return True
    ic('FAIL')
    return False

def main():
    total = 0
    recheck_total = 0
    with open('input.txt', 'r') as f:
        for report in f:
            levels = [int(level) for level in report.split()]
            ic.disable()
            check = check_levels(levels)
            if check:
                total += 1
            else:
                ic.enable()
                check = recheck_levels(levels)
                if check:
                    recheck_total += 1
    print(f"{total=} {recheck_total=} {total+recheck_total=}")


if __name__ == "__main__":
    main()
