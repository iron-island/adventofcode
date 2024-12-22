import string

input_file = "input5.txt"
example_file = "example5.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

upper_list = list(string.ascii_uppercase)
lower_list = list(string.ascii_lowercase)

def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            polymer = line

            line = file.readline()

    # React
    while True:
        prev_polymer = polymer
        for idx, lower in enumerate(lower_list):
            upper = upper_list[idx]

            string1 = lower + upper
            string2 = upper + lower

            polymer = polymer.replace(string1, "")
            polymer = polymer.replace(string2, "")

        if (prev_polymer == polymer):
            break

    output = len(polymer)

    return output

def process_inputs2(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            polymer = line

            line = file.readline()

    init_polymer = polymer

    # Iterate through all possible types
    length_list = []
    for idx_rem, upper_rem in enumerate(upper_list):
        polymer = init_polymer

        # Remove types
        polymer = polymer.replace(upper_rem, "")
        polymer = polymer.replace(lower_list[idx_rem], "")

        # React
        while True:
            prev_polymer = polymer
            for idx, lower in enumerate(lower_list):
                upper = upper_list[idx]

                string1 = lower + upper
                string2 = upper + lower

                polymer = polymer.replace(string1, "")
                polymer = polymer.replace(string2, "")

            if (prev_polymer == polymer):
                break

        # Record lengths
        length_list.append(len(polymer))

    output = min(length_list)

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
