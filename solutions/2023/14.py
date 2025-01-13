#import numpy as np
from collections import defaultdict

input_file = "../../inputs/2023/input14.txt"
example_file = "example14.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def print_grid(grid):
    MAX_ROW = len(grid)-1
    MAX_COL = len(grid[0])-1

    for row in range(0, MAX_ROW+1):
        for col in range(0, MAX_COL+1):
            print(grid[row][col], end="")

        print("")

def process_inputs(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            row = [x for x in line]
            grid.append(row)

            line = file.readline()

    # add to last row
    LEN_GRID = len(grid[0])
    row = ["#"]*LEN_GRID
    grid.append(row)

    #print("Before tilting")
    #for g in grid:
    #    print(g)

    #static_coords = []
    #rock_count = [0]*LEN_GRID
    for c in range(0, LEN_GRID):
        col_rocks = 0
        last_static_r = -1
        num_static = 0
        for r, row in enumerate(grid):
            tile = grid[r][c]
            # If a cube-shaped rock is encountered,
            #   move all the rounded rocks counted so far up to the 
            #   last encountered cube-shaped rock
            if (tile == '#'):
                #static_coords.append((r, c))

                for i in range(last_static_r+1, r):
                    if (col_rocks):
                        grid[i][c] = 'O'
                        col_rocks -= 1
                    else:
                        grid[i][c] = '.'

                last_static_r = r
            # Count rounded rocks encountered so far
            elif (tile == 'O'):
                #rock_count[c] += 1
                col_rocks += 1
    
    #print("After tilting")
    #for g in grid:
    #    print(''.join(g))

    GRID_HEIGHT = len(grid)
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if (grid[r][c] == 'O'):
                output = output + (GRID_HEIGHT - r - 1)

    return output

def process_inputs2(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            row = [x for x in line]
            grid.append(row)

            line = file.readline()


    print("Before tilting")
    for g in grid:
        print(g)

    grid = np.array(grid)

    #for cycle in range(3, -1, -1):
    grid_cache = {}
    orientation_dict = {0: 'N', 1: 'W', 2: 'E', 3: 'S'}
    CYCLES = 1000000000
    for cycle in range(0, CYCLES):
        if (cycle % 100000 == 0):
            print(f'Cycle {cycle}...')
    
        for o in range(0, 4):
            #if ((grid.tobytes(), cycle % 4) in grid_cache):
            #    print(f'In cache at cycle {cycle}!')
            #    return

            # add to last row
            last_row = "#"*len(grid[0])
            row = [x for x in last_row]
            #grid.append(row)
            grid = np.vstack((grid, row))

            static_coords = []
            rock_str = "0"*len(grid[0])
            rock_count = [int(x) for x in rock_str]
            for c in range(0, len(grid[0])):
                col_rocks = 0
                last_static_r = -1
                num_static = 0
                for r, row in enumerate(grid):
                    tile = grid[r][c]
                    if (tile == '#'):
                        static_coords.append((r, c))

                        for i in range(last_static_r+1, r):
                            if (col_rocks):
                                grid[i][c] = 'O'
                                col_rocks -= 1
                            else:
                                grid[i][c] = '.'

                        last_static_r = r
                    elif (tile == 'O'):
                        rock_count[c] += 1
                        col_rocks += 1


            # Remove last row
            grid = grid[:-1, :]

            # Tilt
            grid = np.rot90(grid, 3)

        # Add to last row
        last_row = "#"*len(grid[0])
        row = [x for x in last_row]
        #grid.append(row)
        grid = np.vstack((grid, row))

        # Calculate load
        int_out = 0
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                tile = grid[r][c]

                if (tile == 'O'):
                    int_out += (len(grid) - r - 1)

        # Remove last row
        grid = grid[:-1, :]

        gridkey = int_out
        if (gridkey in grid_cache):
            print(f'Already in cache! cycle {cycle}: {int_out}')
            print(grid_cache.keys())
        else:
            grid_cache[gridkey] = grid

        #print(f'After {cycle+1} cycles:')
        #for g in grid:
        #    print(''.join(g))

    # Add to last row
    last_row = "#"*len(grid[0])
    row = [x for x in last_row]
    #grid.append(row)
    grid = np.vstack((grid, row))
    
    # Calculate load
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            tile = grid[r][c]

            if (tile == 'O'):
                output = output + (len(grid) - r - 1)

    return output

def process_inputs_part1_2(in_file):
    grid = []
    with open(in_file) as file:
        line = file.readline()
   
        row = 0
        while line:
            line = line.strip()

            # Append to first row, considering padding at left and right side
            if (row == 0):
                LEN_GRID = len(line) + 2
                rowline = ["#"]*LEN_GRID
                grid.append(rowline)

            # Pad to the left and right before adding to grid
            rowline = [x for x in line]
            padded_rowline = ["#"] + rowline + ["#"]
            grid.append(padded_rowline)

            row += 1

            line = file.readline()

    # Pad last row
    rowline = ["#"]*LEN_GRID
    grid.append(rowline)
    GRID_HEIGHT = len(grid)

    # Run cycles with pattern checking to shortcut simulating cycles
    cycle = 0
    part1 = 0
    load_dict = defaultdict(list)
    for i in range(0, 1000000000):
        # North tilt
        for c in range(0, LEN_GRID):
            col_rocks = 0
            last_static_r = -1
            for r in range(0, GRID_HEIGHT):
                tile = grid[r][c]
                # If a cube-shaped rock is encountered,
                #   move all the rounded rocks counted so far up to the 
                #   last encountered cube-shaped rock
                if (tile == '#'):
                    for i in range(last_static_r+1, r):
                        if (col_rocks):
                            grid[i][c] = 'O'
                            col_rocks -= 1
                        else:
                            grid[i][c] = '.'

                    last_static_r = r
                # Count rounded rocks encountered so far
                elif (tile == 'O'):
                    col_rocks += 1

        # On north tilt of cycle 1, get load for Part 1
        if not (part1):
            for r, row in enumerate(grid):
                for c, col in enumerate(row):
                    if (grid[r][c] == 'O'):
                        part1 = part1 + (GRID_HEIGHT - r - 1)

        # West tilt: similar to North tilt but iterating for row for column starting from left to right
        for r in range(0, GRID_HEIGHT):
            row_rocks = 0
            last_static_c = -1
            for c in range(0, LEN_GRID):
                tile = grid[r][c]

                # If a cube-shaped rock is encountered,
                #   move all the rounded rocks counted so far west to the 
                #   last encountered cube-shaped rock
                if (tile == '#'):
                    for i in range(last_static_c+1, c):
                        if (row_rocks):
                            grid[r][i] = 'O'
                            row_rocks -= 1
                        else:
                            grid[r][i] = '.'

                    last_static_c = c
                # Count rounded rocks encountered so far
                elif (tile == 'O'):
                    row_rocks += 1

        # South tilt: similar to North tilt but starting at bottom-most row
        for c in range(0, LEN_GRID):
            col_rocks = 0
            last_static_r = GRID_HEIGHT
            for r in range(GRID_HEIGHT-1, -1, -1):
                tile = grid[r][c]
                # If a cube-shaped rock is encountered,
                #   move all the rounded rocks counted so far down to the 
                #   last encountered cube-shaped rock
                if (tile == '#'):
                    for i in range(last_static_r-1, r, -1):
                        if (col_rocks):
                            grid[i][c] = 'O'
                            col_rocks -= 1
                        else:
                            grid[i][c] = '.'

                    last_static_r = r
                # Count rounded rocks encountered so far
                elif (tile == 'O'):
                    col_rocks += 1

        # East tilt: similar to North tilt but iterating for row for column from right to left
        for r in range(0, GRID_HEIGHT):
            row_rocks = 0
            last_static_c = LEN_GRID
            for c in range(LEN_GRID-1, -1, -1):
                tile = grid[r][c]

                # If a cube-shaped rock is encountered,
                #   move all the rounded rocks counted so far east to the 
                #   last encountered cube-shaped rock
                if (tile == '#'):
                    for i in range(last_static_c-1, c, -1):
                        if (row_rocks):
                            grid[r][i] = 'O'
                            row_rocks -= 1
                        else:
                            grid[r][i] = '.'

                    last_static_c = c
                # Count rounded rocks encountered so far
                elif (tile == 'O'):
                    row_rocks += 1

        # Get load
        load = 0
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if (grid[r][c] == 'O'):
                    load += (GRID_HEIGHT - r - 1)
        cycle += 1
        if (cycle == 1000000000):
            part2 = load
            break

        # Check for pattern
        load_dict[load].append(cycle)
        load_cycles_list = load_dict[load]
        # Consider as a pattern if a period is found based on the current cycle
        #   and last 3 previous cycle occurrences of the load
        # Last 2 is enough for my input, while example requires last 3 so
        #   use that instead
        if (len(load_cycles_list) >= 4):
            last1 = load_cycles_list[-2]
            last2 = load_cycles_list[-3]
            last3 = load_cycles_list[-4]
            period = cycle - last1
            if (period == (last1 - last2)) and (period == (last2 - last3)):
                # Shortcut to cycle nearest to 1000000000 based on period
                prev_cycle = cycle
                cycle += int((1000000000 - cycle)/period)*period

                # Immediately check to prevent overshooting
                if (cycle == 1000000000):
                    part2 = load
                    break

    return part1, part2

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2 = process_inputs2(input_file)

#part1, part2 = process_inputs_part1_2(example_file)
part1, part2 = process_inputs_part1_2(input_file)

# Answer was manually computed
#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
