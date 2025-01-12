from math import ceil, inf
from collections import defaultdict

input_file = "../../inputs/2024/input09.txt"
example_file = "example09.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def get_checksum(start_idx, length, file_id):
    sum_idx = 0
    for i in range(start_idx, start_idx+length):
        sum_idx += i
    return sum_idx*file_id

# Original solution, very slow, around 3m30s
#def process_inputs(in_file):
#    output = 0
#
#    with open(in_file) as file:
#        line = file.readline()
#    
#        while line:
#            line = line.strip()
#
#            disk = line
#
#            line = file.readline()
#
#    # Compact
#    compacted_disk = []
#    id_num = 0
#    blank_num = 0
#    blank_string = ""
#    for idx, d in enumerate(disk):
#        d_int = int(d)
#        if ((idx % 2) == 0): # file
#            for i in range(0, d_int):
#                compacted_disk.append(id_num)
#            id_num += 1
#        else: # blank
#            for i in range(0, d_int):
#                compacted_disk.append('.')
#                blank_num += 1
#                blank_string = blank_string + "."
#
#    # Compact
#    length = len(compacted_disk)
#    compacted_string = ""
#    iteration = 0
#    while (True):
#        if ((iteration % 1000) == 0):
#            print(f'{iteration} of {blank_num}')
#        iteration += 1
#
#        compacted_string = [str(x) for x in compacted_disk]
#        compacted_string = ''.join(compacted_string)
#        #print(compacted_string)
#        if (blank_string in compacted_string):
#            break
#        #if (compacted_disk[-blank_num:] == blank_string):
#        #    break
#
#        idx_from = 0
#        for idx_reverse in range(1, length):
#            num = compacted_disk[-idx_reverse]
#            if (num != '.'):
#                idx_from = idx_reverse
#                break
#        #print(num)
#
#        # Move num
#        for idx in range(0, length):
#            blank = compacted_disk[idx]
#            if (blank == '.'):
#                compacted_disk[-idx_from] = blank
#                compacted_disk[idx] = num
#                #print(idx)
#                break
#
#    # Evaluate
#    print(compacted_string)
#    for idx, d in enumerate(compacted_disk):
#        if (d == '.'):
#            break
#
#        output += idx*d
#
#    return output
#
#def process_inputs2(in_file):
#    output = 0
#
#    with open(in_file) as file:
#        line = file.readline()
#    
#        while line:
#            line = line.strip()
#
#            disk = line
#
#            line = file.readline()
#
#    # Compact
#    compacted_disk = []
#    id_num = 0
#    blank_num = 0
#    blank_string = ""
#    for idx, d in enumerate(disk):
#        d_int = int(d)
#        if ((idx % 2) == 0): # file
#            mydict = {}
#            mydict[id_num] = d_int
#            id_num += 1
#            #for i in range(0, d_int):
#            #    compacted_disk.append(id_num)
#            #id_num += 1
#        else: # blank
#            mydict = {}
#            mydict["blank"] = d_int
#            #for i in range(0, d_int):
#            #    compacted_disk.append('.')
#            #    blank_num += 1
#            #    blank_string = blank_string + "."
#        compacted_disk.append(mydict)
#
#    # Compact
#    for id_num_reverse in range(id_num-1, -1, -1):
#        #print(f'{id_num_reverse}: {compacted_disk}')
#
#        # find file ID = id_num_reverse
#        idx_file = -1
#        num_file = -1
#        for idx, mydict in enumerate(compacted_disk):
#            myid = list(mydict.keys())[0]
#            mynum = mydict[myid]
#
#            if (myid == id_num_reverse):
#                idx_file = idx
#                num_file = mynum
#                break
#
#        # Find blank segments
#        new_compacted_disk = compacted_disk
#        for idx, mydict in enumerate(compacted_disk):
#            myid = list(mydict.keys())[0]
#            mynum = mydict[myid]
#
#            if (myid == 'blank') and (idx < idx_file):
#                # debugging
#                #if (id_num_reverse == 7):
#                #    print(f'blank: {mynum}')
#                #    print(f'file:  {num_file}')
#
#                if (mynum == num_file):
#                    # Exchange if exact same length
#                    new_compacted_disk[idx] = {id_num_reverse: num_file}
#                    new_compacted_disk[idx_file] = {'blank': mynum}
#                    break
#                elif (mynum > num_file):
#                    new_compacted_disk[idx] = {id_num_reverse: num_file}
#                    new_compacted_disk[idx_file] = {'blank': num_file}
#                    new_compacted_disk.insert(idx+1, {'blank': mynum-num_file})
#                    break
#        compacted_disk = new_compacted_disk
#
#    # Evaluate
#    actual_idx = 0
#    for idx, mydict in enumerate(compacted_disk):
#        myid = list(mydict.keys())[0]
#        mynum = mydict[myid]
#
#        if (myid != 'blank'):
#            curr_sum = 0
#            for i in range(actual_idx, actual_idx+mynum):
#                partial_sum = i*myid
#                curr_sum += partial_sum
#                #print(partial_sum)
#            output += curr_sum
#
#        actual_idx += mynum
#
#    return output

# Optimized solution
def process_inputs_parts1_2(in_file):
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
                #print(f'File! Computing {id_num} times indices {idx} to {idx+digit-1}')
                #for i in range(idx, idx+digit):
                #    part1 += i*id_num
                part1 += get_checksum(idx, digit, id_num)
                idx += digit
                id_num += 1

                is_block = False
            elif (id_num == id_num_end):
                # Compute indices*id_num where indices is just
                # the sum of an arithmetic sequence of length count
                # starting from idx
                #print(f'File! Computing {id_num} times indices {idx} to {idx+count-1}')
                #for i in range(idx, idx+count):
                #    part1 += i*id_num
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
                    #print(f'Space1! Computing {id_num_end} times indices {idx} to {idx+spaces-1}')
                    #for i in range(idx, idx+spaces):
                    #    part1 += i*id_num_end
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
                    #print(f'Space2! Computing {id_num_end} times indices {idx} to {idx+count-1}')
                    #for i in range(idx, idx+count):
                    #    part1 += i*id_num_end
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

            #print(f'Moved {id_num_block} to indices {idx} to {idx+block_length-1}')

    # Compute checksum of file blocks that weren't moved
    for id_num in block_id_dict:
        if (id_num not in moved_id_set):
            #print(f'File block {id_num} not moved')
            idx, length = block_id_dict[id_num]
            part2 += get_checksum(idx, length, id_num)

    return part1, part2

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2 = process_inputs2(input_file)

#part1_example, part2_example = process_inputs_parts1_2(example_file)
part1, part2 = process_inputs_parts1_2(input_file)

print("")
print("--- Advent of Code 2024 Day 9: Disk Fragmenter ---")
#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
