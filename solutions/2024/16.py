from collections import defaultdict

input_file = "../../inputs/2024/input16.txt"
example_file = "example16.txt"
example2_file = "example16_2.txt"
example3_file = "example16_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    grid_dict = defaultdict(str)
    cost_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
        row = 0
        INIT_COST = 1000000000000
        while line:
            line = line.strip()
            MAX_COL = len(line)-1
            for col, tile in enumerate(line):
                grid_dict[(row, col)] = tile
                for direction in ["up", "down", "left", "right"]:
                    cost_dict[(row, col, direction)] = [INIT_COST, None]

                if (tile == 'S'):
                    S_pos = (row, col)
                    S_dir = "right"
                elif (tile == 'E'):
                    E_pos = (row, col)
            row += 1
            
            line = file.readline()

        MAX_ROW = row-1

    # Dijkstra's
    q = []
    visited = set()
    E_visited_dict = {"up": False, "right": False}
    n_tuple = (0, S_pos[0], S_pos[1], "right")
    q.append(n_tuple)
    while (len(q)):
        # Priority queue
        q.sort()
        cost, row, col, direction = q.pop(0)
        #if (cost > 1000):
        #    print(cost)

        # TODO: check if this is always applicable? what if new path with lesser cost was found?
        if ((row, col, direction) in visited):
            cost_last, last_tuple = cost_dict[(row, col, direction)]
            last_row, last_col, last_dir = last_tuple
            #print("Already visited!")
            continue
            #if (cost > cost_last):
            #    #print("Continue!")
            #    continue
            #else:
            #    print("DEBUG!")

        visited.add((row, col, direction))

        #if (grid_dict[(row, col)] == 'E'):
        #    if (direction in ["up", "right"]):
        #        E_visited_dict[direction] = True

        #    if (E_visited_dict["up"] and E_visited_dict["right"]):
        #        break

        # up
        n_row = row-1
        n_col = col
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "up"):
                n_cost = cost
            elif (direction == "right") or (direction == "left"):
                n_cost = cost + 1000
            elif (direction == "down"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "up"

            n_cost_last, _ = cost_dict[(n_row, n_col, n_dir)]
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, (row, col, direction)]

        # down
        n_row = row+1
        n_col = col
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "down"):
                n_cost = cost
            elif (direction == "right") or (direction == "left"):
                n_cost = cost + 1000
            elif (direction == "up"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "down"

            n_cost_last, _ = cost_dict[(n_row, n_col, n_dir)]
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, (row, col, direction)]

        # left
        n_row = row
        n_col = col-1
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "left"):
                n_cost = cost
            elif (direction == "up") or (direction == "down"):
                n_cost = cost + 1000
            elif (direction == "right"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "left"

            n_cost_last, _ = cost_dict[(n_row, n_col, n_dir)]
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, (row, col, direction)]

        # right
        n_row = row
        n_col = col+1
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "right"):
                n_cost = cost
            elif (direction == "up") or (direction == "down"):
                n_cost = cost + 1000
            elif (direction == "left"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "right"

            n_cost_last, _ = cost_dict[(n_row, n_col, n_dir)]
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, (row, col, direction)]

    # Evaluate
    output = INIT_COST
    for cost_tuple in cost_dict:
        row, col, direction = cost_tuple

        tile = grid_dict[(row, col)]

        if (tile == 'E'):
            cost, pos = cost_dict[cost_tuple]
            #print(cost, pos)
            output = min(output, cost)
            #print(output)

            if (output == cost):
                E_tuple = cost_tuple

    # Debugging
    row, col, direction = E_tuple
    while (True):
        cost, last_tile = cost_dict[(row, col, direction)]

        row, col, direction = last_tile

        if (grid_dict[(row, col)] == 'S'):
            break

        if (direction == "up"): 
            tile = '^'
        elif (direction == "down"):
            tile = 'v'
        elif (direction == "left"):
            tile = '<'
        elif (direction == "right"):
            tile = '>'

        grid_dict[(row, col)] = tile
    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        print(grid_dict[(row, col)], end="")
    #    print()

    return output

def process_inputs2(in_file):
    output = 0

    grid_dict = defaultdict(str)
    cost_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
        row = 0
        INIT_COST = 1000000000000
        while line:
            line = line.strip()
            MAX_COL = len(line)-1
            for col, tile in enumerate(line):
                grid_dict[(row, col)] = tile
                for direction in ["up", "down", "left", "right"]:
                    cost_dict[(row, col, direction)] = [INIT_COST, []]

                if (tile == 'S'):
                    S_pos = (row, col)
                    S_dir = "right"
                elif (tile == 'E'):
                    E_pos = (row, col)
            row += 1
            
            line = file.readline()

        MAX_ROW = row-1

    # Dijkstra's
    q = []
    visited = set()
    E_visited_dict = {"up": False, "right": False}
    n_tuple = (0, S_pos[0], S_pos[1], "right")
    q.append(n_tuple)
    while (len(q)):
        # Priority queue
        q.sort()
        cost, row, col, direction = q.pop(0)
        #if (cost > 1000):
        #    print(cost)

        # TODO: check if this is always applicable? what if new path with lesser cost was found?
        if ((row, col, direction) in visited):
            continue

        visited.add((row, col, direction))

        #if (grid_dict[(row, col)] == 'E'):
        #    if (direction in ["up", "right"]):
        #        E_visited_dict[direction] = True

        #    if (E_visited_dict["up"] and E_visited_dict["right"]):
        #        break

        # up
        n_row = row-1
        n_col = col
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "up"):
                n_cost = cost
            elif (direction == "right") or (direction == "left"):
                n_cost = cost + 1000
            elif (direction == "down"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "up"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            #if (n_row, n_col, n_dir) == (6, 15, "up"):
            #    print("DEBUG!")
            #    print(n_cost, n_cost_last)
            #    print(n_row, n_col, n_dir)
            #assert(prev_tile_list != None)
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

        # down
        n_row = row+1
        n_col = col
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "down"):
                n_cost = cost
            elif (direction == "right") or (direction == "left"):
                n_cost = cost + 1000
            elif (direction == "up"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "down"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            #assert(prev_tile_list != None)
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

        # left
        n_row = row
        n_col = col-1
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "left"):
                n_cost = cost
            elif (direction == "up") or (direction == "down"):
                n_cost = cost + 1000
            elif (direction == "right"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "left"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            #assert(prev_tile_list != None)
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

        # right
        n_row = row
        n_col = col+1
        n_tuple = (n_row, n_col)
        if (grid_dict[n_tuple] != '#'):
            if (direction == "right"):
                n_cost = cost
            elif (direction == "up") or (direction == "down"):
                n_cost = cost + 1000
            elif (direction == "left"):
                n_cost = cost + 2000
            n_cost = n_cost+1
            n_dir = "right"

            n_cost_last, prev_tile_list = cost_dict[(n_row, n_col, n_dir)]
            if (prev_tile_list == None):
                prev_tile_list = []
            #assert(prev_tile_list != None)
            if (n_cost < n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, [(row, col, direction)]]
            elif (n_cost == n_cost_last):
                q.append((n_cost, n_row, n_col, n_dir))
                prev_tile_list.append((row, col, direction))
                cost_dict[(n_row, n_col, n_dir)] = [n_cost, prev_tile_list]

    # Evaluate
    output = INIT_COST
    for cost_tuple in cost_dict:
        row, col, direction = cost_tuple

        tile = grid_dict[(row, col)]

        if (tile == 'E'):
            cost, pos_list = cost_dict[cost_tuple]
            #print(cost, pos_list)
            output = min(output, cost)
            #print(output)

            if (output == cost):
                E_tuple = cost_tuple
                last_tile_list = pos_list

    # Debugging
    row, col, direction = E_tuple
    output_set = set()
    output_set.add((row, col))
    #print(last_tile_list)
    q = []
    q.append((row, col, direction))
    while (True):
        row, col, direction = q.pop(0)
        output_set.add((row, col))
        if (grid_dict[(row, col)] == 'S'):
            break

        cost, last_tile_list = cost_dict[(row, col, direction)]
        #print(row, col, direction, cost, last_tile_list)
        for last_tile in last_tile_list:
            last_row, last_col, last_dir = last_tile
            q.append((last_row, last_col, last_dir))
            #if (last_tile != None):
            #    row, col, direction = last_tile
            #    output_set.add((row, col))
            #else:
            #    break

            #if (direction == "up"): 
            #    tile = '^'
            #elif (direction == "down"):
            #    tile = 'v'
            #elif (direction == "left"):
            #    tile = '<'
            #elif (direction == "right"):
            #    tile = '>'

            #grid_dict[(row, col)] = tile
    output = len(output_set)
    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        print(grid_dict[(row, col)], end="")
    #    print()

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file) # 12048 initial, expected is 11048
#part1_example3 = process_inputs(example3_file)
part1 = process_inputs(input_file) # 122571 too high

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 16: Reindeer Maze ---")
#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
