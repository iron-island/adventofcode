from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input08.txt"

def part1(in_file):
    part1 = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append(line)

            line = file.readline()

    MAX_ROW = len(grid) - 1
    MAX_COL = len(grid[0]) - 1

    ant_dict = {}
    for row, rowline in enumerate(grid):
        for col, colchar in enumerate(rowline):
            if (colchar != '.'):
                if (colchar not in ant_dict):
                    ant_dict[colchar] = []
                ant_dict[colchar].append([row, col])

    # Get antinodes
    antinode_dict = {}
    antinode_loc_list = []
    for ant in ant_dict:
        loc_list = ant_dict[ant]

        antinode_dict[ant] = []
        for idx1, loc in enumerate(loc_list):
            for idx2 in range(idx1+1, len(loc_list)):
                # Compute distances
                row1, col1 = loc
                row2, col2 = loc_list[idx2]

                diff_row = row2 - row1
                diff_col = col2 - col1
                absdiff_row = abs(diff_row)
                absdiff_col = abs(diff_col)

                #if (absdiff_row >= 2*absdiff_col) or (absdiff_col >= 2*absdiff_row):
                if (True):
                    if (row2 < row1) and (col2 > col1): # upper right 
                        antinode_row2 = row2 - absdiff_row
                        antinode_col2 = col2 + absdiff_col

                        antinode_row1 = row1 + absdiff_row
                        antinode_col1 = col1 - absdiff_col
                    elif (row2 > row1) and (col2 > col1): # lower right
                        antinode_row2 = row2 + absdiff_row
                        antinode_col2 = col2 + absdiff_col

                        antinode_row1 = row1 - absdiff_row
                        antinode_col1 = col1 - absdiff_col
                    elif (row2 > row1) and (col2 < col1): # lower left
                        antinode_row2 = row2 + absdiff_row
                        antinode_col2 = col2 - absdiff_col

                        antinode_row1 = row1 - absdiff_row
                        antinode_col1 = col1 + absdiff_col
                    elif (row2 < row1) and (col2 < col1): # upper left
                        antinode_row2 = row2 - absdiff_row
                        antinode_col2 = col2 - absdiff_col

                        antinode_row1 = row1 + absdiff_row
                        antinode_col1 = col1 + absdiff_col

                    tuple1 = (antinode_row1, antinode_col1)
                    tuple2 = (antinode_row2, antinode_col2)

                    if (antinode_row1 <= MAX_ROW) and (antinode_row1 >= 0) and (antinode_col1 <= MAX_COL) and (antinode_col1 >= 0):
                        antinode_dict[ant].append((antinode_row1, antinode_col1))
                        antinode_loc_list.append((antinode_row1, antinode_col1))
                    if (antinode_row2 <= MAX_ROW) and (antinode_row2 >= 0) and (antinode_col2 <= MAX_COL) and (antinode_col2 >= 0):
                        antinode_dict[ant].append((antinode_row2, antinode_col2))
                        antinode_loc_list.append((antinode_row2, antinode_col2))

    # Evaluate
    part1 = len(set(antinode_loc_list))

    return part1

def part2(in_file):
    part2 = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append(line)

            line = file.readline()

    MAX_ROW = len(grid) - 1
    MAX_COL = len(grid[0]) - 1

    ant_dict = {}
    for row, rowline in enumerate(grid):
        for col, colchar in enumerate(rowline):
            if (colchar != '.'):
                if (colchar not in ant_dict):
                    ant_dict[colchar] = []
                ant_dict[colchar].append([row, col])

    # Get antinodes
    antinode_dict = {}
    antinode_loc_list = []
    for ant in ant_dict:
        loc_list = ant_dict[ant]

        antinode_dict[ant] = []
        for idx1, loc in enumerate(loc_list):
            for idx2 in range(idx1+1, len(loc_list)):
                # Compute distances
                row1, col1 = loc
                row2, col2 = loc_list[idx2]

                diff_row = row2 - row1
                diff_col = col2 - col1
                absdiff_row = abs(diff_row)
                absdiff_col = abs(diff_col)

                #if (absdiff_row >= 2*absdiff_col) or (absdiff_col >= 2*absdiff_row):
                if (True):
                    if (row2 < row1) and (col2 > col1): # upper right 
                        antinode_rowdiff2 = - absdiff_row
                        antinode_coldiff2 = + absdiff_col

                        antinode_rowdiff1 = + absdiff_row
                        antinode_coldiff1 = - absdiff_col
                    elif (row2 > row1) and (col2 > col1): # lower right
                        antinode_rowdiff2 = + absdiff_row
                        antinode_coldiff2 = + absdiff_col

                        antinode_rowdiff1 = - absdiff_row
                        antinode_coldiff1 = - absdiff_col
                    elif (row2 > row1) and (col2 < col1): # lower left
                        antinode_rowdiff2 = + absdiff_row
                        antinode_coldiff2 = - absdiff_col

                        antinode_rowdiff1 = - absdiff_row
                        antinode_coldiff1 = + absdiff_col
                    elif (row2 < row1) and (col2 < col1): # upper left
                        antinode_rowdiff2 = - absdiff_row
                        antinode_coldiff2 = - absdiff_col

                        antinode_rowdiff1 = + absdiff_row
                        antinode_coldiff1 = + absdiff_col

                    init_row = row1
                    init_col = col1
                    while (True):
                        # Compute antinodes
                        antinode_row1 = init_row + antinode_rowdiff1 
                        antinode_col1 = init_col + antinode_coldiff1

                        if (antinode_row1 <= MAX_ROW) and (antinode_row1 >= 0) and (antinode_col1 <= MAX_COL) and (antinode_col1 >= 0):
                            antinode_dict[ant].append((antinode_row1, antinode_col1))
                            antinode_loc_list.append((antinode_row1, antinode_col1))
                            init_row = antinode_row1
                            init_col = antinode_col1
                        else:
                            break
                    init_row = row2
                    init_col = col2
                    while (True): 
                        # Compute antinodes
                        antinode_row2 = init_row + antinode_rowdiff2 
                        antinode_col2 = init_col + antinode_coldiff2

                        if (antinode_row2 <= MAX_ROW) and (antinode_row2 >= 0) and (antinode_col2 <= MAX_COL) and (antinode_col2 >= 0):
                            antinode_dict[ant].append((antinode_row2, antinode_col2))
                            antinode_loc_list.append((antinode_row2, antinode_col2))
                            init_row = antinode_row2
                            init_col = antinode_col2
                        else:
                            break

    # Evaluate
    antinode_loc_set = set(antinode_loc_list)
    for ant in ant_dict:
        loc_list = ant_dict[ant]

        for loc in loc_list:
            row, col = loc
            loc_tuple = (row, col)
            antinode_loc_set.add(loc_tuple)
    part2 = len(antinode_loc_set)

    return part2

part1 = part1(input_file)
part2 = part2(input_file)

print("")
print("--- Advent of Code 2024 Day 8: Resonant Collinearity ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
