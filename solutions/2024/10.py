from collections import deque

input_file = "../../inputs/2024/input10.txt"
example_file = "example10.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
   
        while line:
            line = line.strip()

            line_int = [int(x) for x in line]
            grid.append(line_int)

            line = file.readline()

    # Trailheads
    th_list = []
    zero_list = []
    for row, rowline in enumerate(grid):
        for col, tile in enumerate(rowline):
            if (tile == 9):
                th_list.append([row, col])
            elif (tile == 0):
                zero_list.append([row, col])

    # Modify zeros
    for zero in zero_list:
        z_row, z_col = zero
        grid[z_row][z_col] = 9

    # BFS
    MAX_ROW = len(grid)-1
    MAX_COL = len(grid[0])-1
    for zero in zero_list:
        z_row, z_col = zero
        # Return back zero
        grid[z_row][z_col] = 0

        # Trailheads
        for th in th_list:
            th_row, th_col = th

            queue = deque()
            visited = set()
            queue.append((th_row, th_col))
            TH_FOUND = False
            while (len(queue)):
                row, col = queue.popleft()
                visited.add((row, col))

                tile = grid[row][col]
                if (tile == 0):
                    TH_FOUND = True
                    break

                # left
                n_row = row
                n_col = col-1
                n_tuple = (n_row, n_col)
                if (n_col >= 0):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)
                # up
                n_row = row - 1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_row >= 0):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)
                # right
                n_row = row
                n_col = col + 1
                n_tuple = (n_row, n_col)
                if (n_col <= MAX_COL):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)
                # down
                n_row = row+1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_row <= MAX_ROW):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)

            if (TH_FOUND):
                output += 1

        # Modify again
        grid[z_row][z_col] = 9

    return output

def process_inputs2(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_int = [int(x) for x in line]
            grid.append(line_int)

            line = file.readline()

    # Trailheads
    th_list = []
    zero_list = []
    for row, rowline in enumerate(grid):
        for col, tile in enumerate(rowline):
            if (tile == 9):
                th_list.append([row, col])
            elif (tile == 0):
                zero_list.append([row, col])

    # Modify zeros since later on it will be returned back
    #   one at a time so that only 1 trailhead can be seen in 1 BFS run
    for zero in zero_list:
        z_row, z_col = zero
        grid[z_row][z_col] = 9

    # BFS
    MAX_ROW = len(grid)-1
    MAX_COL = len(grid[0])-1
    rating = 0
    part1 = 0
    for zero in zero_list:
        z_row, z_col = zero
        # Return back zero
        grid[z_row][z_col] = 0

        # Trailheads
        # Traverse starting in reverse from 9 instead of 0,
        #   doesn't seem to matter though, this was just based on an initial prediction
        #   of possible Part 2 while I was solving Part 1
        for th in th_list:
            th_row, th_col = th

            queue = deque()
            visited = set()
            queue.append((th_row, th_col))
            TH_FOUND = False
            while (len(queue)):
                row, col = queue.popleft()
                visited.add((row, col))

                tile = grid[row][col]
                if (tile == 0):
                    rating += 1
                    if not (TH_FOUND):
                        part1 += 1
                        TH_FOUND = True

                # left
                n_row = row
                n_col = col-1
                n_tuple = (n_row, n_col)
                if (n_col >= 0):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)
                # up
                n_row = row - 1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_row >= 0):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)
                # right
                n_row = row
                n_col = col + 1
                n_tuple = (n_row, n_col)
                if (n_col <= MAX_COL):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)
                # down
                n_row = row+1
                n_col = col
                n_tuple = (n_row, n_col)
                if (n_row <= MAX_ROW):
                    n_tile = grid[n_row][n_col]
                    if (n_tile == (tile-1)):
                        queue.append(n_tuple)

        # Modify again
        grid[z_row][z_col] = 9

    output = rating

    return part1, output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part1, part2 = process_inputs2(input_file)

#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
