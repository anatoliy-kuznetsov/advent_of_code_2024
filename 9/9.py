def construct_blocks(disk_map: list[str]) -> list[str]:
    blocks = []
    file_id = 0
    for i, size in enumerate(disk_map):
        if i % 2 == 0:
            blocks.extend([str(file_id) for _ in range(int(size))])
            file_id += 1
        else:
            blocks.extend(["." for _ in range(int(size))])
    return blocks

def rearrange_file_blocks_fragmented(blocks: list[str]) -> list[str]:
    rearranged_blocks = blocks.copy()
    last_block_index = len(blocks) - 1
    while blocks[last_block_index] == ".":
        last_block_index -= 1
    first_free_index = rearranged_blocks.index(".")
    while first_free_index < last_block_index:
        rearranged_blocks[first_free_index], rearranged_blocks[last_block_index] = rearranged_blocks[last_block_index], rearranged_blocks[first_free_index]
        while rearranged_blocks[last_block_index] == ".":
            last_block_index -= 1
        first_free_index = rearranged_blocks.index(".")
    return rearranged_blocks

def rearrange_files_unfragmented(disk_map: list[str]) -> list[str]:
    """
    Returns block representation of disk after rearrangement
    """
    memory_map = []
    """
    Represent disk as a list of blocks, each with:
    (id, size)
    """
    file_id = 0
    for i, size in enumerate(disk_map):
        if i % 2 == 0:
            memory_map.append((str(file_id), int(size)))
            file_id += 1
        else:
            memory_map.append((".", int(size)))
    new_map = memory_map.copy()
    for i, item in enumerate(memory_map[::-1]):
        if item[0] == ".":
            continue
        available_space_index = -1
        for j, block in enumerate(new_map):
            if block[0] == "." and block[1] >= item[1]:
                available_space_index = j
                break
            if block == item:
                break
        if available_space_index == -1:
            continue
        new_map[available_space_index] = (".", new_map[available_space_index][1] - item[1])
        freed_memory_index = new_map.index(item)
        # doesn't merge free memory, but OK for now since we just care about the checksum
        new_map[freed_memory_index] = (".", item[1])
        new_map.insert(available_space_index, item)
    blocks = []
    for item in new_map:
        blocks.extend([item[0] for _ in range(item[1])])
    return blocks

def calculate_checksum(blocks: list[str]) -> int:
    checksum = 0
    for i, block in enumerate(blocks):
        if block == ".":
            continue
        checksum += i * int(block)
    return checksum

with open("input.txt", "r") as f:
    line = f.readlines()[0].split()[0]
disk_map = [char for char in line]
blocks = construct_blocks(disk_map)
rearranged_blocks = rearrange_file_blocks_fragmented(blocks)
print(calculate_checksum(rearranged_blocks))
rearranged_blocks = rearrange_files_unfragmented(disk_map)
print(calculate_checksum(rearranged_blocks))