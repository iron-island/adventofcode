from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input11.txt"

def part1_part2(in_file):
    output = 0

    #s_list = []
    new_dict = defaultdict(int)
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line = line.split()
            #s_list = [int(x) for x in line]
            for s in line:
                new_dict[int(s)] += 1

            line = file.readline()

    # Blink
    BLINKS = 75
    part1 = 0
    for b in range(1, BLINKS+1):
        # Update
        s_dict = new_dict.copy()
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

                    new_dict[s] -= num
                    if (new_s in new_dict):
                        new_dict[new_s] += num
                    else:
                        new_dict[new_s] = num
        # Part 1: Compute when blinks are 25
        if (b == 25):
            part1 = sum(new_dict.values())

    part2 = sum(new_dict.values())
    
    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 11: Plutonian Pebbles ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
