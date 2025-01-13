#from functools import cache
from collections import deque

input_file = "../../inputs/2023/input17.txt"
example_file = "example17.txt"
#example_file = "example17_2.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

#@cache
def dfs_crucible_part1(row, col, direction, counter):
    print(row, col, direction, counter)

    if ((row, col, direction, counter) in visited):
        return 10000
    visited.add((row, col, direction, counter))

    # Base case
    curr_heat_loss = grid[row][col]
    if (row == MAX_ROW) and (col == MAX_COL):
        return curr_heat_loss

    u_heat_loss = 10000
    r_heat_loss = 10000
    d_heat_loss = 10000
    l_heat_loss = 10000
    for next_dir in ["u", "d", "l", "r"]:
        if (next_dir == direction):
            if (counter == 3):
                continue
            else:
                next_counter = counter+1
        # Do not move back to previous tile by checking current and next directions
        elif ((direction == "d") and (next_dir == "u")) or \
             ((direction == "u") and (next_dir == "d")) or \
             ((direction == "l") and (next_dir == "r")) or \
             ((direction == "r") and (next_dir == "l")):
            continue
        else:
            next_counter = 1

        # Up
        if (next_dir == "u") and (row > 0):
            next_row = row-1
            next_col = col
            if ((next_row, next_col, next_dir, next_counter) not in visited):
                u_heat_loss = dfs_crucible_part1(next_row, next_col, next_dir, next_counter)
        # Down
        elif (next_dir == "d") and (row < MAX_ROW):
            next_row = row+1
            next_col = col
            if ((next_row, next_col, next_dir, next_counter) not in visited):
                d_heat_loss = dfs_crucible_part1(next_row, next_col, next_dir, next_counter)
        # Left
        elif (next_dir == "l") and (col > 0):
            next_row = row
            next_col = col-1
            if ((next_row, next_col, next_dir, next_counter) not in visited):
                l_heat_loss = dfs_crucible_part1(next_row, next_col, next_dir, next_counter)
        # Right
        elif (next_dir == "r") and (col < MAX_COL):
            next_row = row
            next_col = col+1
            if ((next_row, next_col, next_dir, next_counter) not in visited):
                r_heat_loss = dfs_crucible_part1(next_row, next_col, next_dir, next_counter)

    # Return minimum heat loss
    return curr_heat_loss + min(u_heat_loss, r_heat_loss, d_heat_loss, l_heat_loss)

#@cache
def dfs_crucible_part2(row, col, direction, counter):
    curr_heat_loss = grid[row][col]

    # Base case
    if (row == MAX_ROW) and (col == MAX_COL):
        return curr_heat_loss

    u_heat_loss = 10000
    r_heat_loss = 10000
    d_heat_loss = 10000
    l_heat_loss = 10000
    for next_dir in ["u", "d", "l", "r"]:
        if (next_dir == direction):
            if (counter == 3):
                continue
            else:
                next_counter = counter+1
        else:
            next_counter = 1

        # Up
        if (next_dir == "u") and (row > 0):
            u_heat_loss = curr_heat_loss + dfs_crucible_part2(row-1, col, next_dir, next_counter)
        # Down
        elif (next_dir == "d") and (row < MAX_ROW):
            d_heat_loss = curr_heat_loss + dfs_crucible_part2(row+1, col, next_dir, next_counter)
        # Left
        elif (next_dir == "l") and (col > 0):
            l_heat_loss = curr_heat_loss + dfs_crucible_part2(row, col-1, next_dir, next_counter)
        # Right
        elif (next_dir == "r") and (col < MAX_COL):
            r_heat_loss = curr_heat_loss + dfs_crucible_part2(row, col+1, next_dir, next_counter)

    # Return minimum heat loss
    return min(u_heat_loss, r_heat_loss, d_heat_loss, l_heat_loss)

def process_inputs(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append([int(x) for x in line])

            line = file.readline()

    max_rows = len(grid)-1
    max_cols = len(grid[0])-1
    LARGE_DIST = 1000000
    h_grid = {}
    for counter in range(1, 4):
        for d in ['u', 'd', 'l', 'r']:
            for r in range(0, max_rows+1):
                for c in range(0, max_cols+1):
                    if (r,c) == (0, 0):
                        h_grid[(r, c, d, counter)] = 0
                    else:
                        h_grid[(r, c, d, counter)] = LARGE_DIST
    h_grid[(0, 0, 'r', 0)] = 0
    h_grid[(0, 0, 'd', 0)] = 0
    #h_grid[0][0] = 0

    #for g in grid:
    #    for i in g:
    #        print(i, end="")
    #    print("")

    # Dijkstra's
    queue = []
    visited = set()

    #unvisited = []
    #for counter in range(1, 4):
    #    for d in ['u', 'd', 'l', 'r']:
    #        for r in range(0, max_rows+1):
    #            for c in range(0, max_cols+1):
    #                if ((r, c) != (0, 0)):
    #                    unvisited.append((r, c, d, counter))
    #                else:
    #                    visited.add((r, c, d, counter))

    # row, column, heat loss, direction, direction counter
    #queue.append((0, 0, 0, 'stationary', 0))
    queue.append((0, 0, 0, 'r', 0))
    queue.append((0, 0, 0, 'd', 0))

    left_dist = LARGE_DIST
    right_dist = LARGE_DIST
    up_dist = LARGE_DIST
    down_dist = LARGE_DIST

    TARGET = (max_rows, max_cols)
    #TARGET = (1, 8)
    r_target, c_target = TARGET
    while len(queue):
    #while len(unvisited):
             
        # PRIORITY QUEUE
        min_h = LARGE_DIST
        min_idx = 0
        pop_list = []
        #for idx, p in enumerate(unvisited):
        for idx, p in enumerate(queue):
            r, c, h, d, counter = p
            state = (r, c, d, counter)
            if (h > h_grid[state]):
               pop_list.append(idx) 
            #h = h_grid[r][c]
            else:
                h = h_grid[state]
                if (h <= min_h):
                    min_h = h
                    min_idx = idx
                    q = (r, c, h, d, counter)
        pop_list.append(min_idx)
        for idx in list(reversed(sorted(pop_list))):
            queue.pop(idx)
        #q = unvisited.pop(min_idx)

        # BFS
        #q = queue.pop(0)
        print(len(queue))
        print(q)
        r, c, h_q, d, counter = q
        state = (r, c, d, counter)
        #h = h_grid[r][c] # re-read from h_grid since h might have already updated
        h = h_grid[state] # re-read from h_grid since h might have already updated
        #if (r, c) in [(1, 4), (0, 1), (0, 2), (0, 3), (0,4), (1,1), (1,2), (1,3)]:
        #if (r, c) in [(12, 12), (11, 12), (12, 11)]:
        #    print(q)

        #if (h > h_grid[r][c]):
        #    continue

        #if (r, c) == TARGET:
        #    break

        #if (state in visited):# and (h > h_grid[r][c]):
        #    #visited.add(state)
        #    continue

        if (h_q > h):
            #visited.add(state)
            continue

        if (state in visited):
            continue

        stop = True
        for counter_t in range(1, 4):
            for d_t in ['u', 'd', 'l', 'r']:
                if (h_grid[(r_target, c_target, d_t, counter_t)] == LARGE_DIST):
                    stop = False
        if stop:
            break

        CAN_UP    = (not ((d == 'u') and (counter >= 3))) and (r > 0) and (d != 'd')
        CAN_DOWN  = (not ((d == 'd') and (counter >= 3))) and (r < max_rows) and (d != 'u')
        CAN_RIGHT = (not ((d == 'r') and (counter >= 3))) and (c < max_cols) and (d != 'l')
        CAN_LEFT  = (not ((d == 'l') and (counter >= 3))) and (c > 0) and (d != 'r')

        assert(counter <= 3)

        if (CAN_UP):
            next_r = r-1
            next_c = c
            next_d = 'u'
            if (d == 'u'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        if (CAN_DOWN):
            next_r = r+1
            next_c = c
            next_d = 'd'
            if (d == 'd'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        if (CAN_RIGHT):
            next_r = r
            next_c = c+1
            next_d = 'r'
            if (d == 'r'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        if (CAN_LEFT):
            next_r = r
            next_c = c-1
            next_d = 'l'
            if (d == 'l'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        visited.add(state)

    r, c = TARGET
    #output = h_grid[r][c]
    output = LARGE_DIST+1
    for counter in range(1, 4):
        for d in ['u', 'd', 'l', 'r']:
            h = h_grid[(r, c, d, counter)]
            if (h <= output):
                output = h
                print(f'h = {h}, d = {d}, counter = {counter}')

    #for h in h_grid:
    #    print(h)

    return output

def process_inputs2(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append([int(x) for x in line])

            line = file.readline()

    max_rows = len(grid)-1
    max_cols = len(grid[0])-1
    LARGE_DIST = 1000000
    h_grid = {}
    for counter in range(1, 11):
        for d in ['u', 'd', 'l', 'r']:
            for r in range(0, max_rows+1):
                for c in range(0, max_cols+1):
                    if (r,c) == (0, 0):
                        h_grid[(r, c, d, counter)] = 0
                    else:
                        h_grid[(r, c, d, counter)] = LARGE_DIST
    h_grid[(0, 0, 'r', 0)] = 0
    h_grid[(0, 0, 'd', 0)] = 0
    #h_grid[0][0] = 0

    #for g in grid:
    #    for i in g:
    #        print(i, end="")
    #    print("")

    # Dijkstra's
    queue = []
    visited = set()

    #unvisited = []
    #for counter in range(1, 4):
    #    for d in ['u', 'd', 'l', 'r']:
    #        for r in range(0, max_rows+1):
    #            for c in range(0, max_cols+1):
    #                if ((r, c) != (0, 0)):
    #                    unvisited.append((r, c, d, counter))
    #                else:
    #                    visited.add((r, c, d, counter))

    # row, column, heat loss, direction, direction counter
    #queue.append((0, 0, 0, 'stationary', 0))
    queue.append((0, 0, 0, 'r', 0))
    queue.append((0, 0, 0, 'd', 0))

    left_dist = LARGE_DIST
    right_dist = LARGE_DIST
    up_dist = LARGE_DIST
    down_dist = LARGE_DIST

    TARGET = (max_rows, max_cols)
    #TARGET = (1, 8)
    r_target, c_target = TARGET
    print_count = 0
    while len(queue):
    #while len(unvisited):
        print_count += 1
        if (print_count >= 10000):
            print(len(queue))
            print(q)
            print_count = 0

        # PRIORITY QUEUE
        min_h = LARGE_DIST
        min_idx = 0
        pop_list = []
        #for idx, p in enumerate(unvisited):
        for idx, p in enumerate(queue):
            r, c, h, d, counter = p
            state = (r, c, d, counter)
            if (h > h_grid[state]):
               pop_list.append(idx) 
            #h = h_grid[r][c]
            else:
                h = h_grid[state]
                if (h <= min_h):
                    min_h = h
                    min_idx = idx
                    q = (r, c, h, d, counter)
        pop_list.append(min_idx)
        for idx in list(reversed(sorted(pop_list))):
            queue.pop(idx)
        #q = unvisited.pop(min_idx)

        # BFS
        #q = queue.pop(0)
        r, c, h_q, d, counter = q
        state = (r, c, d, counter)
        #h = h_grid[r][c] # re-read from h_grid since h might have already updated
        h = h_grid[state] # re-read from h_grid since h might have already updated
        #if (r, c) in [(1, 4), (0, 1), (0, 2), (0, 3), (0,4), (1,1), (1,2), (1,3)]:
        #if (r, c) in [(12, 12), (11, 12), (12, 11)]:
        #    print(q)

        #if (h > h_grid[r][c]):
        #    continue

        #if (r, c) == TARGET:
        #    break

        #if (state in visited):# and (h > h_grid[r][c]):
        #    #visited.add(state)
        #    continue

        if (h_q > h):
            #visited.add(state)
            continue

        if (state in visited):
            continue

        stop = True
        for counter_t in range(4, 11):
            for d_t in ['u', 'd', 'l', 'r']:
                if (h_grid[(r_target, c_target, d_t, counter_t)] == LARGE_DIST):
                    stop = False
        if stop:
            break

        CAN_UP    = (not ((d == 'u') and (counter >= 10))) and (r > 0) and (d != 'd') and (not ((d != 'u') and (counter < 4)))
        CAN_DOWN  = (not ((d == 'd') and (counter >= 10))) and (r < max_rows) and (d != 'u') and (not ((d != 'd') and (counter < 4)))
        CAN_RIGHT = (not ((d == 'r') and (counter >= 10))) and (c < max_cols) and (d != 'l') and (not ((d != 'r') and (counter < 4)))
        CAN_LEFT  = (not ((d == 'l') and (counter >= 10))) and (c > 0) and (d != 'r') and (not ((d != 'l') and (counter < 4)))

        assert(counter <= 10)

        if (CAN_UP):
            next_r = r-1
            next_c = c
            next_d = 'u'
            if (d == 'u'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        if (CAN_DOWN):
            next_r = r+1
            next_c = c
            next_d = 'd'
            if (d == 'd'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        if (CAN_RIGHT):
            next_r = r
            next_c = c+1
            next_d = 'r'
            if (d == 'r'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        if (CAN_LEFT):
            next_r = r
            next_c = c-1
            next_d = 'l'
            if (d == 'l'):
                next_counter = counter + 1
            else:
                next_counter = 1
            if ((h + grid[next_r][next_c]) <= h_grid[(next_r, next_c, next_d, next_counter)]):
                next_h = min(h_grid[(next_r, next_c, next_d, next_counter)], h + grid[next_r][next_c])
                h_grid[(next_r, next_c, next_d, next_counter)] = next_h
                queue.append((next_r, next_c, next_h, next_d, next_counter))

        visited.add(state)

    r, c = TARGET
    #output = h_grid[r][c]
    output = LARGE_DIST+1
    for counter in range(4, 11):
        for d in ['u', 'd', 'l', 'r']:
            h = h_grid[(r, c, d, counter)]
            if (h <= output):
                output = h
                print(f'h = {h}, d = {d}, counter = {counter}')

    #for h in h_grid:
    #    print(h)

    return output

def process_inputs_part1_2(in_file):
    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append([int(x) for x in line])

            line = file.readline()

    MAX_ROW = len(grid)-1
    MAX_COL = len(grid[0])-1

    # Part 1
    part1 = 0
    q = []
    q.append((0, (0, 0, "init")))

    visited = set()
    for direction in ["l", "u"]:
        visited.add((0, 0, direction))

    # Dictionary of costs saved as (row, col, direction) : cost
    cost_dict = {}
    END_RIGHT_TUPLE = (MAX_ROW, MAX_COL, "r")
    END_DOWN_TUPLE  = (MAX_ROW, MAX_COL, "d")

    # Dijkstra's
    while len(q):
        # Priority queue
        q.sort()
        cost, curr_tuple = q.pop(0)
        #print(cost, curr_tuple)
        row, col, direction = curr_tuple

        # DEBUG
        #if (row == MAX_ROW) and (col == MAX_COL):
        #    part1 = cost
        #    break

        #if (curr_tuple in visited):
        #    continue
        #visited.add(curr_tuple)

        ## Early exit condition is when exit is reached in both directions
        #if (END_RIGHT_TUPLE in visited) and (END_DOWN_TUPLE in visited):
        #    break

        # Vertical directions
        if (direction not in ["u", "d"]): # direction dependent
            # Up
            heat_loss = 0
            for next_row in range(row-1, row-4, -1): # direction dependent
                if (next_row < 0): # direction dependent
                    break

                heat_loss += grid[next_row][col] # direction dependent
                next_cost = cost + heat_loss

                next_tuple = (next_row, col, "u") # direction dependent
                #if (next_tuple not in visited):

                if (next_tuple in cost_dict):
                    prev_cost = cost_dict[next_tuple]

                    if (prev_cost > next_cost):
                        cost_dict[next_tuple] = next_cost
                        q.append((next_cost, next_tuple))
                else:
                    cost_dict[next_tuple] = next_cost
                    q.append((next_cost, next_tuple))

            # Down
            heat_loss = 0
            for next_row in range(row+1, row+4): # direction dependent
                if (next_row > MAX_ROW): # direction dependent
                    break

                heat_loss += grid[next_row][col] # direction dependent
                next_cost = cost + heat_loss

                next_tuple = (next_row, col, "d") # direction dependent
                #if (next_tuple not in visited):

                if (next_tuple in cost_dict):
                    prev_cost = cost_dict[next_tuple]

                    if (prev_cost > next_cost):
                        cost_dict[next_tuple] = next_cost
                        q.append((next_cost, next_tuple))
                else:
                    cost_dict[next_tuple] = next_cost
                    q.append((next_cost, next_tuple))

        # Horizontal directions
        if (direction not in ["l", "r"]): # direction dependent
            # Left
            heat_loss = 0
            for next_col in range(col-1, col-4, -1): # direction dependent
                if (next_col < 0): # direction dependent
                    break

                heat_loss += grid[row][next_col] # direction dependent
                next_cost = cost + heat_loss

                next_tuple = (row, next_col, "l") # direction dependent
                #if (next_tuple not in visited):

                if (next_tuple in cost_dict):
                    prev_cost = cost_dict[next_tuple]

                    if (prev_cost > next_cost):
                        cost_dict[next_tuple] = next_cost
                        q.append((next_cost, next_tuple))
                else:
                    cost_dict[next_tuple] = next_cost
                    q.append((next_cost, next_tuple))

            # Right
            heat_loss = 0
            for next_col in range(col+1, col+4): # direction dependent
                if (next_col > MAX_COL): # direction dependent
                    break

                heat_loss += grid[row][next_col] # direction dependent
                next_cost = cost + heat_loss

                next_tuple = (row, next_col, "r") # direction dependent
                #if (next_tuple not in visited):

                if (next_tuple in cost_dict):
                    prev_cost = cost_dict[next_tuple]

                    if (prev_cost > next_cost):
                        cost_dict[next_tuple] = next_cost
                        q.append((next_cost, next_tuple))
                else:
                    cost_dict[next_tuple] = next_cost
                    q.append((next_cost, next_tuple))
        # End of Dijkstra's

    #print(cost_dict)
    #print(MAX_ROW, MAX_COL)

    cost1 = 100000 
    cost2 = 100000 
    if (END_RIGHT_TUPLE in cost_dict):
        cost1 = cost_dict[END_RIGHT_TUPLE]
    if (END_DOWN_TUPLE in cost_dict):
        cost2 = cost_dict[END_DOWN_TUPLE]
    part1 = min(cost1, cost2)

    # DEBUG
    #for curr_tuple in cost_dict:
    #    print(f'{curr_tuple} : {cost_dict[curr_tuple]}')

    # Part 2
    # TODO
    part2 = 0

    return part1, part2

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2 = process_inputs2(input_file)

#part1, part2 = process_inputs_part1_2(example_file)
part1, part2 = process_inputs_part1_2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
