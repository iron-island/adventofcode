from collections import defaultdict

input_file = "../../inputs/2024/input15.txt"
example_file = "example15.txt"
example2_file = "example15_2.txt"
example3_file = "example15_3.txt"
example4_file = "example15_4.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part2_example4 = 0
part1 = 0
part2 = 0
visited = []

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

def process_inputs(in_file):
    output = 0

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
            #print(n_tile)

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
                #row_list = [x for x in range(sn_row, MAX_ROW+1)]
                #col_list = [x for x in range(sn_col, MAX_COL+1)]
                #min_dist = min(len(row_list), len(col_list))
                #tile_list = []
                #new_tile_list = []
                #for i in range(0, min_dist):
                #    t_tuple = (row_list[i], col_list[i])
                #    tile_list.append(t_tuple)
                #print(tile_list)
                pos_list = []
                sn_tuple = (sn_row, sn_col)
                orig_sn_tuple = sn_tuple
                #print(sn_tuple)
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
                            #print("Space found!")
                            break
                        elif (sn_tile == '#'):
                            pos_list = []
                            #print("Wall found!")
                            break
                    else:
                        break

                # Move tiles
                #print(pos_list)
                if (len(pos_list)):
                    for pos in pos_list:
                        grid_dict[pos] = 'O'
                    grid_dict[n_tuple] = '@'
                    robot_pos = [n_tuple[0], n_tuple[1]]
                    grid_dict[old_tuple] = '.'

                # Check tiles
                #for t in tile_list:
                #    tile = grid_dict[t]
                #    if (tile == '.'):
                #        counter += 1
                #    else:
                #        break

                ## Move tiles up to counter
                #for i in range(0, counter):
                #    pos = tile_list[i]
                #    grid_dict[pos] = 'O'

                #if (counter):
                #    grid_dict[n_tuple] = '@'
                #    grid_dict[old_tuple] = '.'

                #sn_tuple = (sn_row, sn_col)
                #sn_tile = grid_dict[sn_tuple]

                #if (sn_tile == '.'): # move
                #    grid_dict[sn_tuple] = 'O'
                #    grid_dict[n_tuple] = '@'
                #    grid_dict[old_tuple] = '.'
            #elif (n_tile == '#'): # nothing happens

        # One move ended, so print
        #if (idx < 5):
        #print(f'Move {move}:')
        #for row in range(0, MAX_ROW+1):
        #    for col in range(0, MAX_COL+1):
        #        if ((row, col) in grid_dict):
        #            print(grid_dict[(row, col)], end="")

        #    print()
                
    # GPS
    for pos in grid_dict:
        row, col = pos
        tile = grid_dict[pos]

        if (tile == 'O'):
            output += row*100 + col
    
    return output

def process_inputs2(in_file):
    global visited
    global grid_dict
    output = 0

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
                #row_list = [x for x in range(sn_row, MAX_ROW+1)]
                #col_list = [x for x in range(sn_col, MAX_COL+1)]
                #min_dist = min(len(row_list), len(col_list))
                #tile_list = []
                #new_tile_list = []
                #for i in range(0, min_dist):
                #    t_tuple = (row_list[i], col_list[i])
                #    tile_list.append(t_tuple)
                #print(tile_list)
                pos_list = []
                sn_tuple = (sn_row, sn_col)
                orig_sn_tuple = sn_tuple
                #print(sn_tuple)
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
                                #print("Space found!")
                                break
                            elif (sn_tile == '#'):
                                pos_list = []
                                #print("Wall found!")
                                break
                        elif (move in "^v"):
                            break
                            #side_sn_tile = grid_dict[side_sn_tuple]
                            ## BUG!!! TODO: fix
                            #if ((side_mod == 1) and (sn_tile == '[') and (side_sn_tile == ']')) or ((side_mod == -1) and (sn_tile == ']') and (side_sn_tile == '[')): # valid
                            #    pos_list.append(sn_tuple)
                            #    side_pos_list.append(side_sn_tuple)
                            #    side_sn_row, side_sn_col = side_sn_tuple
                            #    sn_tuple = (sn_row+modifier, sn_col)
                            #    side_sn_tuple = (side_sn_row+modifier, side_sn_col)
                            #elif (sn_tile == '.') and (side_sn_tile == '.'):
                            #    pos_list.append(sn_tuple)
                            #    side_pos_list.append(side_sn_tuple)
                            #    break
                            #else:
                            #    pos_list = []
                            #    side_post_list = []
                            #    break
                    else:
                        break

                # Move tiles
                #print(pos_list)
                #print(side_pos_list) # Correct
                visited = []
                if (len(pos_list)) and (move in "><"):
                    #for pos in pos_list:
                    #    grid_dict[pos] = '[' # TODO
                    pos_list.reverse()
                    for pos in pos_list:
                        row, col = pos
                        grid_dict[pos] = grid_dict[(row, col-modifier)]
                    grid_dict[n_tuple] = '@'
                    robot_pos = [n_tuple[0], n_tuple[1]]
                    grid_dict[old_tuple] = '.'
                elif (move in "^v") and can_move(n_tuple, move):
                    #pos_list.reverse()
                    #side_pos_list.reverse() # DEBUG
                    #for idx, pos in enumerate(pos_list):
                    #    side_pos = side_pos_list[idx]
                    #    row, col = pos
                    #    side_row, side_col = side_pos
                    #    grid_dict[pos] = grid_dict[(row-modifier, col)]
                    #    grid_dict[side_pos] = grid_dict[(side_row-modifier, side_col)]

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
                        #print(f'{v} is tile {tile}, so modify {(row+modifier, col)}')
                        grid_dict[(row+modifier, col)] = tile
                        grid_dict[v] = '.'

                    grid_dict[n_tuple] = '@'
                    robot_pos = [n_tuple[0], n_tuple[1]]
                    grid_dict[old_tuple] = '.'

                    # Adjust side of @
                    grid_dict[(n_tuple[0], n_tuple[1]+side_mod)] = '.'

                # Check tiles
                #for t in tile_list:
                #    tile = grid_dict[t]
                #    if (tile == '.'):
                #        counter += 1
                #    else:
                #        break

                ## Move tiles up to counter
                #for i in range(0, counter):
                #    pos = tile_list[i]
                #    grid_dict[pos] = 'O'

                #if (counter):
                #    grid_dict[n_tuple] = '@'
                #    grid_dict[old_tuple] = '.'

                #sn_tuple = (sn_row, sn_col)
                #sn_tile = grid_dict[sn_tuple]

                #if (sn_tile == '.'): # move
                #    grid_dict[sn_tuple] = 'O'
                #    grid_dict[n_tuple] = '@'
                #    grid_dict[old_tuple] = '.'
            #elif (n_tile == '#'): # nothing happens

        # Assertion
        # Check if boxes are still correct
        #assertion_pass = True
        #for pos in grid_dict:
        #    row, col = pos
        #    tile = grid_dict[pos]

        #    if (tile == '[') and (grid_dict[(row, col+1)] != ']'):
        #        assertion_pass = False
        #        break
        #    if (tile == ']') and (grid_dict[(row, col-1)] != '['):
        #        assertion_pass = False
        #        break

        # One move ended, so print
        #if (assertion_pass):
        #    continue
        ##if ((idx_m+1) in [4000, 4001]):
        #print(f'Move {move}: {idx_m+1} of {len(moves_list)}')
        #for row in range(0, MAX_ROW+1):
        #    for col in range(0, MAX_COL+1):
        #        if ((row, col) in grid_dict):
        #            print(grid_dict[(row, col)], end="")

        #    print()
        #for i in range(0, 11):
        #    print()
        #if (not assertion_pass):
        #    print("Assertion failed!")
        #    break
                
    # GPS
    for pos in grid_dict:
        row, col = pos
        tile = grid_dict[pos]

        if (tile == '['):
            output += row*100 + col
    
    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)  # Check line 7085
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
#part2_example4 = process_inputs2(example4_file)
part2 = process_inputs2(input_file)

#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
#print(f'Part 2 example4: {part2_example4}')
print(f'Part 2: {part2}')
