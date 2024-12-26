input_file = "input6.txt"
example_file = "example6.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
dir_list = ["up", "right", "down", "left"]
def process_inputs(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append(line)

            line = file.readline()

    for idx, row in enumerate(grid):
        for idx_col, col in enumerate(row):
            if (col == '^'):
                INIT_GUARD = (idx, idx_col)

    # BFS
    direction = "up"
    dir_idx = 0
    init_step = [INIT_GUARD[0], INIT_GUARD[1]]
    queue = []
    queue.append(init_step)
    visited = []
    end_guard = False
    MAX_ROW = len(grid) - 1
    MAX_COL = len(grid[0]) - 1
    print(f'INIT_GUARD = {INIT_GUARD[0]}, {INIT_GUARD[1]}')
    print(f'MAX_COL, MAX_ROW = {MAX_COL}, {MAX_ROW}')

    count = 1
    while queue:
        row, col = queue.pop(0)
        v_tuple = (row, col)
        print(f'Position: {row}, {col}')
        visited.append(v_tuple)

        if (direction == "up"):
            n_col = col
            n_row = row - 1

            if (n_row < 0):
                end_guard = True
        elif (direction == "down"):
            n_col = col
            n_row = row + 1

            if (n_row > MAX_ROW):
                end_guard = True
        elif (direction == "left"):
            n_col = col - 1
            n_row = row

            if (n_col < 0):
                end_guard = True
        elif (direction == "right"):
            n_col = col + 1
            n_row = row

            if (n_col > MAX_COL):
                end_guard = True

        if (end_guard):
            print(f'Guard exited at {n_row}, {n_col}')
            break

        if (grid[n_row][n_col] != '#'):
            queue.append([n_row, n_col])
            count += 1
        else:
            # readd current position and move direction
            queue.append([row, col])
            dir_idx = (dir_idx+1)%4

        # Update
        direction = dir_list[dir_idx]

    output = len(set(visited))
    for v in visited:
        print(v)
    #output = count + 1

    return output

def process_inputs2(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append(line)

            line = file.readline()

    for idx, row in enumerate(grid):
        for idx_col, col in enumerate(row):
            if (col == '^'):
                INIT_GUARD = (idx, idx_col)

    # BFS
    MAX_ROW = len(grid) - 1
    MAX_COL = len(grid[0]) - 1
    print(f'INIT_GUARD = {INIT_GUARD[0]}, {INIT_GUARD[1]}')
    print(f'MAX_COL, MAX_ROW = {MAX_COL}, {MAX_ROW}')

    count = 0
    for idx_r, hor in enumerate(grid):
        for idx_c, vert in enumerate(hor):
            # Add obstacle
            if (vert == '.'):
                hor_list = list(hor)
                hor_list[idx_c] = '#'
                grid[idx_r] = ''.join(hor_list)
                #print("Adding obstacle")
                #print(hor)
                #print(grid[idx_r])
                added_obstacle = True
            else:
                added_obstacle = False

            # Go through map
            direction = "up"
            dir_idx = 0
            init_step = [INIT_GUARD[0], INIT_GUARD[1]]
            queue = []
            queue.append(init_step)
            visited = set()
            end_guard = False
            while queue:
                row, col = queue.pop(0)
                v_tuple = (row, col, direction)

                # Check if already visited
                if (v_tuple in visited):
                    count += 1
                    break

                #print(f'Position: {row}, {col}')
                visited.add(v_tuple)

                if (direction == "up"):
                    n_col = col
                    n_row = row - 1

                    if (n_row < 0):
                        end_guard = True
                elif (direction == "down"):
                    n_col = col
                    n_row = row + 1

                    if (n_row > MAX_ROW):
                        end_guard = True
                elif (direction == "left"):
                    n_col = col - 1
                    n_row = row

                    if (n_col < 0):
                        end_guard = True
                elif (direction == "right"):
                    n_col = col + 1
                    n_row = row

                    if (n_col > MAX_COL):
                        end_guard = True

                if (end_guard):
                    #print(f'Guard exited at {n_row}, {n_col}')
                    break

                if (grid[n_row][n_col] != '#'):
                    queue.append([n_row, n_col])
                else:
                    # readd current position and move direction
                    queue.append([row, col])
                    dir_idx = (dir_idx+1)%4

                # Update
                direction = dir_list[dir_idx]

            # Remove obstacle
            if (added_obstacle):
                grid[idx_r] = hor

    output = count

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
