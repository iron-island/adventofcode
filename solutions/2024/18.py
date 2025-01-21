from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import deque

input_file = "../../inputs/2024/input18.txt"

MAX_ROW = 70
MAX_COL = 70

def bfs_path(coords_set):
    q = deque()
    q.append(((0, 0), 0))
    visited = set()
    
    steps = 0
    exit_found = False
    while (len(q)):
        rc, steps = q.popleft()

        if (MAX_ROW, MAX_COL) == rc:
            visited.add(rc)
            exit_found = True
            break

        if (rc in visited):
            continue
        visited.add(rc)
        row, col = rc

        # up
        if (row > 0):
            n_rc = (row-1, col)
            if (n_rc not in coords_set):
                q.append((n_rc, steps+1))

        # down
        if (row < MAX_ROW):
            n_rc = (row+1, col)
            if (n_rc not in coords_set):
                q.append((n_rc, steps+1))

        # left
        if (col > 0):
            n_rc = (row, col-1)
            if (n_rc not in coords_set):
                q.append((n_rc, steps+1))

        # right
        if (col < MAX_COL):
            n_rc = (row, col+1)
            if (n_rc not in coords_set):
                q.append((n_rc, steps+1))

    return steps, exit_found

def part1_part2(in_file):
    output = 0

    coords_list = []
    length = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            coords = [int(x) for x in line.split(",")]
            x, y = coords
            coords_list.append((y, x))
            length += 1

            line = file.readline()

    # Binary search, lower bound is 1024 to solve Part 1
    idx_low = 1023
    idx_up  = len(coords_list)-1
    idx_mid = int((idx_up - idx_low)/2) + idx_low
    while ((idx_up - idx_low) > 2):
        steps_low, exit_found_low = bfs_path(set(coords_list[:idx_low+1]))
        steps_up,  exit_found_up  = bfs_path(set(coords_list[:idx_up+1]))
        steps_mid, exit_found_mid = bfs_path(set(coords_list[:idx_mid+1]))

        # Part 1
        if (idx_low == 1023):
            part1 = steps_low

        # Update bounds
        if (exit_found_mid):
            idx_low = idx_mid
        else:
            idx_up = idx_mid
        idx_mid = int((idx_up - idx_low)/2) + idx_low

    part2 = f'{coords_list[idx_mid][1]},{coords_list[idx_mid][0]}'

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 18: RAM Run ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
