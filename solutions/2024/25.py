from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input25.txt"

def part1(in_file):
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

    # Count lock/key pairs
    part1 = 0
    for lock_heights in lock_list:
        l0, l1, l2, l3, l4 = lock_heights
        for key_heights in key_list:
            k0, k1, k2, k3, k4 = key_heights

            # Progressively check whether total heights exceed 5
            #   to save operations, and if none of them are,
            #   it is a valid lock/key pair
            if ((k0 + l0) > 5):
                continue
            if ((k1 + l1) > 5):
                continue
            if ((k2 + l2) > 5):
                continue
            if ((k3 + l3) > 5):
                continue
            if ((k4 + l4) > 5):
                continue

            part1 += 1
            
    return part1

part1 = part1(input_file)

print("")
print("--- Advent of Code 2024 Day 25: Code Chronicle ---")
print(f'Part 1: {part1}')
print(f'Part 2: ⭐')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
