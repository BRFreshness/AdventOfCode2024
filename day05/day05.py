from icecream import ic
import re

ic.lineWrapWidth = 3000

def check_update(update: list, rules: list) -> bool:
    success = True
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            left_index = update.index(rule[0])
            right_index = update.index(rule[1])
            if left_index > right_index:
                success = False
    # print(f"  check: {update=} {success=}")
    return success

def fix_ordering(update: list, rules: list) -> list:
    new_update = update.copy()
    while check_update(new_update, rules) is False:
        for rule in rules:
            if rule[0] in new_update and rule[1] in new_update:
                left_index = new_update.index(rule[0])
                right_index = new_update.index(rule[1])
                if left_index > right_index:
                    left_value = new_update[left_index]
                    right_value = new_update[right_index]
                    new_update[left_index] = right_value
                    new_update[right_index] = left_value
    return new_update


def main():
    rules = []
    updates = []
    with open('input.txt') as f:
        for line in f:
            if m := re.match(r"(\d+)\|(\d+)", line):
                rules.append( (int(m.group(1)), int(m.group(2))) )
            elif len(pages := re.findall(r"(\d+)", line)) > 0:
                updates.append( [int(page) for page in pages] )
    # ic(rules)
    sum = 0
    fixed_sum = 0
    for update in updates:
        if check_update(update, rules):
            sum += update[int(len(update)/2)]
        else:
            new_update = fix_ordering(update, rules)
            fixed_sum += new_update[int(len(new_update)/2)]
            # ic(update, new_update)
    print(f"{sum=}, {fixed_sum=}")

if __name__ == "__main__":
    main()
