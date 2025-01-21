from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

import heapq
from collections import defaultdict, deque

input_file = "../../inputs/2024/input16.txt"

def part1_part2(in_file):
    grid_dict = defaultdict(str)
    cost_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
        row = 0
        INIT_COST = 1000000000000
        while line:
            line = line.strip()
            MAX_COL = len(line)-1
            for col, tile in enumerate(line):
                grid_dict[(row, col)] = tile
                for direction in ["up", "down", "left", "right"]:
                    cost_dict[(row, col, direction)] = [INIT_COST, []]

                if (tile == 'S'):
                    S_pos = (row, col)
                    S_dir = "right"
                elif (tile == 'E'):
                    E_pos = (row, col)
            row += 1
            
            line = file.readline()

        MAX_ROW = row-1

    # Dijkstra's
    h = []
    visited = set()
    E_visited_dict = {"up": False, "right": False}
    n_tuple = (0, S_pos[0], S_pos[1], "right")
    heapq.heappush(h, n_tuple)
    while (len(h)):
        # Priority queue
        cost, row, col, direction = heapq.heappop(h)

        # TODO: check if this is always applicable? what if new path with lesser cost was found?
        if ((row, col, direction) in visited):
            continue

        visited.add((row, col, direction))

        # up
        n_row = row-1
        n_col = col
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "up"):
                n_cost = cost
            elif (direction == "right") or (direction == "left"):
                n_cost = cost + 1000
            elif (direction == "down"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "up"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            if (n_cost < n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

        # down
        n_row = row+1
        n_col = col
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "down"):
                n_cost = cost
            elif (direction == "right") or (direction == "left"):
                n_cost = cost + 1000
            elif (direction == "up"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "down"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            if (n_cost < n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

        # left
        n_row = row
        n_col = col-1
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "left"):
                n_cost = cost
            elif (direction == "up") or (direction == "down"):
                n_cost = cost + 1000
            elif (direction == "right"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "left"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            if (n_cost < n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

        # right
        n_row = row
        n_col = col+1
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "right"):
                n_cost = cost
            elif (direction == "up") or (direction == "down"):
                n_cost = cost + 1000
            elif (direction == "left"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "right"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            #assert(prev_tile_list != None)
            if (n_cost < n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                heapq.heappush(h, (n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

    # Evaluate Part 1
    part1 = INIT_COST
    for cost_tuple in cost_dict:
        row, col, direction = cost_tuple

        tile = grid_dict[(row, col)]

        if (tile == 'E'):
            cost, pos_list = cost_dict[cost_tuple]
            part1 = min(part1, cost)

            if (part1 == cost):
                E_tuple = cost_tuple
                last_tile_list = pos_list

    # Part 2
    row, col, direction = E_tuple
    part1_set = set()
    part1_set.add((row, col))
    q = deque()
    q.append((row, col, direction))
    while (True):
        row, col, direction = q.popleft()
        part1_set.add((row, col))
        if (grid_dict[(row, col)] == 'S'):
            break

        cost, last_tile_list = cost_dict[(row, col, direction)]
        for last_tile in last_tile_list:
            last_row, last_col, last_dir = last_tile
            q.append((last_row, last_col, last_dir))
    part2 = len(part1_set)

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 16: Reindeer Maze ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
