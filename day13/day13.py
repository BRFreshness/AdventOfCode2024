import re
import sympy
from icecream import ic
ic.lineWrapWidth = 200

def solve(aa: tuple, bb: tuple, prize: tuple, extra: int = 0):
    px = prize[0] + extra
    py = prize[1] + extra
    ax = aa[0]
    ay = aa[1]
    bx = bb[0]
    by = bb[1]
    b = (py * ax - px * ay) / (by * ax - bx * ay)
    a = (px - b * bx) / ax

    if int(a) != a or int(b) != b or a * ax + b * bx != px or a * ay + b * by != py:
        return 0, 0
    return int(a), int(b)


def main(filename: str):
    pattern = re.compile(pattern=r"Button A: X\+(\d+), Y\+(\d+)\s*Button B: X\+(\d+), Y\+(\d+)\s*Prize: X\=(\d+), Y\=(\d+)",
                         flags=re.MULTILINE)
    with open(filename) as f:
        text = f.read()

    extra = 10000000000000
    # extra = 0
    pressed = [0, 0]
    for m in pattern.finditer(text):

        if len(m.groups()) < 6:
            raise RuntimeError(f"Patten matching problem: {m.groups()}")
        aa = (int(m.group(1)), int(m.group(2)))
        bb = (int(m.group(3)), int(m.group(4)))
        prize = (int(m.group(5)), int(m.group(6)))
        a, b = solve(aa, bb, prize, extra=extra)

        pressed[0] += a
        pressed[1] += b

    tokens = pressed[0] * 3 + pressed[1]
    print(f"{pressed=} {tokens=}")


if __name__ == "__main__":
    # main("sample.txt")
    main("input.txt")
