import copy
from collections import defaultdict

input_file = "../../inputs/2021/input25.txt"
example_file = "example25.txt"

part1_example = 0
part1 = 0

def print_grid(grid_dict, MAX_ROW, MAX_COL):
    for row in range(0, MAX_ROW+1):
        for col in range(0, MAX_COL+1):
            print(grid_dict[(row, col)], end="")
        print("")

def process_inputs(in_file):
    output = 0

    #grid_dict = defaultdict(str)
    eastward_set = set()
    southward_set = set()
    MAX_ROW = 0
    MAX_COL = 0
    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            line = line.strip()

            col = 0
            for tile in line:
                #grid_dict[(row, col)] = tile
                if (tile == ">"):
                    eastward_set.add((row, col))
                elif (tile == "v"):
                    southward_set.add((row, col))
                col += 1
            MAX_COL = col-1

            row += 1

            line = file.readline()
        MAX_ROW = row-1

    # Debugging
    #print("Initial state")
    #print_grid(grid_dict, MAX_ROW, MAX_COL)
    #print("")

    steps = 0
    while True:
        no_change = True
        steps += 1
        print(f'Step {steps}')

        #if (steps == 5):
        #    break

        # ORIGINAL DICTIONARY-BASED APPROACH
        # Move east-facing first, starting from MAX_COL
        #new_grid_dict = copy.deepcopy(grid_dict)
        #for col in range(MAX_COL, -1, -1):
        #    for row in range(0, MAX_ROW+1):
        #        if (grid_dict[(row, col)] != ">"):
        #            continue

        #        if (col < MAX_COL):
        #            n_rc = (row, col+1)
        #        else:
        #            n_rc = (row, 0)

        #        if (grid_dict[n_rc] == "."):
        #            new_grid_dict[(row, col)] = "."
        #            new_grid_dict[n_rc] = ">"
        #            no_change = False

        # Move south-facing second, starting from 0
        #grid_dict = copy.deepcopy(new_grid_dict)
        #for row in range(0, MAX_ROW+1):
        #    for col in range(0, MAX_COL+1):
        #        if (new_grid_dict[(row, col)] != "v"):
        #            continue

        #        if (row < MAX_ROW):
        #            n_rc = (row+1, col)
        #        else:
        #            n_rc = (0, col)

        #        if (new_grid_dict[n_rc] == "."):
        #            grid_dict[(row, col)] = "."
        #            grid_dict[n_rc] = "v"
        #            no_change = False

        # OPTIMIZED SET-BASED APPROACH
        # Move east-facing first
        new_eastward_set = set()
        for rc in eastward_set:
            row, col = rc
            if (col < MAX_COL):
                n_rc = (row, col+1)
            else:
                n_rc = (row, 0)

            if (n_rc not in eastward_set) and (n_rc not in southward_set):
                new_eastward_set.add(n_rc)
                no_change = False
            else:
                new_eastward_set.add(rc)

        # Move south-facing second
        new_southward_set = set()
        for rc in southward_set:
            row, col = rc
            if (row < MAX_ROW):
                n_rc = (row+1, col)
            else:
                n_rc = (0, col)

            if (n_rc not in new_eastward_set) and (n_rc not in southward_set):
                new_southward_set.add(n_rc)
                no_change = False
            else:
                new_southward_set.add(rc)
        eastward_set = new_eastward_set
        southward_set = new_southward_set

        # Check if there is no change
        if (no_change):
            break

        # DEBUGGING
        #print_grid(grid_dict, MAX_ROW, MAX_COL)
        #print("")

    output = steps

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
