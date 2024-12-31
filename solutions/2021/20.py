input_file = "../../inputs/2021/input20.txt"
example_file = "example20.txt"

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

            line = file.readline()

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
