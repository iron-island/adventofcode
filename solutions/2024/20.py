from collections import defaultdict, deque

input_file = "../../inputs/2024/input20.txt"
example_file = "example20.txt"
example2_file = "example20_2.txt"
example3_file = "example20_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0
def print_grid(grid_dict, MAX_ROW, MAX_COL, visited=""):
    for row in range(0, MAX_ROW+1):
        for col in range(0, MAX_COL+1):
            if (row, col) in visited:
                print("O", end="")
            else:
                print(grid_dict[(row, col)], end="")
        print("")

def get_dist(tuple1, tuple2):
    row1, col1 = tuple1
    row2, col2 = tuple2

    diff_row = abs(row2-row1)
    diff_col = abs(col2-col1)

    return diff_row+diff_col

def process_inputs(in_file):
    output = 0

    grid_dict = defaultdict(str)
    with open(in_file) as file:
        line = file.readline()

        row = 0    
        while line:
            line = line.strip()

            for col, l in enumerate(line):
                grid_dict[(row, col)] = l

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
    q = deque()
    visited = set()
    t = 0
    row, col = S_pos
    q.append((row, col, t))
    while (len(q)):
        row, col, t = q.popleft()

        if ((row, col) == E_pos):
            break

        if ((row, col) in visited):
            continue
        visited.add((row, col))

        # up
        n_row = row-1
        n_col = col
        n_tuple = (n_row, n_col)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            q.append((n_row, n_col, t+1))

        # down
        n_row = row+1
        n_col = col
        n_tuple = (n_row, n_col)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            q.append((n_row, n_col, t+1))

        # left
        n_row = row
        n_col = col-1
        n_tuple = (n_row, n_col)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            q.append((n_row, n_col, t+1))

        # right
        n_row = row
        n_col = col+1
        n_tuple = (n_row, n_col)
        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            q.append((n_row, n_col, t+1))

    max_t = t

    # Get list of inner walls where cheats can start
    wall_list = []
    for rc in grid_dict:
        row, col = rc
        tile = grid_dict[rc]

        if (row == 0) or (row == MAX_ROW) or (col == 0) or (col == MAX_COL):
            continue

        up_tile    = grid_dict[(row-1, col)]
        down_tile  = grid_dict[(row+1, col)]
        left_tile  = grid_dict[(row, col-1)]
        right_tile = grid_dict[(row, col+1)]

        adj_tile_list = [up_tile, down_tile, left_tile, right_tile]

        # Must not be a space, not at the boundary, and has adjacent .
        if (tile != '.') and (row > 0) and (row < MAX_ROW) and (col > 0) and (col < MAX_COL) and ('.' in adj_tile_list):
            wall_list.append(rc)

    # Debug cheat1
    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        if ((row, col) in wall_list):
    #            print('1', end="")
    #        else:
    #            print(grid_dict[(row, col)], end="")
    #    print("")

    # Find pairs of tiles for cheating
    #cheat_set = set()
    #for wall in wall_list:
    #    row, col = wall

    #    # up
    #    n_row = row-1
    #    n_col = col
    #    n_tuple = (n_row, n_col)
    #    n_cheat = (row, col, n_row, n_col)
    #    if (n_tuple in wall_list):
    #        cheat_set.add(n_cheat)

    #    # down
    #    n_row = row+1
    #    n_col = col
    #    n_tuple = (n_row, n_col)
    #    n_cheat = (row, col, n_row, n_col)
    #    if (n_tuple in wall_list):
    #        cheat_set.add(n_cheat)

    #    # left
    #    n_row = row
    #    n_col = col-1
    #    n_tuple = (n_row, n_col)
    #    n_cheat = (row, col, n_row, n_col)
    #    if (n_tuple in wall_list):
    #        cheat_set.add(n_cheat)

    #    # right
    #    n_row = row
    #    n_col = col+1
    #    n_tuple = (n_row, n_col)
    #    n_cheat = (row, col, n_row, n_col)
    #    if (n_tuple in wall_list):
    #        cheat_set.add(n_cheat)

    # Find all cheats
    #for idx, cheat in enumerate(cheat_set):
    for idx, wall in enumerate(wall_list):
        #if ((idx % 500) == 0):
        #    print(f'{idx} of {len(wall_list)-1}')

        row1, col1 = wall
        cheat1 = wall
        # Iterate through cheat2
        for i in range(0, 4):
            if (i == 0): # up
                row2 = row1-1
                col2 = col1
            elif (i == 1): # down
                row2 = row1+1
                col2 = col1
            elif (i == 2): # left
                row2 = row1
                col2 = col1-1
            elif (i == 3): # right
                row2 = row1
                col2 = col1+1

            # cheat2 should not be a wall
            cheat2 = (row2, col2)
            if (grid_dict[cheat2] == '#'):
                continue

            # Remove wall
            old_tile1 = grid_dict[cheat1]
            old_tile2 = grid_dict[cheat2]
            grid_dict[cheat1] = '1'
            grid_dict[(row2, col2)] = '2'

            # Debug:
            #if (cheat1 == (7, 10)) and (cheat2 == (7, 9)):
            #    print_grid(grid_dict, MAX_ROW, MAX_COL)

            # Internal BFS
            q = deque()
            visited = set()
            t = 0
            row, col = S_pos
            q.append((row, col, t))
            found_exit = False
            while (len(q)):
                row, col, t = q.popleft()

                if ((row, col) == E_pos):
                    found_exit = True
                    break

                if ((row, col) in visited):
                    continue
                visited.add((row, col))

                # If in cheat1, must go to cheat2
                if ((row, col) == cheat1):
                    q.append((row2, col2, t+1))
                    continue

                # up
                n_row = row-1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                    if not (((n_tuple == cheat1) and (cheat2 in visited)) or
                            ((n_tuple == cheat2) and (cheat1 not in visited))):
                        q.append((n_row, n_col, t+1))

                # down
                n_row = row+1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                    if not (((n_tuple == cheat1) and (cheat2 in visited)) or
                            ((n_tuple == cheat2) and (cheat1 not in visited))):
                        q.append((n_row, n_col, t+1))

                # left
                n_row = row
                n_col = col-1
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                    if not (((n_tuple == cheat1) and (cheat2 in visited)) or
                            ((n_tuple == cheat2) and (cheat1 not in visited))):
                        q.append((n_row, n_col, t+1))

                # right
                n_row = row
                n_col = col+1
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                    if not (((n_tuple == cheat1) and (cheat2 in visited)) or
                            ((n_tuple == cheat2) and (cheat1 not in visited))):
                        q.append((n_row, n_col, t+1))

            # BFS while loop ended here

            # Evaluate
            if (found_exit) and ((max_t - t) >= 100):
                output += 1
                #adj_cheat1 = (cheat1[0]+1, cheat1[1]+1)
                #adj_cheat2 = (cheat2[0]+1, cheat2[1]+1)
                #print(f'Cheat1: {adj_cheat1}, Cheat2: {adj_cheat2} to save {max_t-t}')
                ## DEBUG
                #for row in range(0, MAX_ROW+1):
                #    for col in range(0, MAX_COL+1):
                #        if ((row, col) == cheat1):
                #            print('1', end="")
                #        elif ((row, col) == cheat2):
                #            print('2', end="")
                #        elif ((row, col) in visited):
                #            print('O', end="")
                #        else:
                #            print(grid_dict[(row, col)], end="")
                #    print("")

            # Return the wall
            grid_dict[cheat1] = old_tile1
            grid_dict[cheat2] = old_tile2

    # Cheat
    #q = deque()
    #visited = set()
    #t = 0
    #row, col = S_pos
    #num = 0
    #q.append((row, col, t, num))
    #while (len(q)):
    #    row, col, t, num = q.popleft()

    #    if ((row, col) == E_pos):
    #        break

    #    if ((row, col, num) in visited):
    #        continue
    #    visited.add((row, col, num))

    #    # up
    #    n_row = row-1
    #    n_col = col
    #    n_tuple = (n_row, n_col)
    #    if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
    #        q.append((n_row, n_col, t+1, num))
    #    if (n_tuple in grid_dict) and (num == 1): # must cheat
    #        q.append((n_row, n_col, t+1, num+1))
    #    if (n_tuple in grid_dict) and (n_tuple in wall_list) and (num == 0):
    #        q.append((n_row, n_col, t+1, num+1))

    #    # down
    #    n_row = row+1
    #    n_col = col
    #    n_tuple = (n_row, n_col)
    #    if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
    #        q.append((n_row, n_col, t+1, num))
    #    if (n_tuple in grid_dict) and (num == 1): # must cheat
    #        q.append((n_row, n_col, t+1, num+1))
    #    if (n_tuple in grid_dict) and (n_tuple in wall_list) and (num == 0):
    #        q.append((n_row, n_col, t+1, num+1))

    #    # left
    #    n_row = row
    #    n_col = col-1
    #    n_tuple = (n_row, n_col)
    #    if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
    #        q.append((n_row, n_col, t+1, num))
    #    if (n_tuple in grid_dict) and (num == 1): # must cheat
    #        q.append((n_row, n_col, t+1, num+1))
    #    if (n_tuple in grid_dict) and (n_tuple in wall_list) and (num == 0):
    #        q.append((n_row, n_col, t+1, num+1))

    #    # right
    #    n_row = row
    #    n_col = col+1
    #    n_tuple = (n_row, n_col)
    #    if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
    #        q.append((n_row, n_col, t+1, num))
    #    if (n_tuple in grid_dict) and (num == 1): # must cheat
    #        q.append((n_row, n_col, t+1, num+1))
    #    if (n_tuple in grid_dict) and (n_tuple in wall_list) and (num == 0):
    #        q.append((n_row, n_col, t+1, num+1))

    return output

def process_inputs2(in_file, check):
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
        #if ((row, col) in idx_dict):
        #    continue
        #idx_dict[(row, col)] = idx
        #idx += 1

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
    #assert(len(best_path) == max_t+1)
    #assert(best_path[0] == S_pos)
    #assert(best_path[-1] == E_pos)

    # Convert to dict
    idx_dict = defaultdict(int)
    for idx, rc in enumerate(best_path):
        idx_dict[rc] = idx

    # Loop through best_path to connect cheat0 and cheat2, excluding E for cheat0
    saved_dict = defaultdict(int)
    offset_list = [(r, c) for r in range(-20, 21) for c in range(abs(r)-20, (20-abs(r))+1)]
    part1 = 0
    part2 = 0
    for idx, cheat0 in enumerate(best_path[:-1]):
        #cheat2_list = best_path[(idx+1):]
        #if (idx % 100) == 0:
        #    print(f'Checking cheat0 index {idx} of {len(best_path[:-1])-1}')

        start_row, start_col = cheat0
        #for row_offset in range(-20, 21):
        #    max_col_offset = 20-abs(row_offset)
        #    for col_offset in range(-max_col_offset, max_col_offset+1):
        for offset in offset_list:
            row_offset, col_offset = offset
            dist = abs(row_offset) + abs(col_offset)
            cheat2 = (start_row+row_offset, start_col+col_offset)
            #assert(dist == get_dist(cheat0, cheat2))
            if (cheat2 in idx_dict) and (idx_dict[cheat2] > idx):
                saved = idx_dict[cheat2] - idx - dist
                #saved_dict[saved] += 1

                if (saved >= 100):
                    # Part 1 is a subset of Part 2 when cheat lasts at most 2 picoseconds
                    if (dist <= 2):
                        part1 += 1

                    part2 += 1

        #for idx2, cheat2 in enumerate(best_path[idx+1:]):
        #    dist = get_dist(cheat0, cheat2)

        #    if (dist <= 20):
        #        #idx2 = best_path.index(cheat2)
        #        #saved = (idx2 - idx) - dist
        #        saved = idx2 - dist + 1
        #        saved_dict[saved] += 1
    return part1, part2

    # Initial optimization when savings were added to a dictionary,
    if (check == "example"):
        saved = 54
        part2 = saved_dict[saved]
    else:
        for saved in saved_dict:
            if (saved >= 100):
                part2 += saved_dict[saved]

    return part1, part2

    # Alternatives 1 and 2: DOES NOT WORK
    # Get list of inner walls where cheats can start
    wall_list = []
    cheat0_set = set()
    for rc in grid_dict:
        row, col = rc
        tile = grid_dict[rc]

        if (row == 0) or (row == MAX_ROW) or (col == 0) or (col == MAX_COL):
            continue

        up    = (row-1, col)
        down  = (row+1, col)
        left  = (row, col-1)
        right = (row, col+1)

        up_tile    = grid_dict[up]
        down_tile  = grid_dict[down]
        left_tile  = grid_dict[left]
        right_tile = grid_dict[right]

        adj_tile_list = [up_tile, down_tile, left_tile, right_tile]

        # Must not be a space, not at the boundary, and has adjacent .
        if (tile != '.') and (row > 0) and (row < MAX_ROW) and (col > 0) and (col < MAX_COL) and ('.' in adj_tile_list):
            wall_list.append(rc)

            if (up_tile == '.') and (up in visited):
                cheat0_set.add(up)
            if (down_tile == '.') and (down in visited):
                cheat0_set.add(down)
            if (left_tile == '.') and (left in visited):
                cheat0_set.add(left)
            if (right_tile == '.') and (right in visited):
                cheat0_set.add(right)
    # Add starting position to cheat0_set
    cheat0_set.add(S_pos)

    # Debugging
    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        if ((row, col) in cheat0_set):
    #            print("0", end="")
    #        else:
    #            print(grid_dict[(row, col)], end="")
    #    print("")

    #return 0

    # Find all cheats part2
    #for idx, wall in enumerate(wall_list):
    idx = 0
    for cheat0 in cheat0_set:
        #if ((idx % 100) == 0):
        #    print(f'{idx} of {len(wall_list)-1}')
        idx += 1

        row0, col0 = cheat0
        # Iterate through cheat lengths
        # cheat2 ends from 2 to 20 so manhattan distance should be from 2 to 20 as well
        # but cut off until distance to E
        diff_E = get_dist(cheat0, E_pos)
        MIN_DIFF_CHEAT = min(diff_E, 20)
        MIN_DIFF_CHEAT = 20 # so that non-optimal cheats are still tried, since they might still save some time
        for diff_cheat in range(2, MIN_DIFF_CHEAT+1):
            MAX_CHEAT_MODE = diff_cheat+1
            cheat2_set = set()
            # Get possible cheat2's
            for row2 in range(row0-diff_cheat, row0+diff_cheat+1):
                for col2 in range(col0-diff_cheat, col0+diff_cheat+1):
                    diff_row = abs(row0 - row2)
                    diff_col = abs(col0 - col2)

                    actual_diff = diff_row + diff_col
                    if (actual_diff != diff_cheat):
                        continue
                    else:
                        cheat2 = (row2, col2)
                        in_row = (row2 > 0) and (row2 < MAX_ROW)
                        in_col = (col2 > 0) and (col2 < MAX_COL)
                        if (in_row and in_col) and (grid_dict[cheat2] != '#'):
                            cheat2_set.add(cheat2)

            # Debug
            #print(f'{idx}: diff_cheat {diff_cheat}/{MIN_DIFF_CHEAT}')

            # Alternative 2: Remove walls between cheat0 and cheat2
            # Iterate through possible cheat2's
            #for cheat2 in cheat2_set:
            #    row2, col2 = cheat2

            #    # Remove wall
            #    old_grid_dict = defaultdict(str)
            #    min_row = min(row0, row2)
            #    max_row = max(row0, row2)
            #    min_col = min(col0, col2)
            #    max_col = max(col0, col2)
            #    found_walls = False
            #    for r in range(min_row, max_row+1):
            #        for c in range(min_col, max_col+1):
            #            rc = (r, c)
            #            old_tile = grid_dict[rc]
            #            old_grid_dict[rc] = old_tile
            #            grid_dict[rc] = 'O'
            #            if (old_tile == '#'):
            #                found_walls = True

            #    # If no walls were removed, go to next iteration
            #    if (not found_walls):
            #        for rc in old_grid_dict:
            #            grid_dict[rc] = old_grid_dict[rc]
            #        continue

            #    # Internal A*
            #    q = []
            #    visited = set()
            #    t = 0
            #    row, col = S_pos
            #    dist = get_dist(S_pos, E_pos)
            #    q.append((t+dist, row, col, t))
            #    found_exit = False
            #    dist = 0
            #    while (len(q)):
            #        # Priority queue
            #        q.sort()
            #        heuristic, row, col, t = q.pop(0)

            #        if ((row, col) == E_pos):
            #            found_exit = True
            #            break

            #        #if ((row, col) in old_grid_dict) and (cheat0 not in visited):
            #        #    # Not a valid cheat path since we didn't start from cheat0
            #        #    print("Invalid path!")
            #        #    break

            #        if ((row, col) in visited):
            #            continue
            #        visited.add((row, col))

            #        # up
            #        n_row = row-1
            #        n_col = col
            #        n_tuple = (n_row, n_col)
            #        dist = get_dist(n_tuple, E_pos)
            #        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            #            q.append((t+1+dist, n_row, n_col, t+1))

            #        # down
            #        n_row = row+1
            #        n_col = col
            #        n_tuple = (n_row, n_col)
            #        dist = get_dist(n_tuple, E_pos)
            #        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            #            q.append((t+1+dist, n_row, n_col, t+1))

            #        # left
            #        n_row = row
            #        n_col = col-1
            #        n_tuple = (n_row, n_col)
            #        dist = get_dist(n_tuple, E_pos)
            #        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            #            q.append((t+1+dist, n_row, n_col, t+1))

            #        # right
            #        n_row = row
            #        n_col = col+1
            #        n_tuple = (n_row, n_col)
            #        dist = get_dist(n_tuple, E_pos)
            #        if (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
            #            q.append((t+1+dist, n_row, n_col, t+1))

            #    # BFS while loop ended here
            #    if (diff_cheat == 6) and (cheat0 == S_pos):
            #        print(cheat0, cheat2, cheat2_set)
            #        print("print_grid")
            #        for row in range(0, MAX_ROW+1):
            #            for col in range(0, MAX_COL+1):
            #                if ((row, col) in visited) and ((row, col) not in old_grid_dict):
            #                    print("x", end="")
            #                else:
            #                    print(grid_dict[(row, col)], end="")
            #            print("")

            #    # Evaluate
            #    if (check == "example"):
            #        if_check = ((max_t - t) == 76)
            #    else:
            #        if_check = ((max_t - t) >= 100)
            #    print(f'max_t - t = {max_t-t}')
            #    if (found_exit) and if_check:
            #        output += 1
            #        #adj_cheat1 = (cheat1[0]+1, cheat1[1]+1)
            #        #adj_cheat2 = (cheat2[0]+1, cheat2[1]+1)
            #        #print(f'Cheat1: {adj_cheat1}, Cheat2: {adj_cheat2} to save {max_t-t}')
            #        ## DEBUG
            #        #for row in range(0, MAX_ROW+1):
            #        #    for col in range(0, MAX_COL+1):
            #        #        if ((row, col) == cheat1):
            #        #            print('1', end="")
            #        #        elif ((row, col) == cheat2):
            #        #            print('2', end="")
            #        #        elif ((row, col) in visited):
            #        #            print('O', end="")
            #        #        else:
            #        #            print(grid_dict[(row, col)], end="")
            #        #    print("")

            #    # Return the wall
            #    for rc in old_grid_dict:
            #        grid_dict[rc] = old_grid_dict[rc]

            # Alternative 1
            # Iterate through possible cheat2's
            for cheat2 in cheat2_set:
                row2, col2 = cheat2
                # Remove wall
                #old_tile1 = grid_dict[cheat1]
                #old_tile2 = grid_dict[cheat2]
                #grid_dict[cheat1] = '1'
                #grid_dict[(row2, col2)] = '2'

                # Debug:
                #if (cheat1 == (7, 10)) and (cheat2 == (7, 9)):
                #    print_grid(grid_dict, MAX_ROW, MAX_COL)

                # Internal A*
                q = deque()
                visited = set()
                t = 0
                row, col = S_pos
                dist = get_dist(S_pos, E_pos)
                q.append((row, col, t))
                found_exit = False
                dist = 0
                cheat_mode = 0
                while (len(q)):
                    row, col, t = q.popleft()

                    if ((row, col) == E_pos):
                        found_exit = True
                        break

                    #if ((row, col) == cheat0) and (cheat2 in visited):
                    #    # Not a valid cheat path
                    #    break

                    if ((row, col) in visited):
                        continue
                    visited.add((row, col))

                    # If in cheat mode, "teleport" to cheat2 and add all tiles within cheat1 and cheat2 as visited
                    if (cheat_mode == 1) or ((cheat0 == S_pos) and ((row, col) == S_pos)):
                        q.append((row2, col2, t+diff_cheat))
                        cheat_mode = 2
                        # Debug
                        #if (cheat0 == S_pos) and (cheat2 == (7, 3)) and (diff_cheat == 6):
                        #    print(f'Adding to visited, t = {t}, diff_cheat = {diff_cheat}')

                        min_row = min(row0, row2)
                        max_row = max(row0, row2)
                        min_col = min(col0, col2)
                        max_col = max(col0, col2)
                        for r in range(min_row, max_row+1):
                            for c in range(min_col, max_col+1):
                                rc = (r, c)
                                if (rc != cheat2):
                                    visited.add((rc))
                        #if (cheat0 == S_pos) and (cheat2 == (7, 3)) and (diff_cheat == 6):
                        #    print("print_grid in BFS")
                        #    print_grid(grid_dict, MAX_ROW, MAX_COL, visited)
                        continue

                    # up
                    n_row = row-1
                    n_col = col
                    n_tuple = (n_row, n_col)
                    if (cheat_mode == 0) and (n_tuple == cheat0) and (cheat2 not in visited):
                        # Enter cheat mode
                        q.append((n_row, n_col, t+1))
                        cheat_mode = 1
                    elif (n_tuple != cheat0) and (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                        q.append((n_row, n_col, t+1))

                    # down
                    n_row = row+1
                    n_col = col
                    n_tuple = (n_row, n_col)
                    if (cheat_mode == 0) and (n_tuple == cheat0) and (cheat2 not in visited):
                        # Enter cheat mode
                        q.append((n_row, n_col, t+1))
                        cheat_mode = 1
                    elif (n_tuple != cheat0) and (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                        q.append((n_row, n_col, t+1))

                    # left
                    n_row = row
                    n_col = col-1
                    n_tuple = (n_row, n_col)
                    if (cheat_mode == 0) and (n_tuple == cheat0) and (cheat2 not in visited):
                        # Enter cheat mode
                        q.append((n_row, n_col, t+1))
                        cheat_mode = 1
                    elif (n_tuple != cheat0) and (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                        q.append((n_row, n_col, t+1))

                    # right
                    n_row = row
                    n_col = col+1
                    n_tuple = (n_row, n_col)
                    if (cheat_mode == 0) and (n_tuple == cheat0) and (cheat2 not in visited):
                        # Enter cheat mode
                        q.append((n_row, n_col, t+1))
                        cheat_mode = 1
                    elif (n_tuple != cheat0) and (n_tuple in grid_dict) and (grid_dict[n_tuple] != '#'):
                        q.append((n_row, n_col, t+1))

                # BFS while loop ended here
                #if (cheat0 == S_pos) and (cheat2 == (7, 3)) and (diff_cheat == 6):
                #    print("print_grid")
                #    print(t)
                #    for row in range(0, MAX_ROW+1):
                #        for col in range(0, MAX_COL+1):
                #            if ((row, col) in visited):
                #                print("O", end="")
                #            else:
                #                print(grid_dict[(row, col)], end="")
                #        print("")

                # Evaluate
                if (check == "example"):
                    if_check = ((max_t - t) == 50)
                else:
                    if_check = ((max_t - t) >= 100)
                if (found_exit) and if_check:
                    output += 1
                    #adj_cheat1 = (cheat1[0]+1, cheat1[1]+1)
                    #adj_cheat2 = (cheat2[0]+1, cheat2[1]+1)
                    #print(f'Cheat1: {adj_cheat1}, Cheat2: {adj_cheat2} to save {max_t-t}')
                    ## DEBUG
                    #for row in range(0, MAX_ROW+1):
                    #    for col in range(0, MAX_COL+1):
                    #        if ((row, col) == cheat1):
                    #            print('1', end="")
                    #        elif ((row, col) == cheat2):
                    #            print('2', end="")
                    #        elif ((row, col) in visited):
                    #            print('O', end="")
                    #        else:
                    #            print(grid_dict[(row, col)], end="")
                    #    print("")

                # Return the wall
                #grid_dict[cheat1] = old_tile1
                #grid_dict[cheat2] = old_tile2

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file, "example")
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
part1, part2 = process_inputs2(input_file, "input")

#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
