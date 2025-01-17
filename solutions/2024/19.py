from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from functools import cache

input_file = "../../inputs/2024/input19.txt"
example_file = "example19.txt"
example2_file = "example19_2.txt"
example3_file = "example19_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

towels_list = []

@cache
def check_design(design, towels_tuple):
    #print(design)
    if (design in towels_tuple):
        #print("base case 1")
        return 1

    if (design == ""):
        return 1
    
    if (len(design) == 1) and (design not in towels_tuple):
        #print("base case 0")
        return 0
    valid = 0 
    for towel in towels_tuple:
        if (towel in design):
            #if (design == "bwurrg"):
            
            idx = design.find(towel)
            len_towel = len(towel)

            #if (idx+len_towel < len(design)) and (idx > 0):
            if (idx+len_towel < len(design)):
                remaining_design1 = design[0:idx]
                remaining_design2 = design[idx+len_towel:]
                #print(f'remaining_design1 = {remaining_design1}')
                #print(f'remaining_design2 = {remaining_design2}')
                valid1 = check_design(remaining_design1, towels_tuple)
                valid2 = check_design(remaining_design2, towels_tuple)

                if (valid1 and valid2):
                    return 1
            else:
                #print("else case")
                #if (idx == 0):
                #    remaining_design = design[1:]
                #    return check_design(remaining_design, towels_tuple)
                if (True):
                    remaining_design = design[0:idx]
                    return check_design(remaining_design, towels_tuple)
            
    return 0

#@cache
#def check_design2(design, towels_tuple):
#    #print(design)
#    #if (design in towels_tuple):
#    #    return 1
#
#    if (design == ""):
#        return 1
#    
#    if (len(design) == 1) and (design not in towels_tuple):
#        return 0
#
#    tot_valid = 1
#    for towel in towels_tuple:
#        valid = 0
#        if (towel in design):
#            idx = design.find(towel)
#            len_towel = len(towel)
#
#            if (idx+len_towel < len(design)):
#                remaining_design1 = design[0:idx]
#                remaining_design2 = design[idx+len_towel:]
#                len1 = len(remaining_design1)
#                len2 = len(remaining_design2)
#
#                # TODO: what if string is empty?
#                valid1 = check_design2(remaining_design1, towels_tuple)
#                valid2 = check_design2(remaining_design2, towels_tuple)
#
#                valid = valid1*valid2
#            else:
#                remaining_design = design[0:idx]
#                valid3 = check_design2(remaining_design, towels_tuple)
#
#                valid = valid3
#
#        tot_valid += valid
#            
#    return tot_valid
# Alternative 2
@cache
def check_design2(design):
    valid = 0
    for towel in towels_list:
        len_towel = len(towel)

        if (len_towel > len(design)):
            continue

        if (towel == design):
            valid += 1

        if (towel == design[0:len_towel]):
            valid += check_design2(design[len_towel:])

    return valid
            

def process_inputs(in_file):
    output = 0

    designs_list = []
    towels_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if not (len(towels_list)):
                towels_list = [x for x in line.split(", ")]
            elif (line != ""):
                designs_list.append(line)

            line = file.readline()

    # Iterate
    valid = 0
    towels_tuple = tuple(towels_list)
    for idx, design in enumerate(designs_list):
        #print(f'Checking design {idx} of {len(designs_list)-1}')
        valid = check_design(design, towels_tuple)
        if valid:
            #print(f'{design} is possible')
            output += 1

    return output

def process_inputs2(in_file):
    global towels_list

    output = 0

    designs_list = []
    towels_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if not (len(towels_list)):
                towels_list = [x for x in line.split(", ")]
            elif (line != ""):
                designs_list.append(line)

            line = file.readline()

    # Iterate
    valid = 0
    #towels_tuple = tuple(towels_list)
    #valid_list = []
    part1 = 0
    for design in designs_list:
        #print(f'Checking design {idx} of {len(designs_list)-1}')
        valid = check_design2(design)
        if valid:
            #print(f'{design} is possible')
            #valid_list.append(valid)
            output += valid
            part1 += 1

    #print(valid_list)

    return part1, output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
part1, part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 19: Linen Layout ---")
#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
