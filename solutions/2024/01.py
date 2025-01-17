from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input01.txt"

def part1_part2(in_file):
    left_list = []
    right_list = []

    right_count_dict = defaultdict(int)
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            left_str, right_str = line.split()
            right = int(right_str)

            left_list.append(int(left_str))
            right_list.append(right)

            # Populate dictionary with the occurrences of numbers so far for Part 2
            right_count_dict[right] += 1

            line = file.readline()

    left_list.sort()
    right_list.sort()

    # Parts 1 and 2 in the same loop
    part1 = 0
    part2 = 0
    for idx, left in enumerate(left_list):
        part1 += abs(left - right_list[idx])
        part2 += left*right_count_dict[left]

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 1: Historian Hysteria ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
