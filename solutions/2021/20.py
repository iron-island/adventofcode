import copy
from collections import defaultdict

input_file = "../../inputs/2021/input20.txt"
example_file = "example20.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def get_pixel(image_dict, rc):
    if (rc not in image_dict):
        return "0"
    else:
        return image_dict[rc]

def process_inputs(in_file, num_enhancements):
    output = 0

    algo = ""
    image_dict = defaultdict(str)
    with open(in_file) as file:
        line = file.readline()
   
        get_image = False 
        MAX_ROW = 0
        MAX_COL = 0
        while line:
            line = line.strip()

            line_bin = ""
            for p in line:
                if (p == "#"):
                    line_bin += "1"
                else:
                    line_bin += "0"

            if (line == ""):
                get_image = True
                row = 0
            elif (get_image):
                for col, b in enumerate(line_bin):
                    image_dict[(row, col)] = b

                    MAX_COL = max(col, MAX_COL)
                MAX_ROW = max(row, MAX_ROW)
                row += 1
            else:
                algo = algo + line_bin

            line = file.readline()
    MIN_ROW = 0
    MIN_COL = 0
    ORIG_MIN_ROW = 0
    ORIG_MIN_COL = 0
    ORIG_MAX_ROW = MAX_ROW
    ORIG_MAX_COL = MAX_COL

    # DEBUG
    #for row in range(MIN_ROW, MAX_ROW+1):
    #    for col in range(MIN_COL, MAX_COL+1):
    #        if (image_dict[(row, col)] == "1"):
    #            print("#", end="")
    #        else:
    #            print(".", end="")

    #    print("")

    MIN_ROW = MIN_ROW-2*(num_enhancements+1)
    MIN_COL = MIN_COL-2*(num_enhancements+1)
    MAX_ROW = MAX_ROW+2*(num_enhancements+1)
    MAX_COL = MAX_COL+2*(num_enhancements+1)
    for i in range(0, num_enhancements):
        new_image_dict = defaultdict(str)

        # Expand the rows and columns
        print(f'Iteration {i}')
        print(MIN_ROW, MAX_ROW)
        print(MIN_COL, MAX_COL)

        for row in range(MIN_ROW, MAX_ROW+1):
            for col in range(MIN_COL, MAX_COL+1):
                # top left
                tl_rc = (row-1, col-1)

                # top
                t_rc = (row-1, col)

                # top right
                tr_rc = (row-1, col+1)

                # left
                l_rc = (row, col-1)

                # right
                r_rc = (row, col+1)

                # bottom left
                bl_rc = (row+1, col-1)

                # bottom
                b_rc = (row+1, col)

                # bottom right
                br_rc = (row+1, col+1)

                tl = get_pixel(image_dict, tl_rc)
                t  = get_pixel(image_dict, t_rc)
                tr = get_pixel(image_dict, tr_rc)
                l  = get_pixel(image_dict, l_rc)
                m  = get_pixel(image_dict, (row, col))
                r  = get_pixel(image_dict, r_rc)
                bl = get_pixel(image_dict, bl_rc)
                b  = get_pixel(image_dict, b_rc)
                br = get_pixel(image_dict, br_rc)

                idx_str = tl + t + tr + l + m + r + bl + b + br
                idx = int(idx_str, base=2)

                pixel = algo[idx]

                new_image_dict[(row, col)] = pixel

        # Record
        image_dict = copy.deepcopy(new_image_dict)

    # Debug
    assert(len(algo) == 512)
    #for row in range(MIN_ROW, MAX_ROW+1):
    #    for col in range(MIN_COL, MAX_COL+1):
    #        if (image_dict[(row, col)] == "1"):
    #            print("#", end="")
    #        else:
    #            print(".", end="")

    #    print("")

    # Evaluate
    output = 0
    for rc in image_dict:
        row, col = rc
        if (row < (ORIG_MIN_ROW-num_enhancements)) or (row > (ORIG_MAX_ROW+num_enhancements)) or \
           (col < (ORIG_MIN_COL-num_enhancements)) or (col > (ORIG_MAX_COL+num_enhancements)):
            continue

        pixel = image_dict[rc]

        if (pixel == "1"):
            output += 1

    return output

part1_example = process_inputs(example_file, 2)
part1 = process_inputs(input_file, 2)
# 5354 too high
# 5294 too low

part2_example = process_inputs(example_file, 50)
part2 = process_inputs(input_file, 50)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
