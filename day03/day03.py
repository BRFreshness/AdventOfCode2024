from icecream import ic
import re


def main():
    with open('input.txt') as f:
        text = f.read()

    mul_pattern = r"mul\((\d\d?\d?),(\d\d?\d?)\)"
    do_pattern = r"(do\(\))"
    dont_pattern = r"(don't\(\))"

    pattern = re.compile(mul_pattern, re.MULTILINE)
    sum = 0
    for match in pattern.findall(text):
        product = int(match[0])*int(match[1])
        sum += product
    print(sum)

    pattern = re.compile(f"({mul_pattern}|{do_pattern}|{dont_pattern})", re.MULTILINE)
    sum = 0
    do_flag = True
    for match in pattern.findall(text):
        product = None
        if "mul" in match[0]:
            product = int(match[1])*int(match[2])
            if do_flag:
                sum += product
        if "do()" in match[0]:
            do_flag = True
        if "don't()" in match[0]:
            do_flag = False
        # print(do_flag, product, sum, match)
    print(sum)


if __name__ == "__main__":
    main()
