import math

input_file = "../../inputs/2021/input16.txt"
example_file = "example16.txt"
example2_file = "example16_2.txt"
example3_file = "example16_3.txt"
example4_file = "example16_4.txt"
example5_file = "example16_5.txt"
example6_file = "example16_6.txt"
example7_file = "example16_7.txt"
example8_file = "example16_8.txt"
example9_file = "example16_9.txt"
example10_file = "example16_10.txt"
example11_file = "example16_11.txt"
example12_file = "example16_12.txt"
example13_file = "example16_13.txt"
example14_file = "example16_14.txt"
example15_file = "example16_15.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part1_example4 = 0
part1_example5 = 0
part1_example6 = 0
part1_example7 = 0
part1 = 0

part2_example = 0
part2_example8 = 0
part2_example9 = 0
part2_example10 = 0
part2_example11 = 0
part2_example12 = 0
part2_example13 = 0
part2_example14 = 0
part2_example15 = 0
part2 = 0

val_list = []

def dfs_packet(bin_message):
    # Base case
    if (bin_message == "") or (int(bin_message, base=2) == 0):
        return 0

    version = int(bin_message[0:3], base=2)
    type_id = int(bin_message[3:6], base=2)
    print(f'version: {version}, type = {type_id}')

    if (type_id == 4): # literal
        print("  literal packet")
        group_offset = 6
        group_num = 0
        while True:
            group = bin_message[group_offset:group_offset+5]
            group_offset += 5
            group_num = (group_num << 4) + int(group[1:], base=2)
            print(f'  group {int((group_offset-6)/5)}: val = {group_num}')
            if (group[0] == "0"):
                break

        version += dfs_packet(bin_message[group_offset:])
    else: # operator packet
        if (bin_message[6] == "0"):
            print("  operator mode 0")
            # Next 15 bits for length of sub-packet
            length_subpacket = int(bin_message[7:22], base=2)
            idx_end = 22 + length_subpacket
            print(f'  15-bit length = {length_subpacket}')

            version += dfs_packet(bin_message[22:idx_end])
            version += dfs_packet(bin_message[idx_end:])
        else:
            print("  operator mode 1")
            # Next 11 bits for number of sub-packets
            num_subpackets = int(bin_message[7:18], base=2)

            version += dfs_packet(bin_message[18:])

    return version

def dfs_packet2(bin_message):
    global val_list

    # Base case
    if (bin_message == "") or (int(bin_message, base=2) == 0):
        return

    version = int(bin_message[0:3], base=2)
    type_id = int(bin_message[3:6], base=2)
    print(f'version: {version}, type = {type_id}')

    if (type_id == 4): # literal
        print("  literal packet")
        group_offset = 6
        group_num = ""
        while True:
            group = bin_message[group_offset:group_offset+5]
            group_offset += 5
            #group_num = (group_num << 4) + int(group[1:], base=2)
            group_num += group[1:]
            print(f'  group {int((group_offset-6)/5)}: val = {int(group_num, base=2)}')
            if (group[0] == "0"):
                break
        val_list.append(int(group_num, base=2))

        dfs_packet2(bin_message[group_offset:])
    else: # operator packet
        # Modes
        if (bin_message[6] == "0"):
            print("  operator mode 0")
            # Next 15 bits for length of sub-packet
            length_subpacket = int(bin_message[7:22], base=2)
            idx_end = 22 + length_subpacket
            print(f'  15-bit length = {length_subpacket}')

            start_length = len(val_list)
            val_idx_start = start_length

            dfs_packet2(bin_message[22:idx_end])
            end_length = len(val_list)
            val_idx_end = end_length

            subval_list = val_list[val_idx_start:val_idx_end]
            #subval_list = []
            #for i in range(0, val_idx_end-val_idx_start):
            #    subval_list.append(val_list.pop(-1))
            # Operation
            if (type_id == 0):
                val = sum(subval_list)
            elif (type_id == 1):
                val = 1
                for subval in subval_list:
                    val = val*subval
            elif (type_id == 2):
                val = min(subval_list)
            elif (type_id == 3):
                val = max(subval_list)
            elif (type_id == 5):
                assert(len(subval_list) == 2)
                val = 0
                if (subval_list[0] > subval_list[1]):
                    val = 1
            elif (type_id == 6):
                assert(len(subval_list) == 2)
                val = 0
                if (subval_list[0] < subval_list[1]):
                    val = 1
            elif (type_id == 7):
                assert(len(subval_list) == 2)
                val = 0
                if (subval_list[0] == subval_list[1]):
                    val = 1
            for i in range(0, val_idx_end-val_idx_start):
                val_list.pop(val_idx_start)
            val_list.append(val)
            #print(val_list)

            dfs_packet2(bin_message[idx_end:])
        else:
            print("  operator mode 1")
            # Next 11 bits for number of sub-packets
            num_subpackets = int(bin_message[7:18], base=2)
            init_length = len(val_list)
            val_idx_start = init_length
            val_idx_end   = val_idx_start + num_subpackets

            dfs_packet2(bin_message[18:])

            #print(f'DEBUG: num_subpackets = {num_subpackets}, init_length = {init_length}, final_length = {len(val_list)}')

            subval_list = val_list[val_idx_start:val_idx_end]
            assert(num_subpackets == (val_idx_end - val_idx_start))
            #subval_list = []
            #for i in range(0, num_subpackets):
            #    subval_list.append(val_list.pop(-1))
            # Operation
            if (type_id == 0):
                val = sum(subval_list)
            elif (type_id == 1):
                val = 1
                for subval in subval_list:
                    val = val*subval
            elif (type_id == 2):
                val = min(subval_list)
            elif (type_id == 3):
                val = max(subval_list)
            elif (type_id == 5):
                assert(len(subval_list) == 2)
                val = 0
                if (subval_list[0] > subval_list[1]):
                    val = 1
            elif (type_id == 6):
                assert(len(subval_list) == 2)
                val = 0
                if (subval_list[0] < subval_list[1]):
                    val = 1
            elif (type_id == 7):
                assert(len(subval_list) == 2)
                val = 0
                if (subval_list[0] == subval_list[1]):
                    val = 1
            for i in range(0, val_idx_end-val_idx_start):
                val_list.pop(val_idx_start)
            val_list.insert(val_idx_start, val)
            #print(val_list)

def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()
            message = [x for x in line]
            line = file.readline()

    bin_message = ""
    for hex_num in message:
        bin_string = bin(int("0x" + hex_num, base=16))
        bin_string = f'{bin_string[2:]:>04}'
        bin_message += bin_string

    print(bin_message)
    output = dfs_packet(bin_message)

    return output

def process_inputs2(in_file):
    global val_list
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()
            message = [x for x in line]
            line = file.readline()

    bin_message = ""
    for hex_num in message:
        bin_string = bin(int("0x" + hex_num, base=16))
        bin_string = f'{bin_string[2:]:>04}'
        bin_message += bin_string

    print(bin_message)
    val_list = []
    dfs_packet2(bin_message)
    print(val_list)
    output = val_list[0]

    return output

part1_example = process_inputs(example_file)
part1_example2 = process_inputs(example2_file)
part1_example3 = process_inputs(example3_file)
part1_example4 = process_inputs(example4_file)
part1_example5 = process_inputs(example5_file)
part1_example6 = process_inputs(example6_file)
part1_example7 = process_inputs(example7_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2_example8 = process_inputs2(example8_file)
part2_example9 = process_inputs2(example9_file)
part2_example10 = process_inputs2(example10_file)
part2_example11 = process_inputs2(example11_file)
part2_example12 = process_inputs2(example12_file)
part2_example13 = process_inputs2(example13_file)
part2_example14 = process_inputs2(example14_file)
part2_example15 = process_inputs2(example15_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1 example4: {part1_example4}')
print(f'Part 1 example5: {part1_example5}')
print(f'Part 1 example6: {part1_example6}')
print(f'Part 1 example7: {part1_example7}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example8: {part2_example8}')
print(f'Part 2 example9: {part2_example9}')
print(f'Part 2 example10: {part2_example10}')
print(f'Part 2 example11: {part2_example11}')
print(f'Part 2 example12: {part2_example12}')
print(f'Part 2 example13: {part2_example13}')
print(f'Part 2 example14: {part2_example14}')
print(f'Part 2 example15: {part2_example15}')
print(f'Part 2: {part2}')
