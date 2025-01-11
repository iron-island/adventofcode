import copy

input_file = "../../inputs/2024/input11.txt"
example_file = "example11.txt"
example_file = "example11_2.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    s_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line = line.split()
            s_list = [int(x) for x in line]

            line = file.readline()

    # Blink
    new_list = copy.deepcopy(s_list)
    for b in range(0, 25):
        #print(new_list)
        #print(b)
        offset = 0
        for idx, s in enumerate(s_list):
            #print(f'idx = {idx}, s = {s}')
            if (s == 0):
                new_list[idx+offset] = 1
            else:
                s_char = str(s)
                if ((len(s_char) % 2) == 0):
                    length = len(s_char)
                    half = int(length/2)
                    left_s = s_char[0:half]
                    right_s = s_char[half:]

                    new_list[idx+offset] = int(right_s)
                    new_list.insert(idx+offset, int(left_s))
                    offset += 1
                else:
                    new_list[idx+offset] = s*2024

        # Update
        s_list = copy.deepcopy(new_list)

    output = len(new_list)

    return output

def process_inputs2(in_file):
    output = 0

    s_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line = line.split()
            s_list = [int(x) for x in line]

            line = file.readline()

    # Dictionary
    s_dict = {}
    for s in s_list:
        if (s not in s_dict):
            s_dict[s] = 1
        else:
            s_dict[s] += 1
    new_dict = copy.deepcopy(s_dict)

    # Blink
    BLINKS = 75
    part1 = 0
    for b in range(1, BLINKS+1):
        #print(f'Blink {b}:')
        #print(new_dict)
        for s in s_dict:
            num = s_dict[s]
            if (num == 0):
                continue

            if (s == 0):
                new_s = 1

                new_dict[s] -= num
                if (new_s in new_dict):
                    new_dict[new_s] += num
                else:
                    new_dict[new_s] = num
            else:
                s_char = str(s)
                if ((len(s_char) % 2) == 0):
                    length = len(s_char)
                    half = int(length/2)
                    left_s = int(s_char[0:half])
                    right_s = int(s_char[half:])

                    new_dict[s] -= num
                    if (left_s in new_dict):
                        new_dict[left_s] += num
                    else:
                        new_dict[left_s] = num

                    if (right_s in new_dict):
                        new_dict[right_s] += num
                    else:
                        new_dict[right_s] = num
                else:
                    new_s = int(s*2024)
                    #if (s == 2) and (b == BLINKS):
                    #    print(f's = 2 with num = {num}, and new_s = {new_s}')

                    new_dict[s] -= num
                    if (new_s in new_dict):
                        #if (s == 2) and (b == BLINKS):
                        #    print("Add 4048 to dict")
                        new_dict[new_s] += num
                    else:
                        new_dict[new_s] = num
                        #if (s == 2) and (b == BLINKS):
                        #    print(f'Initialize {new_s} to dict with {num}')
                        #    print(f'new_dict[new_s] = {new_dict[new_s]}')
        # Part 1: Compute when blinks are 25
        if (b == 25):
            part1 = sum(new_dict.values())
        # Update
        s_dict = copy.deepcopy(new_dict)

    part2 = sum(new_dict.values())
    
    return part1, part2

    # Evaluate
    #for s in new_dict:
    #    num = new_dict[s]
    #    #print(f'{s}: {num}')
    #    #assert(num >= 0)
    #    output += num

    # Blink
    #s_list = [4610211]
    #s_list = [4] # 13
    #s_list = [0] # 17
    #s_list = [59] # 14
    #s_list = [3907] # 14
    #s_list = [201586]
    #s_list = [586] # after blink
    #s_list = [929] # 16
    #s_list = [33750]
    #new_list = copy.deepcopy(s_list)

    #for b in range(0, 50):
    #    #print(new_list)
    #    #print(b)
    #    offset = 0
    #    cycle_count = 0
    #    for idx, s in enumerate(s_list):
    #        if (s in s_dict):
    #            cycle_count += 1
    #        else:
    #            s_dict[s] = 1

    #        if (s == 0):
    #            new_list[idx+offset] = 1
    #        else:
    #            s_char = str(s)
    #            if ((len(s_char) % 2) == 0):
    #                length = len(s_char)
    #                half = int(length/2)
    #                left_s = s_char[0:half]
    #                right_s = s_char[half:]

    #                new_list[idx+offset] = int(right_s)
    #                new_list.insert(idx+offset, int(left_s))
    #                offset += 1
    #            else:
    #                new_list[idx+offset] = s*2024

    #    # Check cycles
    #    if (cycle_count == len(s_list)):
    #        print(f'Cycles at b = {b}')
    #    #else:
    #    #    print(f'Cycle difference = {cycle_count - len(s_list)}')

    #    # Update
    #    s_list = copy.deepcopy(new_list)

    #output = len(new_list)

    #return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part1, part2 = process_inputs2(input_file)

#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
