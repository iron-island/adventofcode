import numpy as np
from collections import defaultdict
from collections import deque
from functools import cache

input_file = "../../inputs/2024/input14.txt"
example_file = "example14.txt"
example2_file = "example14_2.txt"
example3_file = "example14_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0
def process_inputs(in_file, MAX_ROW, MAX_COL):
    output = 0

    grid = []
    robots_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            p_str, v_str = line.split()

            x, y = p_str[2:].split(",")
            x = int(x)
            y = int(y)

            vx, vy = v_str[2:].split(",")
            vx = int(vx)
            vy = int(vy)

            robots_list.append([(x, y), (vx, vy)])

            line = file.readline()

    # Simulate
    NUM = 100
    final_pos_list = []
    for idx, robot in enumerate(robots_list):
        x, y = robot[0]
        vx, vy = robot[1]

        x = x + NUM*vx
        y = y + NUM*vy

        n_x = x % (MAX_COL+1)
        n_y = y % (MAX_ROW+1)

        final_pos_list.append((n_x, n_y))

        if (idx == 10):
            print(n_x, n_y)

    # Check quadrants
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    X_MID = MAX_COL/2
    Y_MID = MAX_ROW/2
    for pos in final_pos_list:
        x, y = pos
        #if (x != (MAX_COL)/2) and (y != (MAX_ROW)/2):
        #    output += 1

        if (x < X_MID) and (y < Y_MID):
            q1 += 1
        elif (x > X_MID) and (y < Y_MID):
            q2 += 1
        elif (x < X_MID) and (y > Y_MID):
            q3 += 1
        elif (x > X_MID) and (y > Y_MID):
            q4 += 1

    print(final_pos_list)
    print(q1, q2, q3, q4)
    output = q1*q2*q3*q4

    return output

def process_inputs2(in_file, MAX_ROW, MAX_COL):
    output = 0

    grid = []
    robots_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            p_str, v_str = line.split()

            x, y = p_str[2:].split(",")
            x = int(x)
            y = int(y)

            vx, vy = v_str[2:].split(",")
            vx = int(vx)
            vy = int(vy)

            robots_list.append([(x, y), (vx, vy)])

            line = file.readline()

    # Simulate
    NUM = 0
    final_pos_list = []
    while (True):
        NUM += 1
        final_pos_list = []
        invalid = False
        for idx, robot in enumerate(robots_list):
            x, y = robot[0]
            vx, vy = robot[1]

            x = x + NUM*vx
            y = y + NUM*vy

            n_x = x % (MAX_COL+1)
            n_y = y % (MAX_ROW+1)

            if ((n_x, n_y) in final_pos_list):
                invalid = True
                break

            final_pos_list.append((n_x, n_y))

        print(NUM)
        if (not invalid):
            output = NUM
            return output

    # Check quadrants
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    X_MID = MAX_COL/2
    Y_MID = MAX_ROW/2
    for pos in final_pos_list:
        x, y = pos
        #if (x != (MAX_COL)/2) and (y != (MAX_ROW)/2):
        #    output += 1

        if (x < X_MID) and (y < Y_MID):
            q1 += 1
        elif (x > X_MID) and (y < Y_MID):
            q2 += 1
        elif (x < X_MID) and (y > Y_MID):
            q3 += 1
        elif (x > X_MID) and (y > Y_MID):
            q4 += 1

    print(final_pos_list)
    print(q1, q2, q3, q4)
    output = q1*q2*q3*q4

    return output

#part1_example = process_inputs(example_file, 6, 10)
#part1 = process_inputs(input_file, 102, 100)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)

part2_example = process_inputs2(example_file, 6, 10)
part2 = process_inputs2(input_file, 102, 100)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
