import math

input_file = "input21.txt"
example_file = "example21.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def update_plot_dict(plot_dict, rc_tuple):
    if (rc_tuple in plot_dict) and (plot_dict[rc_tuple] != 0):
        plot_dict[rc_tuple] = 0
    elif (rc_tuple not in plot_dict):
        plot_dict[rc_tuple] = 0

def update_neighbors(plot_dict, rock_set, r, c):
    UP = (r-1, c)
    DOWN = (r+1, c)
    LEFT = (r, c-1)
    RIGHT = (r, c+1)

    if (UP not in rock_set):
        update_plot_dict(plot_dict, UP)
    if (DOWN not in rock_set):
        update_plot_dict(plot_dict, DOWN)
    if (LEFT not in rock_set):
        update_plot_dict(plot_dict, LEFT)
    if (RIGHT not in rock_set):
        update_plot_dict(plot_dict, RIGHT)

def update_neighbors2(plot_dict, rock_set, r, c, MAX_ROWS, MAX_COLS):
    UP    = ((r-1) % MAX_ROWS, (c  ) % MAX_COLS)
    DOWN  = ((r+1) % MAX_ROWS, (c  ) % MAX_COLS)
    LEFT  = ((r  ) % MAX_ROWS, (c-1) % MAX_COLS)
    RIGHT = ((r  ) % MAX_ROWS, (c+1) % MAX_COLS)

    if (UP not in rock_set):
        update_plot_dict(plot_dict, UP)
    if (DOWN not in rock_set):
        update_plot_dict(plot_dict, DOWN)
    if (LEFT not in rock_set):
        update_plot_dict(plot_dict, LEFT)
    if (RIGHT not in rock_set):
        update_plot_dict(plot_dict, RIGHT)

def process_inputs(in_file):
    output = 0

    init_grid = []
    with open(in_file) as file:
        line = file.readline()
 
        while line:
            line = line.strip()

            init_grid.append([x for x in line])

            line = file.readline()

    rock_set = set()

    for r, row in enumerate(init_grid):
        for c, plot in enumerate(row):
            if (plot == '#'):
                rock_set.add((r, c))
            elif (plot == 'S'):
                start = (r, c)

    queue = []
    visited = set()

    r, c = start
    step = 0
    MAX_STEPS = 64
    plot_dict = {}
    plot_dict[start] = 0
    for s in range(0, MAX_STEPS):
        queue = []
        print(f'Step {s}')

        for p in plot_dict:
            if plot_dict[p] == 0:
                plot_dict[p] = -1
                queue.append(p)

        for q in queue:
            r, c = q
            update_neighbors(plot_dict, rock_set, r, c)

        #UP = (r-1, c)
        #DOWN = (r+1, c)
        #LEFT = (r, c-1)
        #RIGHT = (r, c+1)

        #new_s = s + 1
        #if UP not in rock_set:
        #    new_r, new_c = UP
        #    update_plot_dict(plot_dict, UP)
        #    queue.append((new_r, new_c, new_s))
        #if DOWN not in rock_set:
        #    new_r, new_c = DOWN
        #    update_plot_dict(plot_dict, DOWN)
        #    queue.append((new_r, new_c, new_s))
        #if LEFT not in rock_set:
        #    new_r, new_c = LEFT
        #    update_plot_dict(plot_dict, LEFT)
        #    queue.append((new_r, new_c, new_s))
        #if RIGHT not in rock_set:
        #    new_r, new_c = RIGHT
        #    update_plot_dict(plot_dict, RIGHT)
        #    queue.append((new_r, new_c, new_s))
        #visited.add((r, c))

    plots = 0
    for p in plot_dict:
        if (plot_dict[p] == 0):
            plots += 1

    output = plots

    return output

def process_inputs2(in_file):
    output = 0

    init_grid = []
    with open(in_file) as file:
        line = file.readline()
 
        while line:
            line = line.strip()

            init_grid.append([x for x in line])

            line = file.readline()

    # Original height and width
    HEIGHT = len(init_grid)
    WIDTH = len(init_grid[0])

    orig_start = (int((HEIGHT-1)/2), int((WIDTH-1)/2))
    init_grid[orig_start[0]][orig_start[1]] = '.'

    NEW_HEIGHT = 5*HEIGHT
    NEW_WIDTH = 5*WIDTH

    # Dynamic programming:
    # Extend the whole map to 5x5 version
    grid = []
    for c in range(0, NEW_HEIGHT):
        orig_row = init_grid[c % HEIGHT]
        grid.append(orig_row + orig_row + orig_row + orig_row + orig_row)

    grid[int((NEW_HEIGHT-1)/2)][int((NEW_WIDTH-1)/2)] = 'S'
    rock_set = set()

    for r, row in enumerate(grid):
        for c, plot in enumerate(row):
            if (plot == '#'):
                rock_set.add((r, c))
            elif (plot == 'S'):
                start = (r, c)

    # Solve steps for 5x5 map first
    queue = []
    visited = set()

    r, c = start
    step = 0
    MAX_STEPS = orig_start[0] + 2*HEIGHT
    plot_dict = {}
    plot_dict[start] = 0
    on_dict = {}
    off_dict = {}
    for s in range(0, MAX_STEPS):
        queue = []
        #print(f'Step {s}/{MAX_STEPS-1}')

        for p in plot_dict:
            if plot_dict[p] == 0:
                plot_dict[p] = -1
                queue.append(p)

        for q in queue:
            r, c = q
            update_neighbors(plot_dict, rock_set, r, c)

    # Check each map in the 5x5 extended grid:
    # -A2B-
    # A617B
    # 51013
    # D918C
    # -D4C-
    # 0: center/start map
    # 1: north adjacent map
    #    west adjacent map
    #    east adjacent map
    #    south adjacent map
    # 2: northernmost map
    # 3: easternmost map
    # 4: southernmost map
    # 5: westernmost map
    # 6: northwest inner diagonal
    # 7: northeast inner diagonal
    # 8: southeast inner diagonal
    # 9: southwest inner diagonal
    # A: northwest outer diagonal
    # B: northeast outer diagonal
    # C: southeast outer diagonal
    # D: southwest outer diagonal
    # map_dict contains [(min_r, min_c), (max_r, max_c)] for each map
    map_dict = {'0' : [(int(2*HEIGHT), int(2*WIDTH)), (int(3*HEIGHT-1), int(3*WIDTH-1))],
                '1' : [(int(1*HEIGHT), int(2*WIDTH)), (int(2*HEIGHT-1), int(3*WIDTH-1))],
                '2' : [(int(0       ), int(2*WIDTH)), (int(1*HEIGHT-1), int(3*WIDTH-1))],
                '3' : [(int(2*HEIGHT), int(4*WIDTH)), (int(3*HEIGHT-1), int(5*WIDTH-1))],
                '4' : [(int(4*HEIGHT), int(2*WIDTH)), (int(5*HEIGHT-1), int(3*WIDTH-1))],
                '5' : [(int(2*HEIGHT), int(0      )), (int(3*HEIGHT-1), int(1*WIDTH-1))],
                '6' : [(int(1*HEIGHT), int(1*WIDTH)), (int(2*HEIGHT-1), int(2*WIDTH-1))],
                '7' : [(int(1*HEIGHT), int(3*WIDTH)), (int(2*HEIGHT-1), int(4*WIDTH-1))],
                '8' : [(int(3*HEIGHT), int(3*WIDTH)), (int(4*HEIGHT-1), int(4*WIDTH-1))],
                '9' : [(int(3*HEIGHT), int(1*WIDTH)), (int(4*HEIGHT-1), int(2*WIDTH-1))],
                'A' : [(int(0       ), int(1*WIDTH)), (int(1*HEIGHT-1), int(2*WIDTH-1))],
                'B' : [(int(0       ), int(3*WIDTH)), (int(1*HEIGHT-1), int(4*WIDTH-1))],
                'C' : [(int(4*HEIGHT), int(3*WIDTH)), (int(5*HEIGHT-1), int(4*WIDTH-1))],
                'D' : [(int(4*HEIGHT), int(1*WIDTH)), (int(5*HEIGHT-1), int(2*WIDTH-1))],
               }
    count_dict = {}

    for m in map_dict:
        count = 0
        min_coord, max_coord = map_dict[m]
        min_r, min_c = min_coord
        max_r, max_c = max_coord

        for r in range(min_r, max_r+1):
            for c in range(min_c, max_c+1):
                if ((r, c) in plot_dict) and (plot_dict[(r, c)] == 0):
                    count += 1

        count_dict[m] = count

    plots = 0
    for p in plot_dict:
        if (plot_dict[p] == 0):
            plots += 1

    # DEBUGGING: Solving only for 5x5 map
    #computed_plots = 0
    #for m in count_dict:
    #    if (m == '1'):
    #        factor = 4
    #    elif (m in ['A', 'B', 'C', 'D']):
    #        factor = 2
    #    else:
    #        factor = 1
    #    computed_plots += factor*count_dict[m]
    #print(f'Plots: {plots}')
    #print(f'Computed plots: {computed_plots}')

    PART2_STEPS = 26501365
    n = math.floor((PART2_STEPS + orig_start[0])/WIDTH)
    print(f'Height: {HEIGHT}')
    print(f'Width : {WIDTH}')
    print(f'Horizontal frontier: {(PART2_STEPS + orig_start[1]) % WIDTH}')
    print(f'Vertical frontier: {(PART2_STEPS + orig_start[0]) % HEIGHT}')
    print(f'No. of maps to the north: {n}')
    print(f'No. of maps to the east: {math.floor((PART2_STEPS + orig_start[1])/WIDTH)}')

    # Compute completed maps first
    computed_plots = 0
    middle_complete_map = 2*n-1
    for complete_map in range(1, middle_complete_map, 2):
        # Assumes n is even
        pattern1 = math.ceil(complete_map/2)
        pattern0 = complete_map - pattern1

        computed_plots += pattern1*count_dict['1'] + pattern0*count_dict['0']

    pattern1 = math.ceil(middle_complete_map/2)
    pattern0 = middle_complete_map - pattern1
    computed_plots = 2*computed_plots + pattern1*count_dict['1'] + pattern0*count_dict['0']

    # Compute borders
    computed_plots += count_dict['2'] + count_dict['3'] + count_dict['4'] + count_dict['5']
    computed_plots += (n-1)*(count_dict['6'] + count_dict['7'] + count_dict['8'] + count_dict['9'])
    computed_plots += n*(count_dict['A'] + count_dict['B'] + count_dict['C'] + count_dict['D'])

    output = computed_plots

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
