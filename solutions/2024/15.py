from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input15.txt"

grid_dict = defaultdict(str)
# Check move 22 for example1
def can_move(n_tuple, move):
    global visited
    global grid_dict

    n_row, n_col = n_tuple

    if (n_tuple in visited):
        return True

    if (n_tuple in grid_dict):
        tile = grid_dict[n_tuple]

        if (move == '^'):
            modifier = -1
        elif (move == 'v'):
            modifier = 1

        if (tile == '.'):
            return True
        elif (tile == '#'):
            return False
        elif (tile == '['):
            adj_tuple = (n_row, n_col+1)
            if (adj_tuple not in visited):
                visited.append(adj_tuple)
            visited.append(n_tuple)
            return (can_move((n_row+modifier, n_col), move) and can_move((n_row+modifier, n_col+1), move))
        elif (tile == ']'):
            adj_tuple = (n_row, n_col-1)
            if (adj_tuple not in visited):
                visited.append(adj_tuple)
            visited.append(n_tuple)
            return (can_move((n_row+modifier, n_col), move) and can_move((n_row+modifier, n_col-1), move))

def part1(in_file):
    part1 = 0

    grid = []
    row = 0
    col = 0
    get_movements = False
    moves_list = ""
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if (line == ""):
                get_movements = True
                MAX_ROW = row-1
            elif (not get_movements):
                MAX_COL = len(line)-1
                for col in range(0, len(line)):
                    grid_dict[(row, col)] = line[col]

                    if (line[col] == '@'):
                        robot_pos = [row, col]
            elif (get_movements):
                moves_list = moves_list + line

            row += 1
            line = file.readline()

    # Simulate
    for idx, move in enumerate(moves_list):
        row, col = robot_pos
        old_tuple = (row, col)

        if (move == '^'):
            n_row = row - 1
            n_col = col
            modifier = -1
        elif (move == '<'):
            n_row = row
            n_col = col - 1
            modifier = -1
        elif (move == 'v'):
            n_row = row + 1
            n_col = col
            modifier = 1
        elif (move == '>'):
            n_row = row
            n_col = col + 1
            modifier = 1

        n_tuple = (n_row, n_col)
        if (n_tuple in grid_dict):
            n_tile = grid_dict[n_tuple]

            if (n_tile == '.'):
                robot_pos = [n_row, n_col]
                grid_dict[n_tuple] = '@'
                grid_dict[old_tuple] = '.'
            elif (n_tile == 'O'):
                # If stone, check if it can move
                if (move == '^'):
                    sn_row = n_row - 1
                    sn_col = n_col
                elif (move == '<'):
                    sn_row = n_row
                    sn_col = n_col - 1
                elif (move == 'v'):
                    sn_row = n_row + 1
                    sn_col = n_col
                elif (move == '>'):
                    sn_row = n_row
                    sn_col = n_col + 1

                # Get all tiles up to boundary
                pos_list = []
                sn_tuple = (sn_row, sn_col)
                orig_sn_tuple = sn_tuple
                while (True):
                    if (sn_tuple in grid_dict):
                        sn_row, sn_col = sn_tuple
                        sn_tile = grid_dict[sn_tuple]
                        if (sn_tile == 'O'):
                            pos_list.append(sn_tuple)
                            if (move in "^v"):
                                sn_tuple = (sn_row+modifier, sn_col)
                            elif (move in "><"):
                                sn_tuple = (sn_row, sn_col+modifier)
                        elif (sn_tile == '.'):
                            pos_list.append(sn_tuple)
                            break
                        elif (sn_tile == '#'):
                            pos_list = []
                            break
                    else:
                        break

                # Move tiles
                if (len(pos_list)):
                    for pos in pos_list:
                        grid_dict[pos] = 'O'
                    grid_dict[n_tuple] = '@'
                    robot_pos = [n_tuple[0], n_tuple[1]]
                    grid_dict[old_tuple] = '.'
                
    # GPS
    for pos in grid_dict:
        row, col = pos
        tile = grid_dict[pos]

        if (tile == 'O'):
            part1 += row*100 + col
    
    return part1

def part2(in_file):
    global visited
    global grid_dict
    part2 = 0

    grid = []
    row = 0
    col = 0
    get_movements = False
    moves_list = ""
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if (line == ""):
                get_movements = True
                MAX_ROW = row-1
            elif (not get_movements):
                MAX_COL = len(line)-1
                # Expand
                line = line.replace("#", "##")
                line = line.replace("O", "[]")
                line = line.replace(".", "..")
                line = line.replace("@", "@.")

                for col in range(0, len(line)):
                    grid_dict[(row, col)] = line[col]

                    if (line[col] == '@'):
                        robot_pos = [row, col]
            elif (get_movements):
                moves_list = moves_list + line

            row += 1
            line = file.readline()

    # Adjust
    MAX_COL = 2*MAX_COL+1

    # Simulate
    for idx_m, move in enumerate(moves_list):
        row, col = robot_pos
        old_tuple = (row, col)

        if (move == '^'):
            n_row = row - 1
            n_col = col
            modifier = -1
        elif (move == '<'):
            n_row = row
            n_col = col - 1
            modifier = -1
        elif (move == 'v'):
            n_row = row + 1
            n_col = col
            modifier = 1
        elif (move == '>'):
            n_row = row
            n_col = col + 1
            modifier = 1

        n_tuple = (n_row, n_col)
        if (n_tuple in grid_dict):
            n_tile = grid_dict[n_tuple]
            #print(n_tile)

            if (n_tile == '.'):
                robot_pos = [n_row, n_col]
                grid_dict[n_tuple] = '@'
                grid_dict[old_tuple] = '.'
            elif (n_tile in "[]"):
                # If stone, check if it can move
                if (move == '^'):
                    sn_row = n_row - 1
                    sn_col = n_col
                elif (move == '<'):
                    sn_row = n_row
                    sn_col = n_col - 1
                elif (move == 'v'):
                    sn_row = n_row + 1
                    sn_col = n_col
                elif (move == '>'):
                    sn_row = n_row
                    sn_col = n_col + 1

                # Get all tiles up to boundary
                pos_list = []
                sn_tuple = (sn_row, sn_col)
                orig_sn_tuple = sn_tuple
                side_pos_list = []
                side_mod = 0
                side2_pos_list = []
                side2_mod = 0
                side3_pos_list = []
                side3_mod = 0
                if (sn_tuple in grid_dict) and (move in "^v"):
                    sn_tile = grid_dict[sn_tuple]
                    sn_row, sn_col = sn_tuple
                    if (n_tile == '['):
                        side_mod = 1
                    elif (n_tile == ']'):
                        side_mod = -1
                    side2_mod = 2*side_mod
                    side3_mod = -side_mod
                    side_sn_tuple = (sn_row, sn_col+side_mod)

                while (True):
                    if (sn_tuple in grid_dict): # assume that side_sn_tuple also in grid
                        sn_row, sn_col = sn_tuple
                        sn_tile = grid_dict[sn_tuple]

                        if (move in "><"):
                            if (sn_tile in '[]'):
                                pos_list.append(sn_tuple)
                                sn_tuple = (sn_row, sn_col+modifier)
                            elif (sn_tile == '.'):
                                pos_list.append(sn_tuple)
                                break
                            elif (sn_tile == '#'):
                                pos_list = []
                                break
                        elif (move in "^v"):
                            break
                    else:
                        break

                # Move tiles
                visited = []
                if (len(pos_list)) and (move in "><"):
                    pos_list.reverse()
                    for pos in pos_list:
                        row, col = pos
                        grid_dict[pos] = grid_dict[(row, col-modifier)]
                    grid_dict[n_tuple] = '@'
                    robot_pos = [n_tuple[0], n_tuple[1]]
                    grid_dict[old_tuple] = '.'
                elif (move in "^v") and can_move(n_tuple, move):
                    # Sort viisited by rows
                    # Ref: https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
                    visited = sorted(visited, key=lambda x: x[0])
                    if (move == 'v'):
                        visited.reverse()

                    #if ((idx_m+1) in [4000, 4001]):
                    #    print(visited)
                    for v in visited:
                        row, col = v
                        tile = grid_dict[v]
                        grid_dict[(row+modifier, col)] = tile
                        grid_dict[v] = '.'

                    grid_dict[n_tuple] = '@'
                    robot_pos = [n_tuple[0], n_tuple[1]]
                    grid_dict[old_tuple] = '.'

                    # Adjust side of @
                    grid_dict[(n_tuple[0], n_tuple[1]+side_mod)] = '.'

    # GPS
    for pos in grid_dict:
        row, col = pos
        tile = grid_dict[pos]

        if (tile == '['):
            part2 += row*100 + col
    
    return part2

part1 = part1(input_file)
part2 = part2(input_file)

print("")
print("--- Advent of Code 2024 Day 15: Warehouse Woes ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
