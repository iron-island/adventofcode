from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input20.txt"

def part1_part2(in_file):
    grid = []
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            grid.append(line)

            # Check start and end coordinates
            if ("S" in line):
                start_rc = (row, line.index("S"))
            elif ("E" in line):
                end_rc = (row, line.index("E"))

            row += 1
            line = file.readline()

    MAX_ROW = len(grid)-1
    MAX_COL = len(grid[0])-1

    # Traverse the path
    # Heuristic: There is only 1 path so BFS is enough
    #            and there's no need to use a set of
    #            visited coordinates
    rc = start_rc
    prev_rc = None

    best_path = []
    idx = 0
    idx_dict = defaultdict(int)
    while True:
        best_path.append(rc)
        idx_dict[rc] = idx
        idx += 1

        # If we arrived at the end, add as a turn
        if (rc == end_rc):
            break

        # Check which direction is the next coordinate
        row, col = rc

        # Up
        n_row = row-1
        next_rc = (n_row, col)
        if (grid[n_row][col] != "#") and (next_rc != prev_rc):
            prev_rc = rc
            rc = next_rc
            continue
        
        # Down
        n_row = row+1
        next_rc = (n_row, col)
        if (grid[n_row][col] != "#") and (next_rc != prev_rc):
            prev_rc = rc
            rc = next_rc
            continue

        # Left
        n_col = col-1
        next_rc = (row, n_col)
        if (grid[row][n_col] != "#") and (next_rc != prev_rc):
            prev_rc = rc
            rc = next_rc
            continue

        # Right
        n_col = col+1
        next_rc = (row, n_col)
        if (grid[row][n_col] != "#") and (next_rc != prev_rc):
            prev_rc = rc
            rc = next_rc
            continue

    # Precompute the row offset, column offset, and distance
    offset_list = [(r, c, abs(r)+abs(c)) for r in range(-20, 21) for c in range(abs(r)-20, (20-abs(r))+1)]

    # Loop through best_path to connect cheat0 and cheat2, excluding E for cheat0
    part1 = 0
    part2 = 0
    for idx, cheat0 in enumerate(best_path[:-1]):
        start_row, start_col = cheat0
        for offset in offset_list:
            row_offset, col_offset, dist = offset

            cheat2 = (start_row+row_offset, start_col+col_offset)
            if (idx_dict[cheat2] > idx):
                saved = idx_dict[cheat2] - idx - dist

                if (saved >= 100):
                    # Part 1 is a subset of Part 2 when cheat lasts at most 2 picoseconds
                    if (dist <= 2):
                        part1 += 1

                    part2 += 1

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 20: Race Condition ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
