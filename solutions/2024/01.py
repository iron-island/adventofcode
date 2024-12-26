input_file = "../../inputs/2024/input01.txt"
example_file = "example01.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    left_list = []
    right_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            left, right = line.split()

            left_list.append(int(left))
            right_list.append(int(right))

            line = file.readline()

    left_list.sort()
    right_list.sort()

    assert(len(left_list) == len(right_list))
    output = 0
    for idx, left in enumerate(left_list):
        diff = abs(left - right_list[idx])
        print(idx)
        output = output + diff

    return output

def process_inputs2(in_file):
    left_list = []
    right_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            left, right = line.split()

            left_list.append(int(left))
            right_list.append(int(right))

            line = file.readline()

    left_list.sort()
    right_list.sort()

    assert(len(left_list) == len(right_list))
    output = 0
    for idx, left in enumerate(left_list):
        count = right_list.count(left)
        output = output + left*count

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

#print(f'Part 1 example: {part1_example}')
#print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
