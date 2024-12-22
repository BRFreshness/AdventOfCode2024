from icecream import ic
import re

ic.lineWrapWidth = 200

attempted_files = []

def compact(block_map: list) -> bool:
    first_empty_block = block_map.index('.')
    last_file_block = None
    # ic(len(block_map))
    for index in range(len(block_map)-1, 0, -1):
        # ic(index, block_map[index])
        if block_map[index] != '.':
            last_file_block = index
            break
    # ic(first_empty_block, last_file_block)
    if first_empty_block < last_file_block:
        block_map[first_empty_block] = block_map[last_file_block]
        block_map[last_file_block] = '.'
        return True
    return False

def find_last_file(block_map: list, end_index: int) -> (str,int,int):
    for last_file_block in range(end_index - 1, 0, -1):
        if block_map[last_file_block] != '.':
            file_id = block_map[last_file_block]
            first_file_block = block_map.index(file_id)
            file_len = last_file_block - first_file_block + 1
            return file_id, first_file_block, file_len
    return None, None, None

def find_space(block_map: list, width: int) -> int:
    location = 0
    while location < len(block_map):
        try:
            location = block_map.index('.', location)
        except ValueError:
            break
        sub_block = "".join(block_map[location:location + width])
        # ic(location, sub_block, width)
        if sub_block == "." * width:
            return location
        location += width
    return -1

def defrag(block_map: list) -> bool:
    location = len(block_map)
    # ic(attempted_files)
    while True:
        file_id, file_block, file_len = find_last_file(block_map, location)
        if file_id is None:
            return False
        if file_id in attempted_files:
            location = file_block
            continue
        attempted_files.append(file_id)

        space_block = find_space(block_map, file_len)
        # ic(file_id, file_block, file_len, space_block)
        if space_block < 0 or space_block > file_block:
            location = file_block-1
            continue
        # ic("moving", file_id)
        for index in range(space_block, space_block+file_len):
            block_map[index] = file_id
        for index in range(file_block, file_block+file_len):
            block_map[index] = "."
        return True
    return False


def compute_checksum(block_map: list) -> int:
    checksum = 0
    for position, token in enumerate(block_map):
        if token == ".":
            continue
        checksum += int(token) * position
    return checksum

def main():
    with open("input.txt") as f:
        disk_map = f.readline()
    block_map = []
    next_file_id = 0
    file_space_flag = True  # True for file, False for space
    for token in list(disk_map):
        if file_space_flag:
            file_id = next_file_id
            next_file_id += 1
            file_length = int(token)
            block_map.extend([str(file_id)] * file_length)
        else:
            block_map.extend(["."] * int(token))
        file_space_flag = not file_space_flag

    original_map = block_map.copy()

    # compact the disk for step 1
    while compact(block_map):
        if len(block_map) < 200:
            print("".join(block_map))
    print(f"Checksum = {compute_checksum(block_map)}")

    # defrag the disk for step 2
    block_map = original_map.copy()
    if len(block_map) < 200:
        print("----")
        print("".join(block_map))
    while defrag(block_map):
        if len(block_map) < 200:
            print("".join(block_map))
    print(f"Checksum = {compute_checksum(block_map)}")

if __name__ == "__main__":
    main()