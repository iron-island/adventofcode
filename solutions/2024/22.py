import numpy as np
from collections import defaultdict
from collections import deque
from functools import cache
import math

input_file = "input22.txt"
example_file = "example22.txt"
example2_file = "example22_2.txt"
example3_file = "example22_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

def move_dir(rc, direction):
    row, col = rc

    assert(direction in ["up", "down", "left", "right"])
    if (direction == "up"):
        n_row = row-1
        n_col = col
    elif (direction == "down"):
        n_row = row+1
        n_col = col
    elif (direction == "left"):
        n_row = row
        n_col = col-1
    elif (direction == "right"):
        n_row = row
        n_col = col+1

    return (n_row, n_col)

def mix(secret_num, val):
    new_secret = secret_num ^ val
    return new_secret

def prune(secret_num):
    new_secret = secret_num % 16777216
    return new_secret

def evolve(secret_num):
    val = secret_num*64
    new_secret = mix(secret_num, val)
    new_secret = prune(new_secret)

    val = int(new_secret/32)
    new_secret = mix(new_secret, val)
    new_secret = prune(new_secret)
    
    val = new_secret*2048
    new_secret = mix(new_secret, val)
    new_secret = prune(new_secret)

    return new_secret

def process_inputs(in_file, t):
    output = 0

    init_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            init_list.append(int(line))

            line = file.readline()

    last_secret_list = []
    for secret_num in init_list:
        new_secret = secret_num
        for i in range(0, t):
            new_secret = evolve(new_secret)

        # Record
        last_secret_list.append(new_secret)

    # Evaluate
    for s in last_secret_list:
        output += s

    return output

def process_inputs2(in_file, t):
    output = 0

    init_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            init_list.append(int(line))

            line = file.readline()

    last_secret_list = []
    changes_array = []
    digit_array = []
    banana_dict = defaultdict(int)
    for idx_s, secret_num in enumerate(init_list):
        new_secret = secret_num
        digit_list = []
        changes_list = []
        changes_set = set()
        for i in range(0, t):
            new_secret = evolve(new_secret)

            # Record
            digit_list.append(new_secret % 10)

        # Get changes
        for idx, d in enumerate(digit_list):
            if (idx == 0):
                change = math.inf
            else:
                change = d - (digit_list[idx-1])

            changes_list.append(change)

            if (idx >= 4):
                seq = tuple(changes_list[(idx-3):(idx+1)])
                if (seq not in changes_set):
                    banana_dict[seq] += d
                    changes_set.add(seq)

        # Record
        #digit_array.append(digit_list)
        #changes_array.append(changes_list)

    # Evaluate
    max_banana = 0
    for seq in banana_dict:
        max_banana = max(max_banana, banana_dict[seq])
    output = max_banana

    # Sliding window
    #max_bananas = 0
    ## Iterate through possible change sequences
    #for change_seq in changes_set:
    #    # Iterate through digit_list and changes_list
    #    for idx_array, digit_list in enumerate(digit_array):

    return output

#part1_example = process_inputs(example_file,10)
#part1_example2 = process_inputs(example2_file,2000)
#part1 = process_inputs(input_file, 2000)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
part2_example3 = process_inputs2(example3_file, 2000)
part2 = process_inputs2(input_file, 2000)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
