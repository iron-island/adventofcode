import math

input_file = "../../inputs/2021/input18.txt"
example_file = "example18.txt"
example2_file = "example18_2.txt"
example3_file = "example18_3.txt"
example4_file = "example18_4.txt"
example5_file = "example18_5.txt"
example6_file = "example18_6.txt"
example7_file = "example18_7.txt"
example8_file = "example18_8.txt"
example9_file = "example18_9.txt"
example10_file = "example18_10.txt"
example11_file = "example18_11.txt"
example12_file = "example18_12.txt"
example13_file = "example18_13.txt"
example14_file = "example18_14.txt"
example15_file = "example18_15.txt"
example16_file = "example18_16.txt"
example17_file = "example18_17.txt"
example18_file = "example18_18.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part1_example4 = 0
part1_example5 = 0
part1_example6 = 0
part1_example7 = 0
part1_example8 = 0
part1_example9 = 0
part1_example10 = 0
part1_example11 = 0
part1_example12 = 0
part1_example13 = 0
part1_example14 = 0
part1_example15 = 0
part1_example16 = 0
part1_example17 = 0
part1_example18 = 0
part2_example = 0
part2_example18 = 0
part1 = 0
part2 = 0

exploded = False
split = False

def dfs_add_exploded(num_list, num1_exp, num2_exp):
    # Base case
    if (isinstance(num_list, int)):
        return num_list + num1_exp + num2_exp

    num1, num2 = num_list

    if (num1_exp > 0):
        if (isinstance(num1, int)):
            num1 = num1 + num1_exp
        else:
            num1 = dfs_add_exploded(num1, num1_exp, num2_exp)
    elif (num2_exp > 0):
        if (isinstance(num2, int)):
            num2 = num2 + num2_exp
        else:
            num2 = dfs_add_exploded(num2, num1_exp, num2_exp)

    return [num1, num2]

def dfs_explode(num_list, depth):
    global exploded

    # Base case for regular number
    if (isinstance(num_list, int)):
        return num_list, 0, 0

    num1, num2 = num_list

    if (depth >= 4) and (isinstance(num1, int)) and (isinstance(num2, int)) and not (exploded):
        # Base case for explode
        exploded = True
        num_exp1 = num1
        num_exp2 = num2

        return 0, num_exp1, num_exp2
    else:
        # DFS num1
        num1, num1_exp1, num1_exp2 = dfs_explode(num1, depth+1)

        # If num1 exploded
        #print(f'Adding explosion to num2: {num2}')
        num2 = dfs_add_exploded(num2, num1_exp=num1_exp2, num2_exp=0)

        # DFS num2
        num2, num2_exp1, num2_exp2 = dfs_explode(num2, depth+1)

        # If num2 exploded
        #print(f'Adding explosion to num1: {num1}')
        num1 = dfs_add_exploded(num1, num1_exp=0, num2_exp=num2_exp1)

        return [num1, num2], num1_exp1, num2_exp2

def dfs_split(num_list):
    global split

    # Base case
    if (isinstance(num_list, int)):
        if (num_list >= 10) and not (split):
            split = True
            half_num = num_list/2
            num1 = math.floor(half_num)
            num2 = math.ceil(half_num)

            return [num1, num2]
        return num_list
    else:
        num1, num2 = num_list

        num1 = dfs_split(num1)
        num2 = dfs_split(num2)

    return [num1, num2]

def dfs_magnitude(num_list):
    num1, num2 = num_list

    if (isinstance(num1, int)):
        # Base case
        num1_mag = num1
    else:
        num1_mag = dfs_magnitude(num1)

    if (isinstance(num2, int)):
        # Base case
        num2_mag = num2
    else:
        num2_mag = dfs_magnitude(num2)

    return 3*num1_mag + 2*num2_mag

def process_inputs(in_file):
    global exploded
    global split

    output = 0

    num_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            num = eval(line)

            num_list.append(num)

            line = file.readline()

    num1 = num_list[0]
    if (len(num_list) == 1):
        # Immediately reduce
        print(num1)
        while True:
            exploded = False
            split = False

            # Explode
            num1, _, _ = dfs_explode(num1, 0)
            break

            # Split
            if not (exploded):
                num1 = dfs_split(num1)

            if (not exploded) and (not split):
                break
        print(num1)
    else:
        for num2 in num_list[1:]:
            num1 = [num1, num2]

            # Start reduction
            num_reduce = 0
            while True:
                exploded = False
                split = False

                # Explode
                num1, _, _ = dfs_explode(num1, 0)

                # Split
                if not (exploded):
                    num1 = dfs_split(num1)

                num_reduce += 1
                #if (num_reduce == 2):
                #    break
                #print(num1)
                if (not exploded) and (not split):
                    break
        print(num1)

    # Evaluate
    output = dfs_magnitude(num1)

    return output

def process_inputs2(in_file):
    global exploded
    global split

    output = 0

    num_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            num = eval(line)

            num_list.append(num)

            line = file.readline()

    num1 = num_list[0]
    if (len(num_list) == 1):
        # Immediately reduce
        print(num1)
        while True:
            exploded = False
            split = False

            # Explode
            num1, _, _ = dfs_explode(num1, 0)
            break

            # Split
            if not (exploded):
                num1 = dfs_split(num1)

            if (not exploded) and (not split):
                break
        print(num1)
    else:
        MAX_OUTPUT = 0
        for idx1, num1 in enumerate(num_list):
            for idx2, num2 in enumerate(num_list):
                if (idx1 == idx2):
                    continue

                new_num = [num1, num2]

                # Start reduction
                while True:
                    exploded = False
                    split = False

                    # Explode
                    new_num, _, _ = dfs_explode(new_num, 0)

                    # Split
                    if not (exploded):
                        new_num = dfs_split(new_num)

                    if (not exploded) and (not split):
                        break

                # Evaluate
                MAX_OUTPUT = max(MAX_OUTPUT, dfs_magnitude(new_num))

    output = MAX_OUTPUT

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file) # single explode
#part1_example3 = process_inputs(example3_file) # single explode
#part1_example4 = process_inputs(example4_file) # single explode
#part1_example5 = process_inputs(example5_file) # single explode
#part1_example6 = process_inputs(example6_file) # single explode
#part1_example7 = process_inputs(example7_file) # final sum
#part1_example8 = process_inputs(example8_file) # final sum
#part1_example9 = process_inputs(example9_file) # final sum
#part1_example10 = process_inputs(example10_file) # final sum
#part1_example11 = process_inputs(example11_file) # final sum
#part1_example12 = process_inputs(example12_file) # final magnitude
#part1_example13 = process_inputs(example13_file) # final magnitude
#part1_example14 = process_inputs(example14_file) # final magnitude
#part1_example15 = process_inputs(example15_file) # final magnitude
#part1_example16 = process_inputs(example16_file) # final magnitude
#part1_example17 = process_inputs(example17_file) # final magnitude
#part1_example18 = process_inputs(example18_file) # final magnitude
#part1 = process_inputs(input_file)

part2_example18 = process_inputs2(example18_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1 example4: {part1_example4}')
print(f'Part 1 example5: {part1_example5}')
print(f'Part 1 example6: {part1_example6}')
print(f'Part 1 example7: {part1_example7}')
print(f'Part 1 example8: {part1_example8}')
print(f'Part 1 example9: {part1_example9}')
print(f'Part 1 example10: {part1_example10}')
print(f'Part 1 example11: {part1_example11}')
print(f'Part 1 example12: {part1_example12}')
print(f'Part 1 example13: {part1_example13}')
print(f'Part 1 example14: {part1_example14}')
print(f'Part 1 example15: {part1_example15}')
print(f'Part 1 example16: {part1_example16}')
print(f'Part 1 example17: {part1_example17}')
print(f'Part 1 example18: {part1_example18}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example18: {part2_example18}')
print(f'Part 2: {part2}')
