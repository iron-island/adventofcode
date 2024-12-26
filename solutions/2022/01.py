input_file = "../../inputs/2022/input01.txt"
example_file = "example01.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    calories_list = []
    curr_cal = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if (line != ""):
                curr_cal += int(line)
            else:
                calories_list.append(curr_cal)
                curr_cal = 0

            line = file.readline()

    output = max(calories_list)

    return output

def process_inputs2(in_file):
    output = 0

    calories_list = []
    curr_cal = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if (line != ""):
                curr_cal += int(line)
            else:
                calories_list.append(curr_cal)
                curr_cal = 0

            line = file.readline()
    calories_list.append(curr_cal)

    max1 = max(calories_list)
    idx1 = calories_list.index(max1)
    calories_list.pop(idx1)

    max2 = max(calories_list)
    idx2 = calories_list.index(max2)
    calories_list.pop(idx2)

    max3 = max(calories_list)

    print(max1, max2, max3)

    output = max1 + max2 + max3

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
