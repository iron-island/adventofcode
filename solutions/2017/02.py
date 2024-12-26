input_file = "input2.txt"
example_file = "example02.txt"
example2_file = "example02_2.txt"

part1_example = 0
part2_example = 0
part2_example2 = 0
part1 = 0
part2 = 0

def process_inputs(in_file):
    output = 0

    ss = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            num_list = [int(x) for x in line.split()]
            ss.append(num_list)

            line = file.readline()

    # Compute
    output = 0
    for num_list in ss:
        min_num = min(num_list)
        max_num = max(num_list)

        output += (max_num - min_num)

    return output

def process_inputs2(in_file):
    output = 0

    ss = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            num_list = [int(x) for x in line.split()]
            ss.append(num_list)

            line = file.readline()

    # Compute
    output = 0
    for num_list in ss:
        for idx1, num1 in enumerate(num_list):
            for idx2, num2 in enumerate(num_list[(idx1+1):]):
                max_num = max(num1, num2)
                min_num = min(num1, num2)

                if ((max_num % min_num) == 0):
                    output += int(max_num/min_num)

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2_example2 = process_inputs2(example2_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2: {part2}')
