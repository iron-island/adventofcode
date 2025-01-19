from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input04.txt"

def part1(in_file):
    part1 = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append(line)

            line = file.readline()

    # Go through grid
    # horizontal
    hor = 0
    hor_reverse = 0
    for line in grid:
        hor += line.count("XMAS")
        hor_reverse += line.count("SAMX")
    part1 += hor + hor_reverse

    # vertical
    column = ""
    vert = 0
    vert_reverse = 0
    MAX_COL = len(line)-1
    for col in range(0, MAX_COL+1):
        column = ""
        for line in grid:
            column = column + line[col]

        vert += column.count("XMAS")
        vert_reverse += column.count("SAMX")
    part1 += vert + vert_reverse

    # diagonal
    MAX_ROW = len(grid) - 1
    diag1 = 0
    diag2 = 0
    diag3 = 0
    diag4 = 0
    for col in range(0, MAX_COL+1):
        for row in range(0, MAX_ROW+1):
            c = grid[row][col]

            # down to up diagonal /
            if (row >= 3) and (col <= (MAX_COL - 3)):
                if (c == "X") and (grid[row-1][col+1] == "M") and (grid[row-2][col+2] == "A") and (grid[row-3][col+3] == "S"):
                    part1 += 1
                    diag1 += 1

            # \ diagonal
            if (row >= 3) and (col >= 3):
                if (c == "X") and (grid[row-1][col-1] == "M") and (grid[row-2][col-2] == "A") and (grid[row-3][col-3] == "S"):
                    part1 += 1
                    diag2 += 1

            # up to down diagonal \
            if (row <= (MAX_ROW - 3)) and (col <= (MAX_COL - 3)):
                if (c == "X") and (grid[row+1][col+1] == "M") and (grid[row+2][col+2] == "A") and (grid[row+3][col+3] == "S"):
                    part1 += 1
                    diag3 += 1

            # / diagonal
            if (row <= (MAX_ROW - 3)) and (col >= 3):
                if (c == "X") and (grid[row+1][col-1] == "M") and (grid[row+2][col-2] == "A") and (grid[row+3][col-3] == "S"):
                    part1 += 1
                    diag4 += 1

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

    # Go through grid
    # horizontal
    hor = 0
    hor_reverse = 0
    for line in grid:
        hor += line.count("XMAS")
        hor_reverse += line.count("SAMX")
    part2 += hor + hor_reverse

    # vertical
    column = ""
    vert = 0
    vert_reverse = 0
    MAX_COL = len(line)-1
    for col in range(0, MAX_COL+1):
        column = ""
        for line in grid:
            column = column + line[col]

        vert += column.count("XMAS")
        vert_reverse += column.count("SAMX")
    part2 += vert + vert_reverse

    # diagonal
    part2 = 0
    MAX_ROW = len(grid) - 1
    diag1 = 0
    diag2 = 0
    diag3 = 0
    diag4 = 0
    for col in range(0, MAX_COL+1):
        for row in range(0, MAX_ROW+1):
            c = grid[row][col]

            if (row >= 1) and (row <= (MAX_ROW - 1)) and (col >= 1) and (col <= (MAX_COL - 1)):
                if (c == "A"):
                    if (grid[row-1][col-1] == "M") and (grid[row+1][col+1] == "S"):
                        # M M
                        #  A
                        # S S
                        if (grid[row-1][col+1] == "M") and (grid[row+1][col-1] == "S"):
                            part2 += 1
                        # M S
                        #  A
                        # M S
                        elif (grid[row-1][col+1] == "S") and (grid[row+1][col-1] == "M"):
                            part2 += 1
                    elif (grid[row-1][col-1] == "S") and (grid[row+1][col+1] == "M"):
                        # S M
                        #  A
                        # S M
                        if (grid[row-1][col+1] == "M") and (grid[row+1][col-1] == "S"):
                            part2 += 1
                        # S S
                        #  A
                        # M M
                        elif (grid[row-1][col+1] == "S") and (grid[row+1][col-1] == "M"):
                            part2 += 1

    return part2

part1 = part1(input_file)
part2 = part2(input_file)

print("")
print("--- Advent of Code 2024 Day 4: Ceres Search ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
