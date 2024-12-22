input_file = "input1.txt"
example_file = "example1.txt"
example2_file = "example1_2.txt"
example3_file = "example1_3.txt"
example4_file = "example1_4.txt"
example5_file = "example1_5.txt"
example6_file = "example1_6.txt"
example7_file = "example1_7.txt"
example8_file = "example1_8.txt"
example9_file = "example1_9.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part1_example4 = 0

part2_example = 0
part2_example5 = 0
part2_example6 = 0
part2_example7 = 0
part2_example8 = 0
part2_example9 = 0
part1 = 0
part2 = 0

def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            captcha = line

            line = file.readline()

    output = 0
    for idx, digit in enumerate(captcha):
        if (idx == (len(captcha)-1)):
            if (digit == captcha[0]):
                output += int(digit)
        elif (digit == captcha[idx+1]):
            output += int(digit)

    return output

def process_inputs2(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            captcha = line

            line = file.readline()

    output = 0
    num_digits = len(captcha)
    half_digits = int(num_digits/2)
    for idx, digit in enumerate(captcha):
        idx2 = (idx+half_digits) % num_digits
        if (digit == captcha[idx2]):
            output += int(digit)

    return output

part1_example = process_inputs(example_file)
part1_example2 = process_inputs(example2_file)
part1_example3 = process_inputs(example3_file)
part1_example4 = process_inputs(example4_file)
part1 = process_inputs(input_file)

part2_example5 = process_inputs2(example5_file)
part2_example6 = process_inputs2(example6_file)
part2_example7 = process_inputs2(example7_file)
part2_example8 = process_inputs2(example8_file)
part2_example9 = process_inputs2(example9_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1 example4: {part1_example4}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example5: {part2_example5}')
print(f'Part 2 example6: {part2_example6}')
print(f'Part 2 example7: {part2_example7}')
print(f'Part 2 example8: {part2_example8}')
print(f'Part 2 example9: {part2_example9}')
print(f'Part 2: {part2}')
