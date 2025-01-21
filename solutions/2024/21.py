from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict
from functools import cache
from math import inf

input_file = "../../inputs/2024/input21.txt"

key_dict = {
    (0, 0): '7',
    (0, 1): '8',
    (0, 2): '9',
    (1, 0): '4',
    (1, 1): '5',
    (1, 2): '6',
    (2, 0): '1',
    (2, 1): '2',
    (2, 2): '3',
    (3, 1): '0',
    (3, 2): 'A'
}

dir_dict = {
    (0, 1): '^',
    (0, 2): 'A',
    (1, 0): '<',
    (1, 1): 'v',
    (1, 2): '>'
}

rev_dir_dict = defaultdict(tuple)

def get_dist(tuple1, tuple2):
    row1, col1 = tuple1
    row2, col2 = tuple2

    diff_row = abs(row2-row1)
    diff_col = abs(col2-col1)

    return diff_row+diff_col

def get_dist_diff(tuple1, tuple2):
    row1, col1 = tuple1
    row2, col2 = tuple2

    diff_row = row2-row1
    diff_col = col2-col1

    return diff_row, diff_col

# Works
# Call stack is:
# dfs_key
#   dfs_dir1_seq
#     dfs_dir1
#       dfs_dir2_seq
#         dfs_dir2
@cache
def dfs_key(startkey_rc, endkey_rc, num_robots):
    startkey = key_dict[startkey_rc]
    endkey   = key_dict[endkey_rc]

    diff_row, diff_col = get_dist_diff(startkey_rc, endkey_rc)

    moves_list = []
    if (diff_col > 0):
        moves_list.append((">", diff_col))
    elif (diff_col < 0):
        moves_list.append(("<", abs(diff_col)))

    if (diff_row > 0):
        moves_list.append(("v", diff_row))
    elif (diff_row < 0):
        moves_list.append(("^", abs(diff_row)))

    # A button
    A_tuple = ('A', 1)
    INIT_COST = inf
    if (len(moves_list) == 1):
        moves_list.append(A_tuple)

        seq = ""
        for move_tuple in moves_list:
            dir1, num1 = move_tuple
            seq = seq + num1*dir1

        # DFS on seq
        cost = dfs_dir1_seq(seq, num_robots-1)
    else:
        rev_moves_list = []
        rev_moves_list.append(moves_list[1])
        rev_moves_list.append(moves_list[0])

        moves_list.append(A_tuple)
        rev_moves_list.append(A_tuple)

        cost = INIT_COST
        for cand_moves_list in [moves_list, rev_moves_list]:
            move1, move2, moveA = cand_moves_list
            dir1, num1 = move1

            # Prune invalid moves
            if (startkey in ['7', '4', '1']) and (endkey in ['0', 'A']) and (dir1 == 'v'):
                continue
            if (endkey in ['7', '4', '1']) and (startkey in ['0', 'A']) and (dir1 == '<'):
                continue

            # Reconstruct sequence
            seq = ""
            for move_tuple in cand_moves_list:
                dir1, num1 = move_tuple
                seq = seq + num1*dir1

            # DFS on seq
            cost = min(cost, dfs_dir1_seq(seq, num_robots-1))

    return cost

@cache
def dfs_dir1_seq(seq, num_robots):
    cost = 0
    for idx, dir1 in enumerate(seq):
        if (idx == 0):
            startdir1 = 'A'
        else:
            startdir1 = seq[idx-1]
        enddir1 = dir1

        cost += dfs_dir1(startdir1, enddir1, num_robots)

    return cost

@cache
def dfs_dir1(startdir1, enddir1, num_robots):
    startdir1_rc = rev_dir_dict[startdir1]
    enddir1_rc   = rev_dir_dict[enddir1]

    diff_row, diff_col = get_dist_diff(startdir1_rc, enddir1_rc)

    moves_list = []
    if (diff_col > 0):
        moves_list.append((">", diff_col))
    elif (diff_col < 0):
        moves_list.append(("<", abs(diff_col)))

    if (diff_row > 0):
        moves_list.append(("v", diff_row))
    elif (diff_row < 0):
        moves_list.append(("^", abs(diff_row)))

    # A button
    A_tuple = ('A', 1)
    INIT_COST = inf
    if (len(moves_list) <= 1):
        moves_list.append(A_tuple)

        # Reconstruct sequence
        seq = ""
        for move_tuple in moves_list:
            dir1, num1 = move_tuple
            seq = seq + num1*dir1

        # DFS on seq
        cost = dfs_dir2_seq(seq, num_robots-1)
    else:
        rev_moves_list = []
        rev_moves_list.append(moves_list[1])
        rev_moves_list.append(moves_list[0])

        moves_list.append(A_tuple)
        rev_moves_list.append(A_tuple)

        cost = INIT_COST
        for cand_moves_list in [moves_list, rev_moves_list]:
            move1, move2, moveA = cand_moves_list
            dir1, num1 = move1

            # Prune invalid moves
            if (startdir1 == '<') and (dir1 == '^'):
                continue
            if (enddir1 == '<') and (startdir1 in ['^', 'A']) and (dir1 == '<'):
                continue

            # Reconstruct sequence
            seq = ""
            for move_tuple in cand_moves_list:
                dir1, num1 = move_tuple
                seq = seq + num1*dir1

            # DFS on seq
            cost = min(cost, dfs_dir2_seq(seq, num_robots-1))

    return cost

@cache
def dfs_dir2_seq(seq, num_robots):
    cost = 0
    for idx, dir2 in enumerate(seq):
        if (idx == 0):
            startdir2 = 'A'
        else:
            startdir2 = seq[idx-1]
        enddir2 = dir2

        cost += dfs_dir2(startdir2, enddir2, num_robots)

    return cost

@cache
def dfs_dir2(startdir2, enddir2, num_robots):
    # Base case
    if (startdir2 == enddir2):
        return 1

    startdir2_rc = rev_dir_dict[startdir2]
    enddir2_rc   = rev_dir_dict[enddir2]

    diff_row, diff_col = get_dist_diff(startdir2_rc, enddir2_rc)

    moves_list = []
    if (diff_col > 0):
        moves_list.append((">", diff_col))
    elif (diff_col < 0):
        moves_list.append(("<", abs(diff_col)))

    if (diff_row > 0):
        moves_list.append(("v", diff_row))
    elif (diff_row < 0):
        moves_list.append(("^", abs(diff_row)))

    # A button
    A_tuple = ('A', 1)
    INIT_COST = inf
    if (len(moves_list) == 1):
        moves_list.append(A_tuple)

        if (num_robots == 0):
            # Compute cost
            curr_cost = 0
            for move_tuple in moves_list:
                dir1, num1 = move_tuple
                curr_cost += num1
            cost = curr_cost
        else:
            # Reconstruct sequence
            seq = ""
            for move_tuple in moves_list:
                dir1, num1 = move_tuple
                seq = seq + num1*dir1

            # DFS on seq
            cost = dfs_dir2_seq(seq, num_robots-1)
    else:
        rev_moves_list = []
        rev_moves_list.append(moves_list[1])
        rev_moves_list.append(moves_list[0])

        moves_list.append(A_tuple)
        rev_moves_list.append(A_tuple)

        cost = INIT_COST
        for cand_moves_list in [moves_list, rev_moves_list]:
            move1, move2, moveA = cand_moves_list
            dir1, num1 = move1

            # Prune invalid moves
            if (startdir2 == '<') and (dir1 == '^'):
                continue
            if (enddir2 == '<') and (startdir2 in ['^', 'A']) and (dir1 == '<'):
                continue

            if (num_robots == 0):
                # Compute cost
                curr_cost = 0
                for move_tuple in cand_moves_list:
                    dir1, num1 = move_tuple
                    curr_cost += num1

                cost = min(cost, curr_cost)
            else:
                # Reconstruct sequence
                seq = ""
                for move_tuple in cand_moves_list:
                    dir1, num1 = move_tuple
                    seq = seq + num1*dir1

                # DFS on seq
                cost = min(cost, dfs_dir2_seq(seq, num_robots-1))

    return cost

def part1_part2(in_file):
    codes_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            codes_list.append(line)

            line = file.readline()

    # Get reversed key_dict and dir_dict
    rev_key_dict = defaultdict(tuple)
    for rc in key_dict:
        key_rc = key_dict[rc]
        rev_key_dict[key_rc] = rc

    #rev_dir_dict = defaultdict(tuple)
    global rev_dir_dict
    for rc in dir_dict:
        dir_rc = dir_dict[rc]
        rev_dir_dict[dir_rc] = rc

    # Part 1 and Part 2 uses the same DFS algorithm,
    #   just with different number of robots which represent the depth
    # Iterate through codes
    part1_cost_dict = defaultdict(int)
    part2_cost_dict = defaultdict(int)
    for code in codes_list:
        # Iterate through keys in code
        part1_cost = 0
        part2_cost = 0
        for idx, endkey in enumerate(code):
            if (idx == 0):
                startkey = 'A'
            else:
                startkey = code[idx-1]

            startkey_rc = rev_key_dict[startkey]
            endkey_rc   = rev_key_dict[endkey]

            # DFS on key chunk for Part 1 with 2 robots
            part1_cost += dfs_key(startkey_rc, endkey_rc, 2)

            # DFS on key chunk for Part 2 with 25 robots
            part2_cost += dfs_key(startkey_rc, endkey_rc, 25)

        part1_cost_dict[code] = part1_cost
        part2_cost_dict[code] = part2_cost

    # Evaluate Part 1
    part1 = 0
    for code in part1_cost_dict:
        cost = part1_cost_dict[code]
        num  = int(code[:-1])

        complexity = cost*num
        part1 += complexity

    # Evaluate Part 2
    part2 = 0
    for code in part2_cost_dict:
        cost = part2_cost_dict[code]
        num  = int(code[:-1])

        complexity = cost*num
        part2 += complexity

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 21: Keypad Conundrum ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
