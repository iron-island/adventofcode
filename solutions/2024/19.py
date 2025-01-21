from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from functools import cache

input_file = "../../inputs/2024/input19.txt"

towels_list = []

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
            
def part1_part2(in_file):
    global towels_list

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
    part1 = 0
    part2 = 0
    for design in designs_list:
        valid = check_design2(design)
        if valid:
            part2 += valid
            part1 += 1

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 19: Linen Layout ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
