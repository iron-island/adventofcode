from collections import defaultdict
from collections import deque
import math

input_file = "input6.txt"
example_file = "example06.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def get_dist(rc, coords_list):
    row1, col1 = rc
    dist_list = []
    for coords in coords_list:
        row2, col2 = coords
        dist_list.append(abs(row2-row1) + abs(col2-col1))

    return dist_list

def move_dir(rc, direction):
    row, col = rc

    assert(direction in ["up", "down", "left", "right"])
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
    
def process_inputs(in_file):
    output = 0

    grid_dict = defaultdict(int)
    MIN_ROW = math.inf
    MIN_COL = math.inf
    MAX_ROW = -math.inf
    MAX_COL = -math.inf
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            col, row = line.split(", ")
            row = int(row)
            col = int(col)
            MIN_ROW = min(row, MIN_ROW)
            MIN_COL = min(col, MIN_COL)
            MAX_ROW = max(row, MAX_ROW)
            MAX_COL = max(col, MAX_COL)
            grid_dict[(row, col)] = 0

            line = file.readline()

    dist_dict = defaultdict(tuple)
    coords_list = list(grid_dict.keys())
    output = 0
    for row in range(MIN_ROW, MAX_ROW+1):
        for col in range(MIN_COL, MAX_COL+1):
            rc = (row, col)
            dist_list = get_dist(rc, coords_list)
            min_dist = min(dist_list)

            if (dist_list.count(min_dist) == 1):
                idx = dist_list.index(min_dist)
                nearest_coord = coords_list[idx]
                #if (nearest_row > 0) and (nearest_row < MAX_ROW) and \
                #   (nearest_col > 0) and (nearest_col < MAX_COL):
                grid_dict[nearest_coord] += 1
                dist_dict[rc] = nearest_coord

    # DEBUG
    #for row in range(0, 10):
    #    for col in range(0, 10):
    #        rc = (row, col)
    #        nearest_coord = dist_dict[(row, col)]
    #        if (nearest_coord == coords_list[0]):
    #            if (nearest_coord == rc):
    #                print('A', end="")
    #            else:
    #                print('a', end="")
    #        elif (nearest_coord == coords_list[1]):
    #            if (nearest_coord == rc):
    #                print('B', end="")
    #            else:
    #                print('b', end="")
    #        elif (nearest_coord == coords_list[2]):
    #            if (nearest_coord == rc):
    #                print('C', end="")
    #            else:
    #                print('c', end="")
    #        elif (nearest_coord == coords_list[3]):
    #            if (nearest_coord == rc):
    #                print('D', end="")
    #            else:
    #                print('d', end="")
    #        elif (nearest_coord == coords_list[4]):
    #            if (nearest_coord == rc):
    #                print('E', end="")
    #            else:
    #                print('e', end="")
    #        elif (nearest_coord == coords_list[5]):
    #            if (nearest_coord == rc):
    #                print('F', end="")
    #            else:
    #                print('f', end="")
    #        else:
    #            print('.', end="")

    #    print("")
    #return 0

    MAX_AREA = -math.inf
    for rc in grid_dict:
        nearest_coord = dist_dict[rc]

        # BFS to check if area is finite by checking that it doesn't touch the boundaries
        q = deque()
        visited = set()
        q.append(rc)
        finite = True
        while len(q):
            row, col = q.popleft()

            if (row in [MIN_ROW, MAX_ROW]) or (col in [MIN_COL, MAX_COL]):       
                finite = False
                break

            if ((row, col) in visited):
                continue
            visited.add((row, col))

            # up
            n_row, n_col = move_dir((row, col), "up")
            n_tuple = (n_row, n_col)
            if (n_tuple in dist_dict) and (dist_dict[n_tuple] == nearest_coord):
                q.append(n_tuple)

            # down
            n_row, n_col = move_dir((row, col), "down")
            n_tuple = (n_row, n_col)
            if (n_tuple in dist_dict) and (dist_dict[n_tuple] == nearest_coord):
                q.append(n_tuple)

            # left
            n_row, n_col = move_dir((row, col), "left")
            n_tuple = (n_row, n_col)
            if (n_tuple in dist_dict) and (dist_dict[n_tuple] == nearest_coord):
                q.append(n_tuple)

            # right
            n_row, n_col = move_dir((row, col), "right")
            n_tuple = (n_row, n_col)
            if (n_tuple in dist_dict) and (dist_dict[n_tuple] == nearest_coord):
                q.append(n_tuple)

        # Check min distance
        if (finite):
            MAX_AREA = max(len(visited), MAX_AREA)

    #max_nearest_coord = max(grid_dict, key=grid_dict.get)
    #output = grid_dict[max_nearest_coord]
    output = MAX_AREA

    return output

def process_inputs2(in_file, bounds):
    output = 0

    grid_dict = defaultdict(int)
    MIN_ROW = math.inf
    MIN_COL = math.inf
    MAX_ROW = -math.inf
    MAX_COL = -math.inf
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            col, row = line.split(", ")
            row = int(row)
            col = int(col)
            MIN_ROW = min(row, MIN_ROW)
            MIN_COL = min(col, MIN_COL)
            MAX_ROW = max(row, MAX_ROW)
            MAX_COL = max(col, MAX_COL)
            grid_dict[(row, col)] = 0

            line = file.readline()

    dist_dict = defaultdict(tuple)
    coords_list = list(grid_dict.keys())
    for row in range(MIN_ROW, MAX_ROW+1):
        for col in range(MIN_COL, MAX_COL+1):
            rc = (row, col)
            dist_list = get_dist(rc, coords_list)

            tot_dist = sum(dist_list)
            if (tot_dist < bounds):
                output += 1

            # DEBUG
            if (rc == (4, 3)):
                print(dist_list)

            #min_dist = min(dist_list)

            #if (dist_list.count(min_dist) == 1):
            #    idx = dist_list.index(min_dist)
            #    nearest_coord = coords_list[idx]
            #    #if (nearest_row > 0) and (nearest_row < MAX_ROW) and \
            #    #   (nearest_col > 0) and (nearest_col < MAX_COL):
            #    grid_dict[nearest_coord] += 1
            #    dist_dict[rc] = nearest_coord

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file, 32)
part2 = process_inputs2(input_file, 10000)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
