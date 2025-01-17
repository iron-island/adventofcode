from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input20.txt"

def get_dist(tuple1, tuple2):
    row1, col1 = tuple1
    row2, col2 = tuple2

    diff_row = abs(row2-row1)
    diff_col = abs(col2-col1)

    return diff_row+diff_col

def part1_part2(in_file):
    grid_dict = defaultdict(str)
    node_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()

        row = 0    
        while line:
            line = line.strip()

            for col, l in enumerate(line):
                grid_dict[(row, col)] = l
                node_dict[(row, col)] = [10000000, None]

                if (l == "S"):
                    S_pos = (row, col)
                elif (l == "E"):
                    E_pos = (row, col)
            MAX_COL = len(line)-1

            row += 1

            line = file.readline()

    MAX_ROW = row-1
    #print(MAX_ROW, MAX_COL)

    # Initial BFS
    q = []
    visited = set()
    #idx_dict = defaultdict(int)
    t = 0
    row, col = S_pos
    dist = get_dist(S_pos, E_pos)
    q.append((t+dist, row, col, t))
    node_dict[S_pos] = [t, None]
    idx = 0
    while (len(q)):
        # Priority queue
        q.sort()
        heuristic, row, col, t = q.pop(0)

        if ((row, col) == E_pos):
            break

        if ((row, col) in visited):
            continue
        visited.add((row, col))

        # up
        n_row = row-1
        n_col = col
        n_tuple = (n_row, n_col)
        dist = get_dist(n_tuple, E_pos)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            prev_t, prev_node = node_dict[n_tuple]
            if (prev_t >= (t+1)):
                q.append((t+1+dist, n_row, n_col, t+1))
                node_dict[n_tuple] = [t+1, (row, col)]

        # down
        n_row = row+1
        n_col = col
        n_tuple = (n_row, n_col)
        dist = get_dist(n_tuple, E_pos)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            prev_t, prev_node = node_dict[n_tuple]
            if (prev_t >= (t+1)):
                q.append((t+1+dist, n_row, n_col, t+1))
                node_dict[n_tuple] = [t+1, (row, col)]

        # left
        n_row = row
        n_col = col-1
        n_tuple = (n_row, n_col)
        dist = get_dist(n_tuple, E_pos)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            prev_t, prev_node = node_dict[n_tuple]
            if (prev_t >= (t+1)):
                q.append((t+1+dist, n_row, n_col, t+1))
                node_dict[n_tuple] = [t+1, (row, col)]

        # right
        n_row = row
        n_col = col+1
        n_tuple = (n_row, n_col)
        dist = get_dist(n_tuple, E_pos)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            prev_t, prev_node = node_dict[n_tuple]
            if (prev_t >= (t+1)):
                q.append((t+1+dist, n_row, n_col, t+1))
                node_dict[n_tuple] = [t+1, (row, col)]

    max_t = t

    # Alternative 3: WORKS
    # Reconstruct best path without cheats
    prev_t, prev_node = node_dict[E_pos]
    best_path = []
    best_path.append(E_pos)
    while (prev_node != None):
        best_path.append(prev_node)

        prev_t, prev_node = node_dict[prev_node]
    best_path.reverse()

    # Convert to dict
    idx_dict = defaultdict(int)
    for idx, rc in enumerate(best_path):
        idx_dict[rc] = idx

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
