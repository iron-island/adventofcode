input_file = "../../inputs/2023/input11.txt"
example_file = "example11.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    grid = []
    expanded_row_grid = []
    expanded_grid = []
    init_num_cols = 0
    num_galaxies = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_list = [x for x in line]
            num_galaxies += line_list.count('#')

            init_num_cols = len(line_list)
            grid.append(line_list)

            expanded_row_grid.append(line_list)
            expanded_grid.append([])

            if ('#' not in line):
                expanded_row_grid.append(line_list)
                expanded_grid.append([])

            line = file.readline()

    # Expand columns
    space = None
    init_num_rows = len(expanded_row_grid)
    final_num_cols = init_num_cols
    for c in range(0, init_num_cols):
        expand = True
        for r in range(0, len(expanded_row_grid)):
            space = expanded_row_grid[r][c]
            if space == '#':
                expand = False

            expanded_grid[r].append(space)

        if (expand):
            final_num_cols += 1
            for r in range(0, init_num_rows):
                expanded_grid[r].append('.')

    # Galaxy coordinates
    cnt = 1
    galaxy_dict = {}
    final_num_rows = init_num_rows
    for r in range(0, init_num_rows):
        for c in range(0, final_num_cols):
            space = expanded_grid[r][c]
            if space == '#':
                galaxy_dict[cnt] = (r, c)
                cnt += 1

    galaxy_list = [x for x in range(1, num_galaxies+1)]
    pair_list = [(x, y) for idx, x in enumerate(galaxy_list) for y in galaxy_list[idx+1:]]

    for pair in pair_list:
        x, y = pair

        galaxy1_r, galaxy1_c = galaxy_dict[x]
        galaxy2_r, galaxy2_c = galaxy_dict[y]

        output = output + abs(galaxy1_r - galaxy2_r) + abs(galaxy1_c - galaxy2_c)

    return output

def process_inputs2(in_file, offset):
    output = 0

    grid = []
    init_num_cols = 0
    num_galaxies = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_list = [x for x in line]
            num_galaxies += line_list.count('#')

            init_num_cols = len(line_list)
            grid.append(line_list)

            line = file.readline()

    # Galaxy coordinates
    cnt = 1
    galaxy_dict = {}
    init_num_rows = len(grid)
    for r in range(0, init_num_rows):
        for c in range(0, init_num_cols):
            space = grid[r][c]
            if space == '#':
                galaxy_dict[cnt] = (r, c)
                cnt += 1

    print('Before expansion:')
    print(galaxy_dict)

    # Row expansion
    row_offset = offset
    expanded_row_dict = {}

    for g in galaxy_dict:
        expanded_row_dict[g] = 0

    for idx, row in enumerate(grid):
        if (row.count('#') == 0):

            for g in galaxy_dict:
                gr, gc = galaxy_dict[g]

                #if (gr > idx):
                if (gr - expanded_row_dict[g]*row_offset) > idx:
                    galaxy_dict[g] = (gr + row_offset, gc)
                    expanded_row_dict[g] = expanded_row_dict[g] + 1

    # Column expansion
    col_offset = offset
    expanded_col_dict = {}

    for g in galaxy_dict:
        expanded_col_dict[g] = 0

    for c in range(0, init_num_cols):
        expand = True
        for r in range(0, init_num_rows):
            space = grid[r][c]
            if (space == '#'):
                expand = False

        if expand:
            print(f'Expand due to column {c}')
            for g in galaxy_dict:
                gr, gc = galaxy_dict[g]

                if (gc - expanded_col_dict[g]*col_offset) > c:
                    #print(f'Expaned galaxy {g} from {gr}, {gc} to {gr}, {gc+col_offset}')
                    galaxy_dict[g] = (gr, gc + col_offset)
                    expanded_col_dict[g] = expanded_col_dict[g] + 1

    galaxy_list = [x for x in range(1, num_galaxies+1)]
    pair_list = [(x, y) for idx, x in enumerate(galaxy_list) for y in galaxy_list[idx+1:]]
    print('After expansion:')
    print(galaxy_dict)

    for pair in pair_list:
        x, y = pair

        galaxy1_r, galaxy1_c = galaxy_dict[x]
        galaxy2_r, galaxy2_c = galaxy_dict[y]

        output = output + abs(galaxy1_r - galaxy2_r) + abs(galaxy1_c - galaxy2_c)

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

OFFSET = 999999
part2_example = process_inputs2(example_file, OFFSET)
part2 = process_inputs2(input_file, OFFSET)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
