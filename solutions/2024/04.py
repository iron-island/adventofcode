input_file = "input4.txt"
example_file = "example4.txt"

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

            grid.append(line)

            line = file.readline()

    # Go through grid
    # horizontal
    hor = 0
    hor_reverse = 0
    for line in grid:
        hor += line.count("XMAS")
        hor_reverse += line.count("SAMX")
    output += hor + hor_reverse

    # vertical
    column = ""
    vert = 0
    vert_reverse = 0
    MAX_COL = len(line)-1
    for col in range(0, MAX_COL+1):
        column = ""
        for line in grid:
            column = column + line[col]

        vert += column.count("XMAS")
        vert_reverse += column.count("SAMX")
    output += vert + vert_reverse

    # diagonal
    #output = 0
    MAX_ROW = len(grid) - 1
    diag1 = 0
    diag2 = 0
    diag3 = 0
    diag4 = 0
    for col in range(0, MAX_COL+1):
        for row in range(0, MAX_ROW+1):
            c = grid[row][col]

            # down to up diagonal /
            if (row >= 3) and (col <= (MAX_COL - 3)):
                if (c == "X") and (grid[row-1][col+1] == "M") and (grid[row-2][col+2] == "A") and (grid[row-3][col+3] == "S"):
                    output += 1
                    diag1 += 1

            # \ diagonal
            if (row >= 3) and (col >= 3):
                if (c == "X") and (grid[row-1][col-1] == "M") and (grid[row-2][col-2] == "A") and (grid[row-3][col-3] == "S"):
                    output += 1
                    diag2 += 1
                    print(f'diag2 (row,col) = ({row},{col})')
                    print(f'grid[row-2][col-2] = {grid[row-2][col-2]}')

            # up to down diagonal \
            if (row <= (MAX_ROW - 3)) and (col <= (MAX_COL - 3)):
                if (c == "X") and (grid[row+1][col+1] == "M") and (grid[row+2][col+2] == "A") and (grid[row+3][col+3] == "S"):
                    output += 1
                    diag3 += 1

            # / diagonal
            if (row <= (MAX_ROW - 3)) and (col >= 3):
                if (c == "X") and (grid[row+1][col-1] == "M") and (grid[row+2][col-2] == "A") and (grid[row+3][col-3] == "S"):
                    output += 1
                    diag4 += 1

            ## TRY HORIZONTAL
            #try:
            #    if (c == "X") and (grid[row][col+1] == "M") and (grid[row][col+2] == "A") and (grid[row][col+3] == "S"):
            #        output += 1
            #except:
            #    output += 0

            #try:
            #    if (c == "X") and (grid[row][col-1] == "M") and (grid[row][col-2] == "A") and (grid[row][col-3] == "S"):
            #        output += 1
            #except:
            #    output += 0

            ### TRY VERTICAL
            #try:
            #    if (c == "X") and (grid[row+1][col] == "M") and (grid[row+2][col] == "A") and (grid[row+3][col] == "S"):
            #        output += 1
            #except:
            #    output += 0

            #try:
            #    if (c == "X") and (grid[row-1][col] == "M") and (grid[row-2][col] == "A") and (grid[row-3][col] == "S"):
            #        output += 1
            #except:
            #    output += 0

    print(f'hor = {hor}') # should be 3
    print(f'hor_reverse = {hor_reverse}') # should be 2
    print(f'vert = {vert}') # should be 1
    print(f'vert_reverse = {vert_reverse}') # should be 2
    print(f'diag1 = {diag1}') # should be 4
    print(f'diag2 = {diag2}') # should be 4
    print(f'diag3 = {diag3}') # should be 1
    print(f'diag4 = {diag4}') # should be 1

    return output

def process_inputs2(in_file):
    output = 0

    grid = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            grid.append(line)

            line = file.readline()

    # Go through grid
    # horizontal
    hor = 0
    hor_reverse = 0
    for line in grid:
        hor += line.count("XMAS")
        hor_reverse += line.count("SAMX")
    output += hor + hor_reverse

    # vertical
    column = ""
    vert = 0
    vert_reverse = 0
    MAX_COL = len(line)-1
    for col in range(0, MAX_COL+1):
        column = ""
        for line in grid:
            column = column + line[col]

        vert += column.count("XMAS")
        vert_reverse += column.count("SAMX")
    output += vert + vert_reverse

    # diagonal
    output = 0
    MAX_ROW = len(grid) - 1
    diag1 = 0
    diag2 = 0
    diag3 = 0
    diag4 = 0
    for col in range(0, MAX_COL+1):
        for row in range(0, MAX_ROW+1):
            c = grid[row][col]

            if (row >= 1) and (row <= (MAX_ROW - 1)) and (col >= 1) and (col <= (MAX_COL - 1)):
                if (c == "A"):
                    if (grid[row-1][col-1] == "M") and (grid[row+1][col+1] == "S"):
                        # M M
                        #  A
                        # S S
                        if (grid[row-1][col+1] == "M") and (grid[row+1][col-1] == "S"):
                            output += 1
                        # M S
                        #  A
                        # M S
                        elif (grid[row-1][col+1] == "S") and (grid[row+1][col-1] == "M"):
                            output += 1
                    elif (grid[row-1][col-1] == "S") and (grid[row+1][col+1] == "M"):
                        # S M
                        #  A
                        # S M
                        if (grid[row-1][col+1] == "M") and (grid[row+1][col-1] == "S"):
                            output += 1
                        # S S
                        #  A
                        # M M
                        elif (grid[row-1][col+1] == "S") and (grid[row+1][col-1] == "M"):
                            output += 1

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
