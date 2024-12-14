import re
input_file = "input10.txt"
#input_file = "input10_modified.txt"
#input_file = "input10_padded.txt"
example_file = "example10.txt"
example_file = "example10_3.txt" # 4 inside
example_file = "example10_4.txt" # 8 inside
#example_file = "example10_5.txt" # 10 inside

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

# Parsing numbers into list of strings from line
# number_list = re.findall(r'[+-]?\d+', line)

#| is a vertical pipe connecting north and south.
#- is a horizontal pipe connecting east and west.
#L is a 90-degree bend connecting north and east.
#J is a 90-degree bend connecting north and west.
#7 is a 90-degree bend connecting south and west.
#F is a 90-degree bend connecting south and east.

up_list = ['|', 'F', '7']
down_list = ['|', 'L', 'J']
left_list = ['-', 'L', 'F']
right_list = ['-', 'J', '7']

curr_up_list = down_list
curr_down_list = up_list
curr_left_list = right_list
curr_right_list = left_list

def process_inputs(in_file):
    grid = [] # row, column
    output = 0

    start = 0
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            grid.append(line)

            for col, l in enumerate(line):
                if (l == 'S'):
                    start = (row, col)

            line = file.readline()
            row += 1

    s_row, s_col = start

    # BFS
    queue = []
    visited = []

    q_row, q_col = start
    # up
    if (q_row > 0):
        up = grid[q_row - 1][q_col]
        if not ((up == '-') or (up == 'L') or (up == 'J') or (up == 'S') or (up == '.')):
            #grid[q_row - 1][q_col] = '.'
            queue.append((q_row-1, q_col))
    # down
    if (q_row < (len(grid)-1)):
        down = grid[q_row+1][q_col]
        if not ((down == '-') or (down == '7') or (down == 'F') or (down == 'S') or (down == '.')):
            #grid[q_row+1][q_col] = '.'
            queue.append((q_row+1, q_col))
    # left
    if (q_col > 0):
        left = grid[q_row][q_col-1]
        if not ((left == '|') or (left == 'J') or (left == '7') or (left == 'S') or (left == '.')):
            #grid[q_row][q_col-1] = '.'
            queue.append((q_row, q_col-1))
    # right
    if (q_col < (len(grid[0])-1)):
        right = grid[q_row][q_col+1]
        if not ((right == '|') or (right == 'L') or (right == 'F') or (right == 'S') or (right == '.')):
            #grid[q_row][q_col+1] = '.' 
            queue.append((q_row, q_col+1))
    visited.append(start)
    while len(queue):
        q = queue.pop(0)
        q_row, q_col = q

        if (q in visited):
            continue

        curr = grid[q_row][q_col]

        #print(f'curr: {q_row}, {q_col}')
        #print(f'old queue: {queue}')

        # up
        if (curr in curr_up_list):
            up = grid[q_row - 1][q_col]
            if (up in up_list):
                queue.append((q_row-1, q_col))
        # down
        if (curr in curr_down_list):
            down = grid[q_row+1][q_col]
            if (down in down_list):
                queue.append((q_row+1, q_col))
        # left
        if (curr in curr_left_list):
            left = grid[q_row][q_col-1]
            if (left in left_list):
                queue.append((q_row, q_col-1))
        # right
        if (curr in curr_right_list):
            right = grid[q_row][q_col+1]
            if (right in right_list):
                queue.append((q_row, q_col+1))
        
        #print(f'new queue: {queue}')

        visited.append(q)

    print(visited)
    #print(len(visited))

    output = len(visited)/2

    return output

def process_inputs2(in_file):
    grid = [] # row, column
    output = 0

    start = 0
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            grid.append(line)

            for col, l in enumerate(line):
                if (l == 'S'):
                    start = (row, col)

            line = file.readline()
            row += 1

    s_row, s_col = start

    # BFS
    queue = []
    visited = []

    q_row, q_col = start
    # up
    if (q_row > 0):
        up = grid[q_row - 1][q_col]
        if not ((up == '-') or (up == 'L') or (up == 'J') or (up == 'S') or (up == '.')):
            #grid[q_row - 1][q_col] = '.'
            queue.append((q_row-1, q_col))
    # down
    if (q_row < (len(grid)-1)):
        down = grid[q_row+1][q_col]
        if not ((down == '-') or (down == '7') or (down == 'F') or (down == 'S') or (down == '.')):
            #grid[q_row+1][q_col] = '.'
            queue.append((q_row+1, q_col))
    # left
    if (q_col > 0):
        left = grid[q_row][q_col-1]
        if not ((left == '|') or (left == 'J') or (left == '7') or (left == 'S') or (left == '.')):
            #grid[q_row][q_col-1] = '.'
            queue.append((q_row, q_col-1))
    # right
    if (q_col < (len(grid[0])-1)):
        right = grid[q_row][q_col+1]
        if not ((right == '|') or (right == 'L') or (right == 'F') or (right == 'S') or (right == '.')):
            #grid[q_row][q_col+1] = '.' 
            queue.append((q_row, q_col+1))
    visited.append(start)
    while len(queue):
        q = queue.pop(0)
        q_row, q_col = q

        if (q in visited):
            continue

        curr = grid[q_row][q_col]

        #print(f'curr: {q_row}, {q_col}')
        #print(f'old queue: {queue}')

        # up
        if (curr in curr_up_list):
            up = grid[q_row - 1][q_col]
            if (up in up_list):
                queue.append((q_row-1, q_col))
        # down
        if (curr in curr_down_list):
            down = grid[q_row+1][q_col]
            if (down in down_list):
                queue.append((q_row+1, q_col))
        # left
        if (curr in curr_left_list):
            left = grid[q_row][q_col-1]
            if (left in left_list):
                queue.append((q_row, q_col-1))
        # right
        if (curr in curr_right_list):
            right = grid[q_row][q_col+1]
            if (right in right_list):
                queue.append((q_row, q_col+1))
        
        #print(f'new queue: {queue}')

        visited.append(q)

    # BFS across outside of loop first
    loop_edge = []
    o_visited = []
    o_queue = []

    not_loop = []

    not_in_loop = 0
    total_tiles = 0
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            total_tiles += 1
            if ((r, c) not in visited):
                #o_queue.append((r, c))
                not_in_loop += 1
    #            #print(".", end="")
    #        #else:
    #        #    print(grid[r][c],end="")
    #    #print("")
    last_r = len(grid)-1
    last_c = len(grid[0])-1
    # hardcoded based on input
    o_queue.append((0, 0))
    o_queue.append((0, last_c))
    o_queue.append((last_r, 0))
    o_queue.append((last_r, last_c))
    print(f'Total tiles: {total_tiles}')
    print(f'Tiles in the loop: {len(visited)}')
    print(f'Tiles not in the loop: {not_in_loop}')

    while len(o_queue):
        q = o_queue.pop(0)
        q_row, q_col = q

        if q in o_visited:
            continue

        # if not in loop, not already visited, and not in queue, don't add to queue
        # up
        if (q_row > 0):
            if (q_row-1, q_col) not in visited and ( (q_row-1, q_col) not in o_visited) and ( (q_row-1, q_col) not in o_queue):
                o_queue.append((q_row-1, q_col))
            elif (q_row-1, q_col) in visited:
                loop_edge.append((q_row-1, q_col))
        # down
        if (q_row < (len(grid)-1)):
            if (q_row+1, q_col) not in visited and ( (q_row+1, q_col) not in o_visited) and ( (q_row+1, q_col) not in o_queue):
                o_queue.append((q_row+1, q_col))
            elif (q_row+1, q_col) in visited:
                loop_edge.append((q_row+1, q_col))
        # left
        if (q_col > 0):
            if (q_row, q_col-1) not in visited and ( (q_row, q_col-1) not in o_visited) and ( (q_row, q_col-1) not in o_queue):
                o_queue.append((q_row, q_col-1))
            elif (q_row, q_col-1) in visited:
                loop_edge.append((q_row, q_col-1))
        # right
        if (q_col < (len(grid[0])-1)):
            if (q_row, q_col+1) not in visited and ( (q_row, q_col+1) not in o_visited) and ( (q_row, q_col+1) not in o_queue):
                o_queue.append((q_row, q_col+1))
            elif (q_row, q_col+1) in visited:
                loop_edge.append((q_row, q_col+1))

        o_visited.append(q)

    # if smallest distance to o_visited is odd: tile is inside
    # else, tile is outside
    io = []
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            if ((r, c) not in visited) and ((r, c) not in o_visited):
                io.append((r, c))

    inside = 0
    inside_tiles = []
    print(len(io))
    for idx, tile in enumerate(io):
        t_row, t_col = tile
        io_queue = []
        io_visited = []
        distance = 0

        print(f'Tile {idx}/{len(io)}: ({t_row}, {t_col})')

        io_queue.append((t_row, t_col, distance))
        while len(io_queue):
            q = io_queue.pop(0)
            q_row, q_col, distance = q

            if q in io_visited:
                continue

            # up
            if (q_row > 0):
                up_row = q_row - 1
                up_col = q_col
                if ((up_row, up_col) not in o_visited):
                    if ((up_row, up_col) in visited):
                        io_queue.append((up_row, up_col, distance+1))
                    else:
                        io_queue.append((up_row, up_col, distance))
                else:
                    if ((distance+1) % 2) == 0:
                        inside += 1
                        inside_tiles.append(tile)
                    #print(f'up: {up_row}, {up_col}, {distance}')
                    break
            # down
            if (q_row < last_r):
                down_row = q_row + 1
                down_col = q_col
                if (down_row, down_col) not in o_visited:
                    if (down_row, down_col) in visited:
                        io_queue.append((down_row, down_col, distance+1))
                    else:
                        io_queue.append((down_row, down_col, distance))
                else:
                    if ((distance+1) % 2) == 0:
                        inside += 1
                        inside_tiles.append(tile)
                    break
            # left
            if (q_col > 0):
                left_row = q_row
                left_col = q_col - 1
                if (left_row, left_col) not in o_visited:
                    if (left_row, left_col) in visited:
                        io_queue.append((left_row, left_col, distance+1))
                    else:
                        io_queue.append((left_row, left_col, distance))
                else:
                    if ((distance+1) % 2) == 0:
                        inside += 1
                        inside_tiles.append(tile)
                    break
            # right
            if (q_col < last_c):
                right_row = q_row
                right_col = q_col + 1
                if (right_row, right_col) not in o_visited:
                    if (right_row, right_col) in visited:
                        io_queue.append((right_row, right_col, distance+1))
                    else:
                        io_queue.append((right_row, right_col, distance))
                else:
                    if ((distance+1) % 2) == 0:
                        inside += 1
                        inside_tiles.append(tile)
                    break

            io_visited.append(q)

    print(inside_tiles)
    output = inside

    return output

def process_inputs3(in_file):
    grid = [] # row, column
    output = 0

    start = 0
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            grid.append(line)

            for col, l in enumerate(line):
                if (l == 'S'):
                    start = (row, col)

            line = file.readline()
            row += 1

    s_row, s_col = start

    # BFS
    queue = []
    visited = []

    q_row, q_col = start
    # up
    if (q_row > 0):
        up = grid[q_row - 1][q_col]
        if not ((up == '-') or (up == 'L') or (up == 'J') or (up == 'S') or (up == '.')):
            #grid[q_row - 1][q_col] = '.'
            queue.append((q_row-1, q_col))
    # down
    if (q_row < (len(grid)-1)):
        down = grid[q_row+1][q_col]
        if not ((down == '-') or (down == '7') or (down == 'F') or (down == 'S') or (down == '.')):
            #grid[q_row+1][q_col] = '.'
            queue.append((q_row+1, q_col))
    # left
    if (q_col > 0):
        left = grid[q_row][q_col-1]
        if not ((left == '|') or (left == 'J') or (left == '7') or (left == 'S') or (left == '.')):
            #grid[q_row][q_col-1] = '.'
            queue.append((q_row, q_col-1))
    # right
    if (q_col < (len(grid[0])-1)):
        right = grid[q_row][q_col+1]
        if not ((right == '|') or (right == 'L') or (right == 'F') or (right == 'S') or (right == '.')):
            #grid[q_row][q_col+1] = '.' 
            queue.append((q_row, q_col+1))
    visited.append(start)
    while len(queue):
        q = queue.pop(0)
        q_row, q_col = q

        if (q in visited):
            continue

        curr = grid[q_row][q_col]

        #print(f'curr: {q_row}, {q_col}')
        #print(f'old queue: {queue}')

        # up
        if (curr in curr_up_list):
            up = grid[q_row - 1][q_col]
            if (up in up_list):
                queue.append((q_row-1, q_col))
        # down
        if (curr in curr_down_list):
            down = grid[q_row+1][q_col]
            if (down in down_list):
                queue.append((q_row+1, q_col))
        # left
        if (curr in curr_left_list):
            left = grid[q_row][q_col-1]
            if (left in left_list):
                queue.append((q_row, q_col-1))
        # right
        if (curr in curr_right_list):
            right = grid[q_row][q_col+1]
            if (right in right_list):
                queue.append((q_row, q_col+1))
        
        #print(f'new queue: {queue}')

        visited.append(q)

    # BFS across outside of loop first
    loop_edge = []
    o_visited = []
    o_queue = []

    not_loop = []

    not_in_loop = 0
    total_tiles = 0
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            total_tiles += 1
            if ((r, c) not in visited):
                #o_queue.append((r, c))
                not_in_loop += 1
    #            #print(".", end="")
    #        #else:
    #        #    print(grid[r][c],end="")
    #    #print("")
    last_r = len(grid)-1
    last_c = len(grid[0])-1
    # hardcoded based on input
    o_queue.append((0, 0))
    o_queue.append((0, last_c))
    o_queue.append((last_r, 0))
    o_queue.append((last_r, last_c))
    print(f'Total tiles: {total_tiles}')
    print(f'Tiles in the loop: {len(visited)}')
    print(f'Tiles not in the loop: {not_in_loop}')

    while len(o_queue):
        q = o_queue.pop(0)
        q_row, q_col = q

        if q in o_visited:
            continue

        # if not in loop, not already visited, and not in queue, don't add to queue
        # up
        if (q_row > 0):
            if (q_row-1, q_col) not in visited and ( (q_row-1, q_col) not in o_visited) and ( (q_row-1, q_col) not in o_queue):
                o_queue.append((q_row-1, q_col))
            elif (q_row-1, q_col) in visited:
                loop_edge.append((q_row-1, q_col))
        # down
        if (q_row < (len(grid)-1)):
            if (q_row+1, q_col) not in visited and ( (q_row+1, q_col) not in o_visited) and ( (q_row+1, q_col) not in o_queue):
                o_queue.append((q_row+1, q_col))
            elif (q_row+1, q_col) in visited:
                loop_edge.append((q_row+1, q_col))
        # left
        if (q_col > 0):
            if (q_row, q_col-1) not in visited and ( (q_row, q_col-1) not in o_visited) and ( (q_row, q_col-1) not in o_queue):
                o_queue.append((q_row, q_col-1))
            elif (q_row, q_col-1) in visited:
                loop_edge.append((q_row, q_col-1))
        # right
        if (q_col < (len(grid[0])-1)):
            if (q_row, q_col+1) not in visited and ( (q_row, q_col+1) not in o_visited) and ( (q_row, q_col+1) not in o_queue):
                o_queue.append((q_row, q_col+1))
            elif (q_row, q_col+1) in visited:
                loop_edge.append((q_row, q_col+1))

        o_visited.append(q)

    # if smallest distance to o_visited is odd: tile is inside
    # else, tile is outside
    io = []
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            if ((r, c) not in visited) and ((r, c) not in o_visited):
                io.append((r, c))

    inside = 0
    inside_tiles = []
    print(len(io))

    for idx, tile in enumerate(io):
        q_row, q_col = tile
        print(f'Tile {idx}/{len(io)}: ({q_row}, {q_col})')

        # special case: if diagonal from outside, then tile is outside as well
        if (q_row > 0):
            if (q_col > 0):
                if (q_row-1, q_col-1) in o_visited:
                    o_visited.append(tile)
                    break
            if (q_col < last_c):
                if (q_row-1, q_col+1) in o_visited:
                    o_visited.append(tile)
                    break
        elif (q_row < last_r):
            if (q_col > 0):
                if (q_row+1, q_col-1) in o_visited:
                    o_visited.append(tile)
                    break
            if (q_col < last_c):
                if (q_row+1, q_col+1) in o_visited:
                    o_visited.append(tile)

    for tile in io:
        q_row, q_col = tile

        up_dist = 0
        down_dist = 0
        left_dist = 0
        right_dist = 0

        for i in range(q_row, -1, -1):
            if ((i, q_col) in visited):
                up_dist += 1
            elif (i, q_col) in o_visited:
                break

        for i in range(q_row, last_r+1):
            if (i, q_col) in visited:
                down_dist += 1
            elif (i, q_col) in o_visited:
                break

        for i in range(q_col, -1, -1):
            if (q_row, i) in visited:
                left_dist +=1
            elif (q_row, i) in o_visited:
                break

        for i in range(q_col, last_c+1):
            if (q_row, i) in visited:
                right_dist +=1
            elif (q_row, i) in o_visited:
                break

        min_dist = min(up_dist, down_dist, left_dist, right_dist)

        #if ((q_row, q_col) == (4, 7)): 
        #    print("(4, 7) distances:")
        #    print(up_dist)
        #    print(down_dist)
        #    print(left_dist)
        #    print(right_dist)

        if (min_dist % 2) == 1:
            inside += 1
            inside_tiles.append((q_row, q_col))

    # propagate inside tiles
    i_queue = []
    i_visited = []
    for it in inside_tiles:
        i_queue.append(it)

    print(f'Initial insides: {inside}')
    print(inside_tiles)
    while len(i_queue):
        q = i_queue.pop(0)
        q_row, q_col = q

        if q in i_visited:
            continue

        up_tuple = (q_row-1, q_col)
        down_tuple = (q_row+1, q_col)
        left_tuple = (q_row, q_col-1)
        right_tuple = (q_row, q_col+1)

        if up_tuple in io and up_tuple not in i_visited:
            inside+=1
            inside_tiles.append(up_tuple)
            i_queue.append(up_tuple)
        if down_tuple in io and down_tuple not in i_visited:
            inside+=1
            inside_tiles.append(down_tuple)
            i_queue.append(down_tuple)
        if left_tuple in io and left_tuple not in i_visited:
            inside+=1
            inside_tiles.append(left_tuple)
            i_queue.append(left_tuple)
        if right_tuple in io and right_tuple not in i_visited:
            inside+=1
            inside_tiles.append(right_tuple)
            i_queue.append(right_tuple)

        i_visited.append(q)

    print(f'New insides: {inside}')
    print(inside_tiles)
    output = inside

    return output

def process_inputs4(in_file):
    grid = [] # row, column
    output = 0

    start = 0
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            grid.append(line)

            for col, l in enumerate(line):
                if (l == 'S'):
                    start = (row, col)

            line = file.readline()
            row += 1

    s_row, s_col = start

    # BFS
    queue = []
    visited = []

    q_row, q_col = start
    # up
    if (q_row > 0):
        up = grid[q_row - 1][q_col]
        if not ((up == '-') or (up == 'L') or (up == 'J') or (up == 'S') or (up == '.')):
            #grid[q_row - 1][q_col] = '.'
            queue.append((q_row-1, q_col))
    # down
    if (q_row < (len(grid)-1)):
        down = grid[q_row+1][q_col]
        if not ((down == '-') or (down == '7') or (down == 'F') or (down == 'S') or (down == '.')):
            #grid[q_row+1][q_col] = '.'
            queue.append((q_row+1, q_col))
    # left
    if (q_col > 0):
        left = grid[q_row][q_col-1]
        if not ((left == '|') or (left == 'J') or (left == '7') or (left == 'S') or (left == '.')):
            #grid[q_row][q_col-1] = '.'
            queue.append((q_row, q_col-1))
    # right
    if (q_col < (len(grid[0])-1)):
        right = grid[q_row][q_col+1]
        if not ((right == '|') or (right == 'L') or (right == 'F') or (right == 'S') or (right == '.')):
            #grid[q_row][q_col+1] = '.' 
            queue.append((q_row, q_col+1))
    visited.append(start)
    while len(queue):
        q = queue.pop(0)
        q_row, q_col = q

        if (q in visited):
            continue

        curr = grid[q_row][q_col]

        #print(f'curr: {q_row}, {q_col}')
        #print(f'old queue: {queue}')

        # up
        if (curr in curr_up_list):
            up = grid[q_row - 1][q_col]
            if (up in up_list):
                queue.append((q_row-1, q_col))
        # down
        if (curr in curr_down_list):
            down = grid[q_row+1][q_col]
            if (down in down_list):
                queue.append((q_row+1, q_col))
        # left
        if (curr in curr_left_list):
            left = grid[q_row][q_col-1]
            if (left in left_list):
                queue.append((q_row, q_col-1))
        # right
        if (curr in curr_right_list):
            right = grid[q_row][q_col+1]
            if (right in right_list):
                queue.append((q_row, q_col+1))
        
        #print(f'new queue: {queue}')

        visited.append(q)

    # BFS across outside of loop first
    loop_edge = []
    o_visited = []
    o_queue = []

    not_loop = []

    not_in_loop = 0
    total_tiles = 0
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            total_tiles += 1
            if ((r, c) not in visited):
                #o_queue.append((r, c))
                not_in_loop += 1
    #            #print(".", end="")
    #        #else:
    #        #    print(grid[r][c],end="")
    #    #print("")
    last_r = len(grid)-1
    last_c = len(grid[0])-1
    # hardcoded based on input
    o_queue.append((0, 0))
    o_queue.append((0, last_c))
    o_queue.append((last_r, 0))
    o_queue.append((last_r, last_c))
    print(f'Total tiles: {total_tiles}')
    print(f'Tiles in the loop: {len(visited)}')
    print(f'Tiles not in the loop: {not_in_loop}')

    while len(o_queue):
        q = o_queue.pop(0)
        q_row, q_col = q

        if q in o_visited:
            continue

        # if not in loop, not already visited, and not in queue, don't add to queue
        # up
        if (q_row > 0):
            if (q_row-1, q_col) not in visited and ( (q_row-1, q_col) not in o_visited) and ( (q_row-1, q_col) not in o_queue):
                o_queue.append((q_row-1, q_col))
            elif (q_row-1, q_col) in visited:
                loop_edge.append((q_row-1, q_col))

            if (q_col > 0):
                if (q_row-1, q_col-1) not in visited and ((q_row-1, q_col-1) not in o_visited) and ( (q_row-1, q_col-1) not in o_queue):
                    o_queue.append((q_row-1, q_col-1))

            if (q_col < (len(grid[0])-1)):
                if (q_row-1, q_col+1) not in visited and ((q_row-1, q_col+1) not in o_visited) and ( (q_row-1, q_col+1) not in o_queue):
                    o_queue.append((q_row-1, q_col+1))
        # down
        if (q_row < (len(grid)-1)):
            if (q_row+1, q_col) not in visited and ( (q_row+1, q_col) not in o_visited) and ( (q_row+1, q_col) not in o_queue):
                o_queue.append((q_row+1, q_col))
            elif (q_row+1, q_col) in visited:
                loop_edge.append((q_row+1, q_col))

            if (q_col > 0):
                if (q_row+1, q_col-1) not in visited and ( (q_row+1, q_col-1) not in o_visited) and ( (q_row+1, q_col-1) not in o_queue):
                    o_queue.append((q_row+1, q_col-1))

            if (q_col < (len(grid[0])-1)):
                if (q_row+1, q_col+1) not in visited and ( (q_row+1, q_col+1) not in o_visited) and ( (q_row+1, q_col+1) not in o_queue):
                    o_queue.append((q_row+1, q_col+1))

        # left
        if (q_col > 0):
            if (q_row, q_col-1) not in visited and ( (q_row, q_col-1) not in o_visited) and ( (q_row, q_col-1) not in o_queue):
                o_queue.append((q_row, q_col-1))
            elif (q_row, q_col-1) in visited:
                loop_edge.append((q_row, q_col-1))
        # right
        if (q_col < (len(grid[0])-1)):
            if (q_row, q_col+1) not in visited and ( (q_row, q_col+1) not in o_visited) and ( (q_row, q_col+1) not in o_queue):
                o_queue.append((q_row, q_col+1))
            elif (q_row, q_col+1) in visited:
                loop_edge.append((q_row, q_col+1))

        o_visited.append(q)

    print(f'Tiles not yet identified: {total_tiles - len(visited) - len(o_visited)}')
    io = []
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            if ((r, c) not in visited) and ((r, c) not in o_visited):
                io.append((r, c))

    loop = []
    for i in range(0, len(visited), 2):
        loop.append(visited[i])

    if (len(visited) % 2 == 0):
        start = len(visited) - 1
    else:
        start = len(visited) - 2
    for i in range(start, 0, -2):
        loop.append(visited[i])

    print(f'Loop: {loop}')

    # "Encircle" the tiles in io
    inside_tiles = []
    inside = 0
    outside = True
    print(len(io))
    for tile in io:
        q_row, q_col = tile

        # special case: if diagonal from outside, then tile is outside as well
        #if (q_row > 0):
        #    if (q_col > 0):
        #        if (q_row-1, q_col-1) in o_visited:
        #            o_visited.append(tile)
        #            continue
        #    if (q_col < last_c):
        #        if (q_row-1, q_col+1) in o_visited:
        #            o_visited.append(tile)
        #            continue

        #if (q_row < last_r):
        #    if (q_col > 0):
        #        if (q_row+1, q_col-1) in o_visited:
        #            o_visited.append(tile)
        #            continue
        #    if (q_col < last_c):
        #        if (q_row+1, q_col+1) in o_visited:
        #            o_visited.append(tile)
        #            continue

        intersection = None
        inter = []
        prev_l_row = None
        prev_l_col = None
        above = 0
        below = 0
        left = 0
        right = 0
        possiblyinside = False
        running_inter = []
        for l in loop:
            if (prev_l_row == None):
                prev_l_row, prev_l_col = loop[-1]
            else:
                prev_l_row, prev_l_col = l_row, l_col
            l_row, l_col = l

            if (l_row == q_row):
                if (l_row < prev_l_row):
                    vertical_dir = "up"
                elif (l_row > prev_l_row):
                    vertical_dir = "down"
                elif (grid[l_row][l_col] in ['F', '7']):
                    vertical_dir = "down"
                elif (grid[l_row][l_col] in ['J', 'L']):
                    vertical_dir = "up"
                else:
                    vertical_dir = None

            if (l_row == q_row) and (vertical_dir in ['up', 'down']):
                if (l_col < q_col):
                    left += 1
                    pos = "left"

                elif (l_col > q_col):
                    right += 1
                    pos = "right"

                running_inter.append((l_row, l_col, vertical_dir, pos))

                if (len(inter)):
                    last_dir, last_pos = inter[-1]
                    if (last_dir != vertical_dir) and (last_pos != pos):
                        inter.append((vertical_dir, pos))
                        possiblyinside = True
                    elif (last_dir != vertical_dir) and (last_pos == pos):
                        inter.pop()
                    elif (last_dir == vertical_dir) and (last_pos == pos):
                        # possible for example FJI, F and J both go up
                        print("same direction and position")
                        #inter.append((vertical_dir, pos))
                    else:
                        # same direction but different position?
                        print(f'impossible? tile {tile}, loop ({l_row}, {l_col})')
                        inter.append((vertical_dir, pos))
                else:
                    inter.append((vertical_dir, pos))

            if (l_col == q_col):
                if (l_col < prev_l_col):
                    horizontal_dir = "left"
                elif (l_col > prev_l_col):
                    horizontal_dir = "right"
                else:
                    horizontal_dir = None

            if (l_col == q_col) and (horizontal_dir in ['left', 'right']):
                if (l_row < q_row):
                    above += 1
                elif (l_row > q_row):
                    below += 1

        if ((q_row, q_col) == (2, 3)):
            print(f'DEBUG: {tile}: running_inter = {running_inter}')

        # process running intersection
        inter = []
        for idx, ri in enumerate(running_inter):
            if (idx > 0):
                prev_i_row, prev_i_col, prev_i_dir, prev_i_pos = running_inter[idx-1]
            else:
                inter.append(ri)
                continue
            i_row, i_col, i_dir, i_pos = ri

            if (prev_i_dir == i_dir) and (prev_i_pos == i_pos):
                continue
            else:
                inter.append(ri)

        if ((q_row, q_col) == (2, 3)):
            print(f'DEBUG: {tile}: inter = {inter}')

        possiblyinside = False
        counter = 0
        for idx in range(1, len(inter), 2):
            prev_i_row, prev_i_col, prev_i_dir, prev_i_pos = inter[idx-1]
            
            i_row, i_col, i_dir, i_pos = inter[idx]

            if (prev_i_dir != i_dir) and (prev_i_pos != i_pos):
                possiblyinside = True
                counter += 1

        if (possiblyinside) and (counter % 2 == 1):
        #if (possiblyinside) and (len(inter)) > 1:
        #if (left % 2 == 1) and (right % 2 == 1):
            inside += 1
            inside_tiles.append([tile, counter])

    print(f'Inside tiles: {inside_tiles}')

    for idx_r, row in enumerate(grid):
        for idx_c, r in enumerate(row):
            tile = (idx_r, idx_c)
            if (tile in visited):
                print(grid[idx_r][idx_c], end="")
            elif (tile in o_visited):
                print('.', end="")
            elif (tile in inside_tiles):
                print("I", end="")
            else:
                print('?', end="")

        print("")

    output = inside

    return output

def process_inputs5(in_file):
    grid = [] # row, column
    output = 0

    start = 0
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            grid.append(line)

            for col, l in enumerate(line):
                if (l == 'S'):
                    start = (row, col)

            line = file.readline()
            row += 1

    s_row, s_col = start

    # BFS
    queue = []
    visited = []

    q_row, q_col = start
    # up
    if (q_row > 0):
        up = grid[q_row - 1][q_col]
        if not ((up == '-') or (up == 'L') or (up == 'J') or (up == 'S') or (up == '.')):
            #grid[q_row - 1][q_col] = '.'
            queue.append((q_row-1, q_col))
    # down
    if (q_row < (len(grid)-1)):
        down = grid[q_row+1][q_col]
        if not ((down == '-') or (down == '7') or (down == 'F') or (down == 'S') or (down == '.')):
            #grid[q_row+1][q_col] = '.'
            queue.append((q_row+1, q_col))
    # left
    if (q_col > 0):
        left = grid[q_row][q_col-1]
        if not ((left == '|') or (left == 'J') or (left == '7') or (left == 'S') or (left == '.')):
            #grid[q_row][q_col-1] = '.'
            queue.append((q_row, q_col-1))
    # right
    if (q_col < (len(grid[0])-1)):
        right = grid[q_row][q_col+1]
        if not ((right == '|') or (right == 'L') or (right == 'F') or (right == 'S') or (right == '.')):
            #grid[q_row][q_col+1] = '.' 
            queue.append((q_row, q_col+1))
    visited.append(start)
    while len(queue):
        q = queue.pop(0)
        q_row, q_col = q

        if (q in visited):
            continue

        curr = grid[q_row][q_col]

        #print(f'curr: {q_row}, {q_col}')
        #print(f'old queue: {queue}')

        # up
        if (curr in curr_up_list):
            up = grid[q_row - 1][q_col]
            if (up in up_list):
                queue.append((q_row-1, q_col))
        # down
        if (curr in curr_down_list):
            down = grid[q_row+1][q_col]
            if (down in down_list):
                queue.append((q_row+1, q_col))
        # left
        if (curr in curr_left_list):
            left = grid[q_row][q_col-1]
            if (left in left_list):
                queue.append((q_row, q_col-1))
        # right
        if (curr in curr_right_list):
            right = grid[q_row][q_col+1]
            if (right in right_list):
                queue.append((q_row, q_col+1))
        
        #print(f'new queue: {queue}')

        visited.append(q)

    # BFS across outside of loop first
    loop_edge = []
    o_visited = []
    o_queue = []

    not_loop = []

    not_in_loop = 0
    total_tiles = 0
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            total_tiles += 1
            if ((r, c) not in visited):
                #o_queue.append((r, c))
                not_in_loop += 1
    #            #print(".", end="")
    #        #else:
    #        #    print(grid[r][c],end="")
    #    #print("")
    last_r = len(grid)-1
    last_c = len(grid[0])-1
    # hardcoded based on input
    o_queue.append((0, 0))
    o_queue.append((0, last_c))
    o_queue.append((last_r, 0))
    o_queue.append((last_r, last_c))
    print(f'Total tiles: {total_tiles}')
    print(f'Tiles in the loop: {len(visited)}')
    print(f'Tiles not in the loop: {not_in_loop}')

    while len(o_queue):
        q = o_queue.pop(0)
        q_row, q_col = q

        if q in o_visited:
            continue

        # if not in loop, not already visited, and not in queue, don't add to queue
        # up
        if (q_row > 0):
            if (q_row-1, q_col) not in visited and ( (q_row-1, q_col) not in o_visited) and ( (q_row-1, q_col) not in o_queue):
                o_queue.append((q_row-1, q_col))
            elif (q_row-1, q_col) in visited:
                loop_edge.append((q_row-1, q_col))

            if (q_col > 0):
                if (q_row-1, q_col-1) not in visited and ((q_row-1, q_col-1) not in o_visited) and ( (q_row-1, q_col-1) not in o_queue):
                    o_queue.append((q_row-1, q_col-1))

            if (q_col < (len(grid[0])-1)):
                if (q_row-1, q_col+1) not in visited and ((q_row-1, q_col+1) not in o_visited) and ( (q_row-1, q_col+1) not in o_queue):
                    o_queue.append((q_row-1, q_col+1))
        # down
        if (q_row < (len(grid)-1)):
            if (q_row+1, q_col) not in visited and ( (q_row+1, q_col) not in o_visited) and ( (q_row+1, q_col) not in o_queue):
                o_queue.append((q_row+1, q_col))
            elif (q_row+1, q_col) in visited:
                loop_edge.append((q_row+1, q_col))

            if (q_col > 0):
                if (q_row+1, q_col-1) not in visited and ( (q_row+1, q_col-1) not in o_visited) and ( (q_row+1, q_col-1) not in o_queue):
                    o_queue.append((q_row+1, q_col-1))

            if (q_col < (len(grid[0])-1)):
                if (q_row+1, q_col+1) not in visited and ( (q_row+1, q_col+1) not in o_visited) and ( (q_row+1, q_col+1) not in o_queue):
                    o_queue.append((q_row+1, q_col+1))

        # left
        if (q_col > 0):
            if (q_row, q_col-1) not in visited and ( (q_row, q_col-1) not in o_visited) and ( (q_row, q_col-1) not in o_queue):
                o_queue.append((q_row, q_col-1))
            elif (q_row, q_col-1) in visited:
                loop_edge.append((q_row, q_col-1))
        # right
        if (q_col < (len(grid[0])-1)):
            if (q_row, q_col+1) not in visited and ( (q_row, q_col+1) not in o_visited) and ( (q_row, q_col+1) not in o_queue):
                o_queue.append((q_row, q_col+1))
            elif (q_row, q_col+1) in visited:
                loop_edge.append((q_row, q_col+1))

        o_visited.append(q)

    print(f'Tiles not yet identified: {total_tiles - len(visited) - len(o_visited)}')
    io = []
    for r, grid_row in enumerate(grid):
        for c, tile in enumerate(grid_row):
            if ((r, c) not in visited) and ((r, c) not in o_visited):
                io.append((r, c))

    loop = []
    for i in range(0, len(visited), 2):
        loop.append(visited[i])

    if (len(visited) % 2 == 0):
        start = len(visited) - 1
    else:
        start = len(visited) - 2
    for i in range(start, 0, -2):
        loop.append(visited[i])

    # "Encircle" the tiles in io
    inside = 0
    inside_tiles = []
    print(f'io = {io}')
    for tile in io:
        q_row, q_col = tile

        row = grid[q_row]

        left = 0
        for i in range(0, q_col):
            if ((q_row, i) in visited):
                loop_pipe = grid[q_row][i]

                if (loop_pipe in up_list) or (loop_pipe in down_list):
                    left += 1

        right = 0
        for i in range(q_col+1, last_c):
            if ((q_row, i) in visited):
                loop_pipe = grid[q_row][i]

                if (loop_pipe in up_list) or (loop_pipe in down_list):
                    right += 1

        leftiseven = (left % 2 == 0)
        leftisodd = (left % 2 == 1)
        rightiseven = (right % 2 == 0)
        rightisodd = (right % 2 == 1)
        if ((left % 2) == 1) or ((right % 2) == 1) or (leftiseven and rightiseven and (left != right)):
            inside += 1
            inside_tiles.append((q_row, q_col))

    output = inside
    print(f'Inside tiles: {inside_tiles}')

    return output

#part1_example = process_inputs(example_file)
#part1         = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2         = process_inputs2(input_file)
#part2_example = process_inputs3(example_file)
#part2         = process_inputs3(input_file)
part2_example = process_inputs4(example_file) # closest so far
part2         = process_inputs4(input_file)
#part2_example = process_inputs5(example_file)
#part2         = process_inputs5(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1        : {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2        : {part2}')

