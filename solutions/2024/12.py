from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict, deque

input_file = "../../inputs/2024/input12.txt"

def part1(in_file):
    part1 = 0

    grid = []
    types_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_list = [l for l in line]
            grid.append(line_list)

            line = file.readline()

    # Check coordinates
    grid_dict = {}
    for row, rowline in enumerate(grid):
        for col, l in enumerate(rowline):
            types_dict[l].append((row, col))

            grid_dict[(row, col)] = l

    # BFS
    for l in types_dict:
        #print(l)
        visited = set()
        region_dict = defaultdict(list)
        perimeter_dict = defaultdict(int)
        for init_coord in types_dict[l]:
            if (init_coord in visited):
                continue

            q = deque()
            q.append(init_coord)
            perimeter = 0
            while (len(q)):
                row, col = q.popleft()

                if ((row, col) in visited):
                    continue
                visited.add((row, col))
                region_dict[init_coord].append((row, col))

                # up
                n_row = row-1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    #print(f'Up fence at {n_tuple}')

                # down
                n_row = row+1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    #print(f'Down fence at {n_tuple}')

                # left
                n_row = row
                n_col = col-1
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    #print(f'Left fence at {n_tuple}')

                # right
                n_row = row
                n_col = col+1
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    #print(f'Right fence at {n_tuple}')

            # Record perimeter
            perimeter_dict[init_coord] = perimeter

        # Compute area
        #if (l == 'I'):
        #    print(region_dict)
        for init_coord in region_dict:
            area = len(region_dict[init_coord])
            perimeter = perimeter_dict[init_coord]
            #print(area, perimeter)
            part1 += area*perimeter

    return part1

def vertical_scan(fences_list):
    MIN_ROW = 1000000
    MIN_COL = 1000000
    MAX_ROW = -100000
    MAX_COL = -100000
    for coords in fences_list:
        row, col = coords
    
        MIN_ROW = min(MIN_ROW, row)
        MIN_COL = min(MIN_COL, col)
        MAX_ROW = max(MAX_ROW, row)
        MAX_COL = max(MAX_COL, col)
    
    sides = 0
    for col in range(MIN_COL, MAX_COL+1):
        started_side = False
        for row in range(MIN_ROW, MAX_ROW+1):
            n_tuple = (row, col)
    
            if (started_side == False) and (n_tuple in fences_list):
                started_side = True
            elif (started_side) and (n_tuple not in fences_list):
                # Side has ended
                started_side = False
                sides += 1
    
        if (started_side):
            sides += 1

    return sides

def horizontal_scan(fences_list):
    MIN_ROW = 1000000
    MIN_COL = 1000000
    MAX_ROW = -100000
    MAX_COL = -100000
    for coords in fences_list:
        row, col = coords
    
        MIN_ROW = min(MIN_ROW, row)
        MIN_COL = min(MIN_COL, col)
        MAX_ROW = max(MAX_ROW, row)
        MAX_COL = max(MAX_COL, col)
    
    sides = 0
    for row in range(MIN_ROW, MAX_ROW+1):
        started_side = False
        for col in range(MIN_COL, MAX_COL+1):
            n_tuple = (row, col)
    
            if (started_side == False) and (n_tuple in fences_list):
                started_side = True
            elif (started_side) and (n_tuple not in fences_list):
                # Side has ended
                started_side = False
                sides += 1
    
        if (started_side):
            sides += 1

    return sides

def part2(in_file):
    part2 = 0

    grid = []
    types_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_list = [l for l in line]
            grid.append(line_list)

            line = file.readline()

    # Check coordinates
    grid_dict = {}
    for row, rowline in enumerate(grid):
        for col, l in enumerate(rowline):
            types_dict[l].append((row, col))

            grid_dict[(row, col)] = l

    # BFS
    for l in types_dict:
        #print(l)
        visited = set()
        region_dict = defaultdict(list)
        leftfences_dict = defaultdict(list)
        rightfences_dict = defaultdict(list)
        upfences_dict = defaultdict(list)
        downfences_dict = defaultdict(list)
        perimeter_dict = defaultdict(int)
        for init_coord in types_dict[l]:
            if (init_coord in visited):
                continue

            q = deque()
            q.append(init_coord)
            perimeter = 0
            while (len(q)):
                row, col = q.popleft()

                if ((row, col) in visited):
                    continue
                visited.add((row, col))
                region_dict[init_coord].append((row, col))

                # up
                n_row = row-1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    upfences_dict[init_coord].append(n_tuple)
                    #print(f'Up fence at {n_tuple}')

                # down
                n_row = row+1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    downfences_dict[init_coord].append(n_tuple)
                    #print(f'Down fence at {n_tuple}')

                # left
                n_row = row
                n_col = col-1
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    leftfences_dict[init_coord].append(n_tuple)
                    #print(f'Left fence at {n_tuple}')

                # right
                n_row = row
                n_col = col+1
                n_tuple = (n_row, n_col)
                if (n_tuple in grid_dict) and (n_tuple not in visited) and (grid_dict[n_tuple] == l):
                    q.append(n_tuple)
                elif (n_tuple not in grid_dict) or (grid_dict[n_tuple] != l):
                    # Found a fence
                    perimeter += 1
                    rightfences_dict[init_coord].append(n_tuple)
                    #print(f'Right fence at {n_tuple}')

            # Record perimeter
            perimeter_dict[init_coord] = perimeter

        # Compute area
        #if (l == 'O'):
        #    print(upfences_dict)
        #    print(downfences_dict)
        #    print(leftfences_dict)
        #    print(rightfences_dict)
        for init_coord in region_dict:
            area = len(region_dict[init_coord])

            # Compute sides
            upfences_list = upfences_dict[init_coord]
            downfences_list = downfences_dict[init_coord]
            leftfences_list = leftfences_dict[init_coord]
            rightfences_list = rightfences_dict[init_coord]
            sides = 0

            # Vertical scan
            leftsides = vertical_scan(leftfences_list)
            rightsides = vertical_scan(rightfences_list)

            # Horizontal scan
            upsides = horizontal_scan(upfences_list)
            downsides = horizontal_scan(downfences_list)

            sides = upsides + downsides + leftsides + rightsides
            sides_tuple = (upsides, downsides, leftsides, rightsides)
            #print(area, sides, sides_tuple)
            part2 += area*sides

    return part2

part1 = part1(input_file)
part2 = part2(input_file)

print("")
print("--- Advent of Code 2024 Day 12: Garden Groups ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
