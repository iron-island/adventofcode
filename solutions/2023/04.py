import re

input_file = "input4.txt"
example_file = "example04.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            numbers = line.split(": ")[1]

            l1, l2 = numbers.split(" | ")

            nl1 = re.findall(r'\d+', l1)
            nl2 = re.findall(r'\d+', l2)

            points_exp = 0
            for n1 in nl1:
                if (n1 in nl2):
                    points_exp += 1

            if (points_exp > 0):
                output = output + 2**(points_exp-1)

            line = file.readline()

    return output

def process_inputs2(in_file, in_length):
    output = 0

    mul_list = []
    for i in range(0, in_length):
        mul_list.append(1)

    m = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            numbers = line.split(": ")[1]

            l1, l2 = numbers.split(" | ")

            nl1 = re.findall(r'\d+', l1)
            nl2 = re.findall(r'\d+', l2)

            ############################
            points_exp = 0
            for n1 in nl1:
                if (n1 in nl2):
                    points_exp += 1

            print(points_exp)

            for i in range(m+1, m+points_exp+1):
                if (i >= in_length):
                    continue
                mul_list[i] += mul_list[m]

            m += 1
            line = file.readline()

    print(mul_list)
    for mul in mul_list:
        output = output + mul    

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file, 6)
part2 = process_inputs2(input_file, 205)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
