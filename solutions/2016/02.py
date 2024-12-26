import numpy as np
from collections import defaultdict
from collections import deque
from functools import cache

input_file = "input2.txt"
example_file = "example02.txt"
example2_file = "example02.txt"
example3_file = "example02.txt"

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

    inst_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            inst_list.append(line)

            line = file.readline()

    # Follow instructions
    row = 1
    col = 1
    keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    code = ""
    for inst in inst_list:
        for i in inst:

            if (i == "U"):
                row = row-1
            elif (i == "L"):
                col = col-1
            elif (i == "D"):
                row = row+1
            elif (i == "R"):
                col = col+1

            # Clip
            row = min(2, row)
            row = max(0, row)
            col = min(2, col)
            col = max(0, col)

        code = code + str(keypad[row][col])

    output = code

    return output

def process_inputs2(in_file):
    output = 0

    inst_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            inst_list.append(line)

            line = file.readline()

    # Follow instructions
    row = 2
    col = 0
    keypad = [
        [0, 0, 1, 0, 0],
        [0, 2, 3, 4, 0],
        [5, 6, 7, 8, 9],
        [0, 'A', 'B', 'C', 0],
        [0, 0, 'D', 0, 0]
    ]
    code = ""
    for inst in inst_list:
        for i in inst:

            if (i == "U"):
                n_row = row-1
                n_col = col
            elif (i == "L"):
                n_col = col-1
                n_row = row
            elif (i == "D"):
                n_row = row+1
                n_col = col
            elif (i == "R"):
                n_col = col+1
                n_row = row

            # Clip
            n_row = min(4, n_row)
            n_row = max(0, n_row)
            n_col = min(4, n_col)
            n_col = max(0, n_col)

            # Check
            if (keypad[n_row][n_col] != 0):
                row, col = n_row, n_col

        code = code + str(keypad[row][col])

    output = code

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2_example2 = process_inputs2(example2_file)
part2_example3 = process_inputs2(example3_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
