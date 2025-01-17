from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict
from functools import cache
from math import inf

input_file = "../../inputs/2024/input21.txt"
example_file = "example21.txt"
example2_file = "example21_2.txt"
example3_file = "example21_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

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

def move_dir(rc, direction):
    row, col = rc

    #assert(direction in ["up", "down", "left", "right"])
    if (direction == "up"):
        n_row = row-1
        n_col = col
    elif (direction == "down"):
        n_row = row+1
        n_col = col
    elif (direction == "left"):
        n_row = row
        n_col = col-1
    elif (direction == "right"):
        n_row = row
        n_col = col+1

    return (n_row, n_col)

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

def run_dijkstra(startkey, endkey, curr_dir, key_dict, rev_key_dict, human_cost_dict):
    q = []
    row, col = rev_key_dict[startkey]
    endkey_rc = rev_key_dict[endkey]
    visited = set()
    cost = 0
    q.append((cost, row, col, curr_dir))

    # Initialize table of costs and last key for recording
    rec_cost_dict = defaultdict(list)
    for rc in key_dict:
        if (rc == (row, col)):
            rec_cost_dict[rc] = [0, None]
        else:
            rec_cost_dict[rc] = [100000000, None]
    while (len(q)):
        # Priority queue
        q.sort()
        cost, row, col, curr_dir = q.pop(0)
        rc = (row, col)

        #if (rc == endkey_rc):
        #    break

        if (rc in visited):
            continue
        visited.add(rc)

        # up
        n_tuple = move_dir(rc, "up")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_dir = '^'
            n_cost = cost + human_cost_dict[(curr_dir, n_dir)]

            # If we will arrive at the end key, need to also take into account
            #   the cost of pressing A
            if (n_tuple == endkey_rc):
                n_cost += human_cost_dict[(n_dir, 'A')]

            rec_cost, prev_node = rec_cost_dict[n_tuple]
            if (cost < rec_cost):
                rec_cost_dict[n_tuple] = [n_cost, rc]
                q.append((n_cost, n_row, n_col, n_dir))

        # down
        n_tuple = move_dir(rc, "down")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_dir = 'v'
            n_cost = cost + human_cost_dict[(curr_dir, n_dir)]

            # If we will arrive at the end key, need to also take into account
            #   the cost of pressing A
            if (n_tuple == endkey_rc):
                n_cost += human_cost_dict[(n_dir, 'A')]

            rec_cost, prev_node = rec_cost_dict[n_tuple]
            if (cost < rec_cost):
                rec_cost_dict[n_tuple] = [n_cost, rc]
                q.append((n_cost, n_row, n_col, n_dir))

        # left
        n_tuple = move_dir(rc, "left")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_dir = '<'
            n_cost = cost + human_cost_dict[(curr_dir, n_dir)]

            # If we will arrive at the end key, need to also take into account
            #   the cost of pressing A
            if (n_tuple == endkey_rc):
                n_cost += human_cost_dict[(n_dir, 'A')]

            rec_cost, prev_node = rec_cost_dict[n_tuple]
            if (cost < rec_cost):
                rec_cost_dict[n_tuple] = [n_cost, rc]
                q.append((n_cost, n_row, n_col, n_dir))

        # right
        n_tuple = move_dir(rc, "right")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_dir = '>'
            n_cost = cost + human_cost_dict[(curr_dir, n_dir)]

            # If we will arrive at the end key, need to also take into account
            #   the cost of pressing A
            if (n_tuple == endkey_rc):
                n_cost += human_cost_dict[(n_dir, 'A')]

            rec_cost, prev_node = rec_cost_dict[n_tuple]
            if (cost < rec_cost):
                rec_cost_dict[n_tuple] = [n_cost, rc]
                q.append((n_cost, n_row, n_col, n_dir))

    # Also return curr_dir for next keys
    rec_cost, prev_node = rec_cost_dict[endkey_rc]
    return rec_cost, curr_dir

# Verified working with example
def get_tot_human_cost(robot_seq, human_cost_dict):
    tot_cost = 0
    for idx, enddir in enumerate(robot_seq):
        if (idx == 0):
            startdir = 'A'
        else:
            startdir = robot_seq[idx-1]

        tot_cost += human_cost_dict[(startdir, enddir)]

    return tot_cost

# Works but inefficient and brute force
def get_key_to_robot_dir(startkey, endkey, key_dict, rev_key_dict):
    global seq_list

    # Dijkstra
    q = []
    visited = set()
    cost = 0
    row, col = rev_key_dict[startkey]
    startkey_rc = row, col
    q.append((cost, row, col))

    prev_node_dict = defaultdict(list)
    for rc in key_dict:
        if (rc == startkey_rc):
            prev_node_dict[rc] = [0, set()]
        else:
            prev_node_dict[rc] = [100000, set()]

    while len(q):
        # Priority queue
        q.sort()
        cost, row, col = q.pop(0)
        rc = (row, col)

        # up
        n_tuple = move_dir(rc, "up")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_cost = cost+1
            prev_cost, prev_node_set = prev_node_dict[n_tuple]

            if (n_cost <= prev_cost):
                prev_node_set.add(rc)
                prev_node_dict[n_tuple] = [n_cost, prev_node_set]
                q.append((n_cost, n_row, n_col))

        # down
        n_tuple = move_dir(rc, "down")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_cost = cost+1
            prev_cost, prev_node_set = prev_node_dict[n_tuple]

            if (n_cost <= prev_cost):
                prev_node_set.add(rc)
                prev_node_dict[n_tuple] = [n_cost, prev_node_set]
                q.append((n_cost, n_row, n_col))

        # left
        n_tuple = move_dir(rc, "left")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_cost = cost+1
            prev_cost, prev_node_set = prev_node_dict[n_tuple]

            if (n_cost <= prev_cost):
                prev_node_set.add(rc)
                prev_node_dict[n_tuple] = [n_cost, prev_node_set]
                q.append((n_cost, n_row, n_col))

        # right
        n_tuple = move_dir(rc, "right")
        n_row, n_col = n_tuple
        if (n_tuple in key_dict):
            n_cost = cost+1
            prev_cost, prev_node_set = prev_node_dict[n_tuple]

            if (n_cost <= prev_cost):
                prev_node_set.add(rc)
                prev_node_dict[n_tuple] = [n_cost, prev_node_set]
                q.append((n_cost, n_row, n_col))

    # Reconstruct path
    endkey_rc = rev_key_dict[endkey]
    cost, _ = prev_node_dict[endkey_rc]
    #print(cost)
    curr_rc_set = set()
    curr_rc_set.add(endkey_rc)
    seq = ""
    reconstruct_path(prev_node_dict, curr_rc_set, key_dict, seq)
    actual_seq_list = []

    for seq in seq_list:
        actual_seq = ""
        for idx, s in enumerate(seq[:-1]):
            row1, col1 = rev_key_dict[s]
            row2, col2 = rev_key_dict[seq[idx+1]]

            if (row1-1) == row2:
                actual_seq += '^'
            elif (row1+1) == row2:
                actual_seq += 'v'
            elif (col1-1) == col2:
                actual_seq += '<'
            elif (col1+1) == col2:
                actual_seq += '>'
        actual_seq_list.append(actual_seq + 'A')

    return actual_seq_list

def get_key_to_dir1(startkey, endkey, rev_key_dict, horizontal_priority=False):
    diff_row, diff_col = get_dist_diff(rev_key_dict[startkey], rev_key_dict[endkey])

    dir1_dict = defaultdict(int)
    #horizontal_priority = False
    if (startkey in ['7', '4', '1']) and (endkey in ['0', 'A']):
        horizontal_priority = True
    if (startkey == '<'):
        horizontal_priority = True
    if (endkey in ['<']):
        horizontal_priority = False

    # Hardcoded case for 379A example
    #if ((startkey, endkey) in [('3', '7'), ('A', 'v'), ('v', 'A')]):
    #    horizontal_priority = True

    if (horizontal_priority):
        if (diff_col > 0):
            dir1_dict[">"] = diff_col
        elif (diff_col < 0):
            dir1_dict["<"] = abs(diff_col)

        if (diff_row > 0):
            dir1_dict["v"] = diff_row
        elif (diff_row < 0):
            dir1_dict["^"] = abs(diff_row)

    else:
        if (diff_row > 0):
            dir1_dict["v"] = diff_row
        elif (diff_row < 0):
            dir1_dict["^"] = abs(diff_row)

        if (diff_col > 0):
            dir1_dict[">"] = diff_col
        elif (diff_col < 0):
            dir1_dict["<"] = abs(diff_col)

    return dir1_dict

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
    INIT_COST = 10000000000000000000
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

    #assert(cost < INIT_COST)
    #assert(cost > 0)

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
    INIT_COST = 10000000000000000000
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

    #assert(cost < INIT_COST)
    #assert(cost > 0)

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
    INIT_COST = 10000000000000000000
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

    #assert(cost < INIT_COST)
    #assert(cost > 0)

    return cost

seq_list = []
def reconstruct_path(prev_node_dict, curr_rc_set, key_dict, seq):
    global seq_list

    if not (len(curr_rc_set)):
        seq_list.append(seq)
        return

    for rc in curr_rc_set:
        _, next_rc_set = prev_node_dict[rc]

        next_seq = key_dict[rc] + seq
        reconstruct_path(prev_node_dict, next_rc_set, key_dict, next_seq)

# Works
def simulate_dir2(human_seq, dir_dict):
    seq = ''
    # Direction starts at A
    row, col = (0, 2)
    for h in human_seq:
        #assert((row, col) in dir_dict)
        if (h == 'A'):
            seq = seq + dir_dict[(row, col)]
            continue
        elif (h == '^'):
            n_row = row-1
            n_col = col
        elif (h == 'v'):
            n_row = row+1
            n_col = col
        elif (h == '>'):
            n_row = row
            n_col = col+1
        elif (h == '<'):
            n_row = row
            n_col = col-1

        n_tuple = (n_row, n_col)
        row, col = n_tuple
    return seq

# Works
def simulate_key(input_seq, key_dict):
    seq = ''
    # Direction starts at A
    row, col = (3, 2)
    for h in input_seq:
        #assert((row, col) in key_dict)
        if (h == 'A'):
            seq = seq + key_dict[(row, col)]
            continue
        elif (h == '^'):
            n_row = row-1
            n_col = col
        elif (h == 'v'):
            n_row = row+1
            n_col = col
        elif (h == '>'):
            n_row = row
            n_col = col+1
        elif (h == '<'):
            n_row = row
            n_col = col-1

        n_tuple = (n_row, n_col)
        row, col = n_tuple

    return seq

def process_inputs(in_file):
    output = 0

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
    for rc in dir_dict:
        dir_rc = dir_dict[rc]
        rev_dir_dict[dir_rc] = rc

    # Find cost of getting from one directional key to another
    human_cost_dict = defaultdict(int)
    dir_list = ['A', '^', 'v', '<', '>']
    for idx0, k0 in enumerate(dir_list):
        for idx1, k1 in enumerate(dir_list):
            # Check cost based on Manhattan distance
            k0_tuple = rev_dir_dict[k0]
            k1_tuple = rev_dir_dict[k1]
            dist = get_dist(k0_tuple, k1_tuple)
            # Plus 1 for cost of pressing A
            human_cost_dict[(k0, k1)] = dist + 1

    # Iterate through codes
    seq_dict = defaultdict(int)
    code_cost_dict = defaultdict(int)
    for code in codes_list:
        # Iterate through keys in code
        code_cost = 0
        seq = ""
        for idx, endkey in enumerate(code):
            if (idx == 0):
                startkey = 'A'
            else:
                startkey = code[idx-1]

            # Get dir1_dict
            # Contains number of presses needed on dir1
            dir1_dict = get_key_to_dir1(startkey, endkey, rev_key_dict)
            dir1_dict['A'] = 1

            len_dir1_dict = len(dir1_dict.keys())
            #assert(len_dir1_dict in [2, 3])

            # Get dir2_dict
            dir2_dict_list = []
            startdir1 = 'A'
            for dir1 in dir1_dict:
                dir2_dict = get_key_to_dir1(startdir1, dir1, rev_dir_dict)
                startdir1 = dir1

                # Needs to return to A, then press based on value in dir1_dict
                num_dir1 = dir1_dict[dir1]
                dir2_dict['A'] = num_dir1

                dir2_dict_list.append(dir2_dict)

            # Iterate through each dir2_dict, which represents a sequence
            code_seq = ""
            for dir2_dict in dir2_dict_list:
                dir2 = list(dir2_dict.keys())
                for d in dir2:
                    num = dir2_dict[d]
                    code_seq = code_seq + num*d
            #if (code == "379A"):
            #    print(startkey, endkey, code_seq)

            seq = seq + code_seq

            # Dijkstra's from startkey to endkey
            #curr_cost, curr_dir = run_dijkstra(startkey, endkey, curr_dir, key_dict, rev_key_dict, human_cost_dict)
            #tot_cost += curr_cost

        # Debug
        #if (code == "379A"):
        #    dir1_seq = simulate_dir2(seq, dir_dict)
        #    sim_code = simulate_key(dir1_seq, key_dict)
        #    print(sim_code)

        # Record cost
        code_cost += get_tot_human_cost(seq, human_cost_dict)
        code_cost_dict[code] = code_cost

        #if (code == '379A'):
        #    print(seq)
        
        # Record in seq_dict
        seq_dict[code] = seq

    # Evaluate
    for code in code_cost_dict:
        code_cost = code_cost_dict[code]
        #code_cost = len(seq_dict[code])
        num = int(code[:-1])

        complexity = code_cost*num
        output += complexity

        #print(f'complexity of {code}: {code_cost}*{num} = {complexity}')

    # DEBUGGING
    #result = run_dijkstra('A', '0', 'A', key_dict, rev_key_dict, human_cost_dict)
    #print(result)

    # Example
    #tot_cost = get_tot_human_cost("v<<A>>^A<A>AvA<^AA>A<vAAA>^A", human_cost_dict)
    #print(tot_cost)
    #get_key_to_robot_dir('2', '9', key_dict, rev_key_dict)
    #print(get_key_to_dir1('2', '9', rev_key_dict))

    # For 029A
    #print("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
    #actual_seq = simulate_dir2("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A", dir_dict)

    # For 379A
    #dir2_seq = simulate_dir2("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A", dir_dict)
    #print(dir2_seq)
    #dir1_seq = simulate_dir2(dir2_seq, dir_dict)
    #actual_code = simulate_key(dir1_seq, key_dict)
    #print(actual_code)

    # For 029A
    #dir1_seq = simulate_dir2("v<<A>>^A<A>AvA<^AA>A<vAAA>^A", dir_dict)
    #actual_code = simulate_key(dir1_seq, key_dict)
    #print(actual_code)

    #dir1_seq = simulate_dir2("<A>Av<<AA>^AA>AvAA^Av<AAA^>A", dir_dict)
    #code_seq = simulate_key(dir1_seq, key_dict)
    #print(f'Wrong   dir1_seq: {dir1_seq}')
    #print(f'Wrong   code_seq: {code_seq}')
    #dir1_seq = simulate_dir2("<A>Av<<AA>^AA>AvAA^A<vAAA>^A", dir_dict)
    #code_seq = simulate_key(dir1_seq, key_dict)
    #print(f'Correct dir1_seq: {dir1_seq}')
    #print(f'Correct code_seq: {code_seq}')

    return output

def process_inputs1(in_file, num_robots):
    output = 0

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

    # Find cost of getting from one directional key to another
    human_cost_dict = defaultdict(int)
    dir_list = ['A', '^', 'v', '<', '>']
    for idx0, k0 in enumerate(dir_list):
        for idx1, k1 in enumerate(dir_list):
            # Check cost based on Manhattan distance
            k0_tuple = rev_dir_dict[k0]
            k1_tuple = rev_dir_dict[k1]
            dist = get_dist(k0_tuple, k1_tuple)
            # Plus 1 for cost of pressing A
            human_cost_dict[(k0, k1)] = dist + 1

    # Iterate through codes
    seq_dict = defaultdict(int)
    cost_dict = defaultdict(int)
    for code in codes_list:
        # Iterate through keys in code
        cost = 0
        for idx, endkey in enumerate(code):
            if (idx == 0):
                startkey = 'A'
            else:
                startkey = code[idx-1]

            startkey_rc = rev_key_dict[startkey]
            endkey_rc   = rev_key_dict[endkey]

            # DFS on key chunk
            cost += dfs_key(startkey_rc, endkey_rc, num_robots)

        cost_dict[code] = cost

    # Evaluate
    output = 0
    for code in cost_dict:
        cost = cost_dict[code]
        num  = int(code[:-1])

        complexity = cost*num
        #print(f'Code {code}, complexity {complexity} = {cost}*{num}')
        output += complexity

    return output

# Only relevant functions for the solution are the dfs_* functions
# Other functions were either non-working solutions or helper functions to understand the problem better
#part1_example = process_inputs1(example_file, 2)
part1 = process_inputs1(input_file, 2)

#part2_example = process_inputs2(example_file)
part2 = process_inputs1(input_file, 25)

print("")
print("--- Advent of Code 2024 Day 21: Keypad Conundrum ---")
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
