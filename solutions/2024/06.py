from collections import deque

input_file = "../../inputs/2024/input06.txt"
example_file = "example06.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
MAX_ROW = 0
MAX_COL = 0

def bfs_path_part1(INIT_GUARD, rowcol_list, colrow_list):
    # BFS to get original path
    direction = "up"
    q = deque()
    q.append(INIT_GUARD)
    turns_list = []
    path_set = set()
    while len(q):
        row, col = q.popleft()

        turns_list.append((row, col, direction))

        if (direction == "up"):
            row_list = colrow_list[col]

            last_obj_row = None
            for obj_row in row_list:
                if (obj_row < row):
                    last_obj_row = obj_row
                else:
                    break

            # If obj_row was encountered, add turn to queue and change direction
            if (last_obj_row != None):
                q.append((last_obj_row+1, col))
                direction = "right"

                curr_path = [(r, c) for r in range(row, last_obj_row, -1) for c in [col]]
                for path in curr_path:
                    path_set.add(path)
            # If didn't encounter any obj_row, then guard exits out of bounds
            else:
                turns_list.append((0, col, "exit"))

                curr_path = [(r, c) for r in range(row, -1, -1) for c in [col]]
                for path in curr_path:
                    path_set.add(path)
                break
        elif (direction == "right"):
            col_list = rowcol_list[row]

            last_obj_col = None
            for obj_col in reversed(col_list):
                if (obj_col > col):
                    last_obj_col = obj_col
                else:
                    break

            # If obj_col was encountered, add turn to queue and change direction
            if (last_obj_col != None):
                q.append((row, last_obj_col-1))
                direction = "down"

                curr_path = [(r, c) for r in [row] for c in range(col, last_obj_col)]
                for path in curr_path:
                    path_set.add(path)
            # If didn't encounter any obj_col, then guard exits out of bounds
            else:
                turns_list.append((row, MAX_COL, "exit"))

                curr_path = [(r, c) for r in [row] for c in range(col, MAX_COL+1)]
                for path in curr_path:
                    path_set.add(path)
                break
        elif (direction == "down"):
            row_list = colrow_list[col]

            last_obj_row = None
            for obj_row in reversed(row_list):
                if (obj_row > row):
                    last_obj_row = obj_row
                else:
                    break

            # If obj_row was encountered, add turn to queue and change direction
            if (last_obj_row != None):
                q.append((last_obj_row-1, col))
                direction = "left"

                curr_path = [(r, c) for r in range(row, last_obj_row) for c in [col]]
                for path in curr_path:
                    path_set.add(path)
            # If didn't encounter any obj_row, then guard exits out of bounds
            else:
                turns_list.append((MAX_ROW, col, "exit"))

                curr_path = [(r, c) for r in range(row, MAX_ROW+1) for c in [col]]
                for path in curr_path:
                    path_set.add(path)
                break
        elif (direction == "left"):
            col_list = rowcol_list[row]

            last_obj_col = None
            for obj_col in col_list:
                if (obj_col < col):
                    last_obj_col = obj_col
                else:
                    break

            # If obj_col was encountered, add turn to queue and change direction
            if (last_obj_col != None):
                q.append((row, last_obj_col+1))
                direction = "up"

                curr_path = [(r, c) for r in [row] for c in range(col, last_obj_col, -1)]
                for path in curr_path:
                    path_set.add(path)
            # If didn't encounter any obj_col, then guard exits out of bounds
            else:
                turns_list.append((row, 0, "exit"))

                curr_path = [(r, c) for r in [row] for c in range(col, -1, -1)]
                for path in curr_path:
                    path_set.add(path)
                break

    return path_set

# Same as bfs_path_part1, but doesn't construct path_set and just returns if 
#   path is repeated based on turns_list
def bfs_path_part2(INIT_GUARD, rowcol_list, colrow_list):
    # BFS to get original path
    direction = "up"
    q = deque()
    q.append(INIT_GUARD)
    turns_list = []
    repeated = False
    while len(q):
        row, col = q.popleft()

        if ((row, col, direction) in turns_list):
            repeated = True
            break
        turns_list.append((row, col, direction))

        if (direction == "up"):
            row_list = colrow_list[col]

            last_obj_row = None
            for obj_row in row_list:
                if (obj_row < row):
                    last_obj_row = obj_row
                else:
                    break

            # If obj_row was encountered, add turn to queue and change direction
            if (last_obj_row != None):
                q.append((last_obj_row+1, col))
                direction = "right"
            # If didn't encounter any obj_row, then guard exits out of bounds
            else:
                turns_list.append((0, col, "exit"))
                break
        elif (direction == "right"):
            col_list = rowcol_list[row]

            last_obj_col = None
            for obj_col in reversed(col_list):
                if (obj_col > col):
                    last_obj_col = obj_col
                else:
                    break

            # If obj_col was encountered, add turn to queue and change direction
            if (last_obj_col != None):
                q.append((row, last_obj_col-1))
                direction = "down"
            # If didn't encounter any obj_col, then guard exits out of bounds
            else:
                turns_list.append((row, MAX_COL, "exit"))
                break
        elif (direction == "down"):
            row_list = colrow_list[col]

            last_obj_row = None
            for obj_row in reversed(row_list):
                if (obj_row > row):
                    last_obj_row = obj_row
                else:
                    break

            # If obj_row was encountered, add turn to queue and change direction
            if (last_obj_row != None):
                q.append((last_obj_row-1, col))
                direction = "left"
            # If didn't encounter any obj_row, then guard exits out of bounds
            else:
                turns_list.append((MAX_ROW, col, "exit"))
                break
        elif (direction == "left"):
            col_list = rowcol_list[row]

            last_obj_col = None
            for obj_col in col_list:
                if (obj_col < col):
                    last_obj_col = obj_col
                else:
                    break

            # If obj_col was encountered, add turn to queue and change direction
            if (last_obj_col != None):
                q.append((row, last_obj_col+1))
                direction = "up"
            # If didn't encounter any obj_col, then guard exits out of bounds
            else:
                turns_list.append((row, 0, "exit"))
                break

    return repeated

def process_inputs2(in_file):
    global MAX_ROW
    global MAX_COL

    rowcol_list = []
    colrow_list = []
    with open(in_file) as file:
        line = file.readline()

        row = 0
        while line:
            line = line.strip()

            # List of lists used for optimized solution
            col_list = []
            col = 0
            for tile in line:
                if (row == 0):
                    colrow_list.append([])

                if (tile == "#"):
                    col_list.append(col)

                    colrow_list[col].append(row)
                elif (tile == "^"):
                    INIT_GUARD = (row, col)

                col += 1
            rowcol_list.append(col_list)
            MAX_COL = col-1

            row += 1
            line = file.readline()
        MAX_ROW = row-1

    #print(MAX_ROW, MAX_COL)
    path_set = bfs_path_part1(INIT_GUARD, rowcol_list, colrow_list)
    part1 = len(path_set)

    part2 = 0
    for path in path_set:
        p_row, p_col = path

        # Add obstacle in rowcol_list and colrow_list
        orig_col_list = [x for x in rowcol_list[p_row]]
        orig_row_list = [x for x in colrow_list[p_col]]
        rowcol_list[p_row].append(p_col)
        rowcol_list[p_row].sort()
        colrow_list[p_col].append(p_row)
        colrow_list[p_col].sort()

        repeated = bfs_path_part2(INIT_GUARD, rowcol_list, colrow_list)
        if (repeated):
            part2 += 1
        # Remove obstacle from rowcol_list, colrow_list
        rowcol_list[p_row] = [x for x in orig_col_list]
        colrow_list[p_col] = [x for x in orig_row_list]

    return part1, part2

#part1_example, part2_example = process_inputs2(example_file)
part1, part2 = process_inputs2(input_file)

#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
