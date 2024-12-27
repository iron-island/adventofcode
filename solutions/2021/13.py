from collections import defaultdict
import copy

input_file = "../../inputs/2021/input13.txt"
example_file = "example13.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

letter_dict = defaultdict(list)
letter_set_dict = defaultdict(set)
letter_dict["A"] = [
".##.",
"#..#",
"#..#",
"####",
"#..#",
"#..#"
]
letter_dict["C"] = [
".##.",
"#..#",
"#...",
"#...",
"#..#",
".##."
]
letter_dict["H"] = [
"#..#",
"#..#",
"####",
"#..#",
"#..#",
"#..#"
]
letter_dict["L"] = [
"#...",
"#...",
"#...",
"#...",
"#...",
"####"
]
letter_dict["R"] = [
"###.",
"#..#",
"#..#",
"###.",
"#.#.",
"#..#"
]

def process_inputs(in_file):
    output = 0

    dots_list = []
    folds_list = []
    MAX_ROW = 0
    MAX_COL = 0
    with open(in_file) as file:
        line = file.readline()
   
        get_folds = False 
        while line:
            line = line.strip()

            if (line == ""):
                get_folds = True
            elif (get_folds):
                if ("x=" in line):
                    axis = "col"
                elif ("y=" in line):
                    axis = "row"

                num = int(line.split("=")[1])
                folds_list.append((axis, num))
            else:
                col, row = line.split(",")
                row, col = map(int, [row, col])

                MAX_ROW = max(MAX_ROW, row)
                MAX_COL = max(MAX_COL, col)

                dots_list.append((row, col))

            line = file.readline()

    for idx in range(0, 1):
        axis, num = folds_list[idx]

        new_dots_list = []
        for dot in dots_list:
            row, col = dot

            if (axis == "row"):
                MAX_ROW = num - 1
                if (row > num):
                    # Fold row
                    row = num - (row - num)
            elif (axis == "col"):
                MAX_COL = num - 1
                if (col > num):
                    # Fold col
                    col = num - (col - num)

            new_dots_list.append((row, col))

    output = len(set(new_dots_list))
    #print(MAX_ROW, MAX_COL)
    #for row in range(0, MAX_ROW+1):
    #    for col in range(0, MAX_COL+1):
    #        if ((row, col) in new_dots_list):
    #            print("#", end="")
    #        else:
    #            print(".", end="")

    #    print("")

    return output

def process_inputs2(in_file):
    global letter_set_dict

    output = 0

    dots_list = []
    folds_list = []
    MAX_ROW = 0
    MAX_COL = 0
    with open(in_file) as file:
        line = file.readline()
   
        get_folds = False 
        while line:
            line = line.strip()

            if (line == ""):
                get_folds = True
            elif (get_folds):
                if ("x=" in line):
                    axis = "col"
                elif ("y=" in line):
                    axis = "row"

                num = int(line.split("=")[1])
                folds_list.append((axis, num))
            else:
                col, row = line.split(",")
                row, col = map(int, [row, col])

                MAX_ROW = max(MAX_ROW, row)
                MAX_COL = max(MAX_COL, col)

                dots_list.append((row, col))

            line = file.readline()

    # Populate letter_set_dict
    for letter in letter_dict:
        if (letter not in letter_set_dict):
            letter_list = letter_dict[letter]

            letter_set = set()
            for row, rowline in enumerate(letter_list):
                for col, char in enumerate(rowline):
                    if (char == "#"):
                        letter_set.add((row, col))
            letter_set_dict[letter] = letter_set

    for fold in folds_list:
        axis, num = fold

        new_dots_set = set(dots_list)
        for dot in dots_list:
            row, col = dot

            if (axis == "row"):
                MAX_ROW = num - 1
                if (row > num):
                    # Fold row
                    row = num - (row - num)
            elif (axis == "col"):
                MAX_COL = num - 1
                if (col > num):
                    # Fold col
                    col = num - (col - num)

            new_dots_set.add((row, col))

        dots_list = list(new_dots_set)

    # Print
    print(MAX_ROW, MAX_COL)
    for row in range(0, MAX_ROW+1):
        for col in range(0, MAX_COL+1):
            if ((row, col) in new_dots_set):
                print("#", end="")
            else:
                print(".", end="")

        print("")

    # Strip off coordinates outside of (0, 0) and (MAX_ROW, MAX_COL) region
    dots_set = set()
    for dot in new_dots_set:
        row, col = dot

        if (row < 0) or (row > MAX_ROW) or (col < 0) or (col > MAX_COL):
            continue

        dots_set.add((row, col))

    # Identify letters
    output = ""
    while (len(output) < 8):
        letter_set = set()
        col_offset = len(output)*5
        new_dots_set = copy.deepcopy(dots_set)
        for dot in dots_set:
            row, col = dot

            new_col = col - col_offset

            # Letters are 4 characters wide
            if (new_col < 4):
                letter_set.add((row, new_col))
                new_dots_set.remove((row, col))

        # Update dots_set
        dots_set = copy.deepcopy(new_dots_set)

        # Find the letter
        for letter in letter_set_dict:
            if (letter_set == letter_set_dict[letter]):
                output += letter
                break

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
