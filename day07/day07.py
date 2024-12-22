from icecream import ic
import re
from itertools import product

debug = False

def add(a: int, b: int) -> int:
    return a + b

def mult(a: int, b: int) -> int:
    return a * b

def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")

def test_functions(target: int, args: list[int], functions: list) -> bool:
    if debug:
        print(f"{target=} {args=}")
    for combination in product(functions, repeat=len(args)-1):
        comb_string = " ".join([op.__name__ for op in combination])
        if debug:
            print(f"{comb_string=}")
        a = args[0]
        for index in range(len(args)-1):
            b = args[index+1]
            op = combination[index]
            value = op(a, b)
            if debug:
                print(f"  {op.__name__}({a},{b}) -> {value}")
            a = value
        if a == target:
            if debug:
                print(f"found!")
            return True
    return False

def main():
    for functions in ([add, mult], [add, mult, concat]):
        with open('input.txt') as f:
            total = 0
            for line in f:
                m = [int(val) for val in re.findall(r"(\d+)", line)]
                if test_functions(m[0], m[1:], functions):
                    total += m[0]
        func_string = ", ".join([f.__name__ for f in functions])
        print(f"[{func_string}] {total=}")


if __name__ == "__main__":
    main()

