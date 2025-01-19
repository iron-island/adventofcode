from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from math import ceil, inf
from collections import defaultdict

input_file = "../../inputs/2024/input09.txt"

def get_checksum(start_idx, length, file_id):
    sum_idx = 0
    for i in range(start_idx, start_idx+length):
        sum_idx += i
    return sum_idx*file_id

# Optimized solution
def part1_part2(in_file):
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            disk = [int(x) for x in line]

            line = file.readline()


    # Part 1
    is_block = True
    idx = 0

    # Get IDs
    len_disk = len(disk)
    id_num = 0
    id_num_end = ceil(len_disk/2) - 1

    # Get block count of last file, which is always
    # at index id_num_end*2
    count = disk[id_num_end*2]
    part1 = 0
    for digit in disk:
        if (is_block):
            if (id_num < id_num_end):
                # Compute indices*id_num where indices is just
                # the sum of an arithmetic sequence of length digit
                # starting from idx
                part1 += get_checksum(idx, digit, id_num)
                idx += digit
                id_num += 1

                is_block = False
            elif (id_num == id_num_end):
                # Compute indices*id_num where indices is just
                # the sum of an arithmetic sequence of length count
                # starting from idx
                part1 += get_checksum(idx, count, id_num)
                break
            elif (id_num > id_num_end):
                break
        else:
            # Iteratively move blocks pointed by id_num_end to the
            #   spaces
            spaces = digit
            while True:
                # If there are enough files to fill in the spaces
                if (count >= spaces):
                    # Compute indices*id_num_end where indices is just
                    # the sum of an arithmetic sequence of length spaces
                    # starting from idx
                    part1 += get_checksum(idx, spaces, id_num_end)
                    idx += spaces
                    count = count-spaces

                    # Space has been filled exactly
                    # If file block count is depleted, move on to next end ID number
                    # before proceeding to next digit
                    if (count == 0):
                        id_num_end -= 1
                        count = disk[id_num_end*2]
                    break
                # Else there were not enough blocks to fill in the space
                else:
                    # Compute indices*id_num_end where indices is just
                    # the sume of an arithmetic sequence of length count
                    # starting from idx
                    part1 += get_checksum(idx, count, id_num_end)
                    idx += count
                    spaces = spaces-count

                    # New count value would be the next end file
                    id_num_end -= 1
                    count = disk[id_num_end*2]

            is_block = True

    # Part 2
    # Dictionaries for ID number : (index, length) mapping
    block_id_dict = defaultdict(tuple)
    space_id_dict = defaultdict(tuple)
    # Data structure for space length : [space ID numbers] mapping
    length_dict = defaultdict(list)
    is_block = True
    idx = 0
    id_num = 0
    for length in disk:
        if (is_block):
            block_id_dict[id_num] = (idx, length)
            is_block = False
        else:
            space_id_dict[id_num] = (idx, length)
            if (length > 0):
                length_dict[length].append(id_num)
            id_num += 1
            is_block = True

        idx += length

    # Start moving blocks to lower spaces
    part2 = 0
    moved_id_set = set()
    for id_num_block in range(id_num, -1, -1):
        _, block_length = block_id_dict[id_num_block]
        if (block_length == 0):
            continue

        # A block can occupy block_length, block_length+1, ..., 9
        #   so iterate through all those space_lengths and find the
        #   leftmost space by checking the lowest space ID number
        MIN_ID_NUM_SPACE = inf
        for space_length in range(block_length, 10):
            space_list = length_dict[space_length]
            if (space_list):
                MIN_ID_NUM_SPACE = min(space_list[0], MIN_ID_NUM_SPACE)

        # Move the file block only if space ID is lower than file block ID,
        #   meaning that the file block can be moved to the left
        if (MIN_ID_NUM_SPACE < id_num_block):
            # Remove the space ID from the list
            idx, space_length = space_id_dict[MIN_ID_NUM_SPACE]
            length_dict[space_length].pop(0)

            # Compute checksum contribution of filled in space
            part2 += get_checksum(idx, block_length, id_num_block)
            moved_id_set.add(id_num_block)

            # If space was higher than file block length,
            #   add to the list of the remaining unoccupied space,
            #   and update the (idx, length) in that space's ID
            remaining_length = space_length-block_length
            if (remaining_length > 0):
                length_dict[remaining_length].append(MIN_ID_NUM_SPACE)
                length_dict[remaining_length].sort()

                space_id_dict[MIN_ID_NUM_SPACE] = (idx+block_length, remaining_length)

    # Compute checksum of file blocks that weren't moved
    for id_num in block_id_dict:
        if (id_num not in moved_id_set):
            idx, length = block_id_dict[id_num]
            part2 += get_checksum(idx, length, id_num)

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 9: Disk Fragmenter ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
