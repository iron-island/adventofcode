import re
#import numpy as np
input_file = "../../inputs/2023/input16.txt"
example_file = "example16.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

# Parsing numbers into list of strings from line
# number_list = re.findall(r'[+-]?\d+', line)

def process_inputs(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()

        while line:
            line = line.strip()

            line = [x for x in line]
            grid.append(line)

            line = file.readline()

    # BFS
    queue = []
    visited = []

    # l, r, u, d
    queue.append((0, 0, 'r'))
    max_rows = len(grid) - 1
    max_cols = len(grid[0]) - 1
    energized = set()
    while len(queue):
        q = queue.pop(0)
        r, c, d = q

        if q in visited:
            continue

        energized.add((r, c))

        g = grid[r][c]
        CAN_UP = (r > 0)
        CAN_DOWN = (r < max_rows)
        CAN_LEFT = (c > 0)
        CAN_RIGHT = (c < max_cols)
        if (d == 'r'):
            if (CAN_RIGHT) and ((g == '.') or (g == '-')):
                queue.append((r, c+1, 'r'))
            elif (CAN_DOWN) and (g == "\\"):
                queue.append((r+1, c, 'd'))
            elif (CAN_UP) and (g == "/"):
                queue.append((r-1, c, 'u'))
            elif (g == "|"):
                if (CAN_UP):
                    queue.append((r-1, c, 'u'))
                if (CAN_DOWN):
                    queue.append((r+1, c, 'd'))
        elif (d == 'l'):
            if (CAN_LEFT) and ((g == '.') or (g == '-')):
                queue.append((r, c-1, 'l'))
            elif (CAN_DOWN) and (g == '/'):
                queue.append((r+1, c, 'd'))
            elif (CAN_UP) and (g == '\\'):
                queue.append((r-1, c, 'u'))
            elif (g == '|'):
                if (CAN_UP):
                    queue.append((r-1, c, 'u'))
                if (CAN_DOWN):
                    queue.append((r+1, c, 'd'))
        elif (d == 'u'):
            if (CAN_UP) and ((g == '.') or (g == '|')):
                queue.append((r-1, c, 'u'))
            elif (CAN_LEFT) and (g == '\\'):
                queue.append((r, c-1, 'l'))
            elif (CAN_RIGHT) and (g == '/'):
                queue.append((r, c+1, 'r'))
            elif (g == '-'):
                if (CAN_LEFT):
                    queue.append((r, c-1, 'l'))
                if (CAN_RIGHT):
                    queue.append((r, c+1, 'r'))
        elif (d == 'd'):
            if (CAN_DOWN) and ((g == '.') or (g == '|')):
                queue.append((r+1, c, 'd'))
            elif (CAN_RIGHT) and (g == '\\'):
                queue.append((r, c+1, 'r'))
            elif (CAN_LEFT) and (g == '/'):
                queue.append((r, c-1, 'l'))
            elif (g == '-'):
                if (CAN_LEFT):
                    queue.append((r, c-1, 'l'))
                if (CAN_RIGHT):
                    queue.append((r, c+1, 'r'))

        visited.append(q)

    for g in grid:
        print(''.join(g))

    print("Energized:")
    for r, g in enumerate(grid):
        for c, i in enumerate(g):
            coord = (r, c)
            if (coord in energized):
                print('#', end="")
            else:
                print('.', end="")
        print("")

    output = len(energized)

    return output

def process_inputs2(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()

        while line:
            line = line.strip()

            line = [x for x in line]
            grid.append(line)

            line = file.readline()

    max_rows = len(grid) - 1
    max_cols = len(grid[0]) - 1
    starters = []

    for c in range(0, max_cols+1):
        starters.append((0, c, 'd'))
        starters.append((max_rows, c, 'u'))

    for r in range(0, max_rows+1):
        starters.append((r, 0, 'r'))
        starters.append((r, max_cols, 'l'))

    # Loop through all possible starting beams
    max_energized = 0
    for idx, s in enumerate(starters):
        print(f'Starter {idx} of {len(starters)}...')
        # BFS
        queue = []
        visited = []

        # l, r, u, d
        queue.append(s)
        energized = set()
        while len(queue):
            q = queue.pop(0)
            r, c, d = q

            if q in visited:
                continue

            energized.add((r, c))

            g = grid[r][c]
            CAN_UP = (r > 0)
            CAN_DOWN = (r < max_rows)
            CAN_LEFT = (c > 0)
            CAN_RIGHT = (c < max_cols)
            if (d == 'r'):
                if (CAN_RIGHT) and ((g == '.') or (g == '-')):
                    queue.append((r, c+1, 'r'))
                elif (CAN_DOWN) and (g == "\\"):
                    queue.append((r+1, c, 'd'))
                elif (CAN_UP) and (g == "/"):
                    queue.append((r-1, c, 'u'))
                elif (g == "|"):
                    if (CAN_UP):
                        queue.append((r-1, c, 'u'))
                    if (CAN_DOWN):
                        queue.append((r+1, c, 'd'))
            elif (d == 'l'):
                if (CAN_LEFT) and ((g == '.') or (g == '-')):
                    queue.append((r, c-1, 'l'))
                elif (CAN_DOWN) and (g == '/'):
                    queue.append((r+1, c, 'd'))
                elif (CAN_UP) and (g == '\\'):
                    queue.append((r-1, c, 'u'))
                elif (g == '|'):
                    if (CAN_UP):
                        queue.append((r-1, c, 'u'))
                    if (CAN_DOWN):
                        queue.append((r+1, c, 'd'))
            elif (d == 'u'):
                if (CAN_UP) and ((g == '.') or (g == '|')):
                    queue.append((r-1, c, 'u'))
                elif (CAN_LEFT) and (g == '\\'):
                    queue.append((r, c-1, 'l'))
                elif (CAN_RIGHT) and (g == '/'):
                    queue.append((r, c+1, 'r'))
                elif (g == '-'):
                    if (CAN_LEFT):
                        queue.append((r, c-1, 'l'))
                    if (CAN_RIGHT):
                        queue.append((r, c+1, 'r'))
            elif (d == 'd'):
                if (CAN_DOWN) and ((g == '.') or (g == '|')):
                    queue.append((r+1, c, 'd'))
                elif (CAN_RIGHT) and (g == '\\'):
                    queue.append((r, c+1, 'r'))
                elif (CAN_LEFT) and (g == '/'):
                    queue.append((r, c-1, 'l'))
                elif (g == '-'):
                    if (CAN_LEFT):
                        queue.append((r, c-1, 'l'))
                    if (CAN_RIGHT):
                        queue.append((r, c+1, 'r'))

            visited.append(q)

        max_energized = max(max_energized, len(energized))

    #for g in grid:
    #    print(''.join(g))

    #print("Energized:")
    #for r, g in enumerate(grid):
    #    for c, i in enumerate(g):
    #        coord = (r, c)
    #        if (coord in energized):
    #            print('#', end="")
    #        else:
    #            print('.', end="")
    #    print("")

    output = max_energized

    return output

#part1_example = process_inputs(example_file)
#part1         = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2         = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1        : {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2        : {part2}')

