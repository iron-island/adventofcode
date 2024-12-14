import numpy as np

input_file = "input14.txt"
example_file = "example14.txt"

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

            row = [x for x in line]
            grid.append(row)

            line = file.readline()

    # add to last row
    last_row = "#"*len(grid[0])
    row = [x for x in last_row]
    grid.append(row)

    print("Before tilting")
    for g in grid:
        print(g)

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
    
    print("After tilting")
    for g in grid:
        print(''.join(g))

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            tile = grid[r][c]

            if (tile == 'O'):
                output = output + (len(grid) - r - 1)

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

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

# Answer was manually computed
print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
