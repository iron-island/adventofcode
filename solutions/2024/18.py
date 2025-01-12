from collections import deque

input_file = "../../inputs/2024/input18.txt"
example_file = "example18.txt"
example2_file = "example18_2.txt"
example3_file = "example18_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

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

def process_inputs(in_file, MAX_ROW, MAX_COL, MAX_LEN):
    output = 0

    coords_list = []
    grid_dict = defaultdict(list)
    length = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            coords = [int(x) for x in line.split(",")]
            coords_list.append(coords)
            x, y = coords
            if (length < MAX_LEN):
                grid_dict[(y, x)] = '#'
                length += 1

            line = file.readline()

    # BFS
    q = deque()
    q.append([0, 0, 0])
    visited = set()

    steps = 0
    while (len(q)):
        row, col, steps = q.popleft()

        if (MAX_ROW, MAX_COL) == (row, col):
            #print("BREAK!")
            visited.add((row, col))
            #steps += 1
            break

        if ((row, col) in visited):
            continue

        visited.add((row, col))

        # up
        n_row = row-1
        n_col = col
        n_tuple = (n_row, n_col)
        n_list = [n_row, n_col, steps+1]
        if (n_tuple not in grid_dict) and (n_row >= 0):
            q.append(n_list)

            #if (n_tuple == (4, 6)):
            #    print("up")

        # down
        n_row = row+1
        n_col = col
        n_tuple = (n_row, n_col)
        n_list = [n_row, n_col, steps+1]
        if (n_tuple not in grid_dict) and (n_row <= MAX_ROW):
            q.append(n_list)
            #if (n_tuple == (4, 6)):
            #    print("down")

        # left
        n_row = row
        n_col = col-1
        n_tuple = (n_row, n_col)
        n_list = [n_row, n_col, steps+1]
        if (n_tuple not in grid_dict) and (n_col >= 0):
            q.append(n_list)
            #if (n_tuple == (4, 6)):
            #    print("left")

        # right
        n_row = row
        n_col = col+1
        n_tuple = (n_row, n_col)
        n_list = [n_row, n_col, steps+1]
        if (n_tuple not in grid_dict) and (n_col <= MAX_COL):
            q.append(n_list)
            #if (n_tuple == (4, 6)):
            #    print("right")

    output = steps
    #print(visited)

    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        if ((row, col) in grid_dict):
    #            print("#", end="")
    #        elif (row, col) in visited:
    #            print("O", end="")
    #        else:
    #            print(".", end="")

    #    print("")

    return output

def process_inputs2(in_file, MAX_ROW, MAX_COL, MAX_LEN):
    output = 0

    coords_list = []
    grid_dict = defaultdict(list)
    length = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            coords = [int(x) for x in line.split(",")]
            x, y = coords
            coords_list.append([y, x])
            grid_dict[(y, x)] = '#'
            length += 1

            line = file.readline()

    # Loop through lengths
    new_coords_list = deque()
    coords_list.reverse()
    for coords in coords_list:
        y, x = coords
        new_coords_list.append((y, x))
    for idx, coords in enumerate(coords_list):
        #if (idx % 100) == 0:
        #    print(f'Trial {idx} of {len(coords_list)-1}')
        #y, x = coords
        #new_coords_list.append((y, x))
        new_coords_list.popleft()

        # BFS
        q = deque()
        q.append([0, 0, 0])
        visited = set()

        steps = 0
        exit_found = False
        while (len(q)):
            row, col, steps = q.popleft()

            if (MAX_ROW, MAX_COL) == (row, col):
                visited.add((row, col))
                exit_found = True
                break

            if ((row, col) in visited):
                continue

            visited.add((row, col))

            # up
            n_row = row-1
            n_col = col
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_row >= 0):
                q.append(n_list)

                #if (n_tuple == (4, 6)):
                #    print("up")

            # down
            n_row = row+1
            n_col = col
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_row <= MAX_ROW):
                q.append(n_list)
                #if (n_tuple == (4, 6)):
                #    print("down")

            # left
            n_row = row
            n_col = col-1
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_col >= 0):
                q.append(n_list)
                #if (n_tuple == (4, 6)):
                #    print("left")

            # right
            n_row = row
            n_col = col+1
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_col <= MAX_COL):
                q.append(n_list)
                #if (n_tuple == (4, 6)):
                #    print("right")
    
        #if (exit_found == False):
        #    y, x = coords
        #    output = f'{x},{y}'
        #    break
        if (exit_found):
            y, x = coords
            #print(f'{len(coords_list)-idx-1}')
            output = f'{x},{y}'
            break

    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        if ((row, col) in grid_dict):
    #            print("#", end="")
    #        elif (row, col) in visited:
    #            print("O", end="")
    #        else:
    #            print(".", end="")

    #    print("")

    return output

def process_inputs_part1_2(in_file):
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

    # Loop through lengths
    new_coords_list = deque()
    coords_list.reverse()
    for coords in coords_list:
        y, x = coords
        new_coords_list.append((y, x))
    for idx, coords in enumerate(coords_list):
        #if (idx % 100) == 0:
        #    print(f'Trial {idx} of {len(coords_list)-1}')
        #y, x = coords
        #new_coords_list.append((y, x))
        new_coords_list.popleft()

        # BFS
        q = deque()
        q.append([0, 0, 0])
        visited = set()

        steps = 0
        exit_found = False
        while (len(q)):
            row, col, steps = q.popleft()

            if (MAX_ROW, MAX_COL) == (row, col):
                visited.add((row, col))
                exit_found = True
                break

            if ((row, col) in visited):
                continue

            visited.add((row, col))

            # up
            n_row = row-1
            n_col = col
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_row >= 0):
                q.append(n_list)

                #if (n_tuple == (4, 6)):
                #    print("up")

            # down
            n_row = row+1
            n_col = col
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_row <= MAX_ROW):
                q.append(n_list)
                #if (n_tuple == (4, 6)):
                #    print("down")

            # left
            n_row = row
            n_col = col-1
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_col >= 0):
                q.append(n_list)
                #if (n_tuple == (4, 6)):
                #    print("left")

            # right
            n_row = row
            n_col = col+1
            n_tuple = (n_row, n_col)
            n_list = [n_row, n_col, steps+1]
            if (n_tuple not in new_coords_list) and (n_col <= MAX_COL):
                q.append(n_list)
                #if (n_tuple == (4, 6)):
                #    print("right")
    
        #if (exit_found == False):
        #    y, x = coords
        #    output = f'{x},{y}'
        #    break
        if (exit_found):
            y, x = coords
            #print(f'{len(coords_list)-idx-1}')
            output = f'{x},{y}'
            break

    return part1, output

#part1_example = process_inputs(example_file, 6, 6, 12)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
#part1 = process_inputs(input_file, 70, 70, 1024)

#part2_example = process_inputs2(example_file, 6, 6, 12)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
#part2 = process_inputs2(input_file, 70, 70, 1024)

part1, part2 = process_inputs_part1_2(input_file)

print("")
print("--- Advent of Code 2024 Day 18: RAM Run ---")
#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
