from icecream import ic

ic.lineWrapWidth = 200

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
        while location < len(block_map) and block_map[location] == '.':
            location = location + 1
    return -1

def defrag(block_map: list):

    # find last file number
    index = len(block_map)-1
    while block_map[index] == '.':
        index -= 1
    last_file_id = block_map[index]

    # try to move each file, starting with the highest ID, to a lower location
    for file_number in range(int(last_file_id)+1).__reversed__():
        file_id = str(file_number)
        file_location = block_map.index(file_id)
        file_len = 1
        while file_location+file_len < len(block_map) and block_map[file_location+file_len] == file_id:
            file_len += 1
        space_location = find_space(block_map, file_len)
        if space_location < 0 or space_location > file_location:
            continue
        for i in range(space_location, space_location+file_len):
            block_map[i] = file_id
        for i in range(file_location, file_location+file_len):
            block_map[i] = "."

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
    defrag(block_map)
    if len(block_map) < 200:
        print("".join(block_map))
    print(f"Checksum = {compute_checksum(block_map)}")

if __name__ == "__main__":
    main()