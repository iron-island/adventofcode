import numpy as np
from collections import defaultdict
from collections import deque
from functools import cache

input_file = "../../inputs/2024/input25.txt"
example_file = "example25.txt"
example2_file = "example_2.txt"
example3_file = "example_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

def process_inputs(in_file):
    output = 0

    lock_list = []
    key_list = []
    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        get_lock = False
        while line:
            line = line.strip()

            if (line == ""):
                row = 0
            elif (row == 0):
                if ("#" in line): # lock
                    get_lock = True
                    curr_heights = [0, 0, 0, 0, 0]
                elif ("." in line): # key
                    get_lock = False
                    curr_heights = [-1, -1, -1, -1, -1]
                row += 1
            else:
                for idx, l in enumerate(line):
                    if ('#' == l):
                        curr_heights[idx] += 1
                row += 1

                if (row == 7):
                    if (get_lock):
                        lock_list.append(curr_heights)
                    else:
                        key_list.append(curr_heights)

            line = file.readline()
    print(lock_list)
    print(key_list)

    # Count lock/key pairs
    output = 0
    for lock_heights in lock_list:
        l0, l1, l2, l3, l4 = lock_heights
        for key_heights in key_list:
            k0, k1, k2, k3, k4 = key_heights

            h0 = k0 + l0
            h1 = k1 + l1
            h2 = k2 + l2
            h3 = k3 + l3
            h4 = k4 + l4

            if (h0 <= 5) and (h1 <= 5) and (h2 <= 5) and (h3 <= 5) and (h4 <= 5):
                output += 1
            
    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
#part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
