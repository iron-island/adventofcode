input_file = "input2.txt"
example_file = "example2.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def process_inputs(in_file):
    output = 0

    policy_list = []
    password_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            policy, password = line.split(": ")
            minmax, character = policy.split(" ")
            min_num, max_num = minmax.split("-")
            
            policy_list.append((int(min_num), int(max_num), character))
            password_list.append(password)

            line = file.readline()

    output = 0
    for idx, policy in enumerate(policy_list):
        min_num, max_num, c = policy
        password = password_list[idx]

        c_count = password.count(c)
        if (c_count >= min_num) and (c_count <= max_num):
            output += 1

    return output

def process_inputs2(in_file):
    output = 0

    policy_list = []
    password_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            policy, password = line.split(": ")
            minmax, character = policy.split(" ")
            min_num, max_num = minmax.split("-")
            
            policy_list.append((int(min_num), int(max_num), character))
            password_list.append(password)

            line = file.readline()

    output = 0
    for idx, policy in enumerate(policy_list):
        min_num, max_num, c = policy
        password = password_list[idx]

        min_c = password[min_num-1]
        max_c = password[max_num-1]

        if (min_c == max_c):
            continue
        elif (min_c == c) or (max_c == c):
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
