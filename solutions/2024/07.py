import numpy as np
from functools import cache

input_file = "../../inputs/2024/input07.txt"
example_file = "example07.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
OPS = ['+', '*']
OPS2 = ['+', '*', '|']

def concat(x, y):
    return x + y

@cache
def dfs(eq, num_tuple, result):
    # Early exit if current test result is already larger than expected
    if (eq > result):
        return None

    # Base case
    if (len(num_tuple) == 0):
        if (eq == result):
            return eq
        else:
            return None

    num_str = num_tuple[0]
    # Addition
    eq1 = dfs(eq + int(num_str), num_tuple[1:], result)

    if (eq1 == result):
        return result

    # Multiplication
    eq2 = dfs(eq*int(num_str), num_tuple[1:], result)

    if (eq2 == result):
        return result

    # Concatenation
    eq3 = dfs(eq*(10**len(num_str)) + int(num_str), num_tuple[1:], result)

    if (eq3 == result):
        return result

    # If did not become equal to result, return None so it fails test equality
    return None

def process_inputs(in_file):
    output = 0

    eq_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            result, nums = line.split(": ")
            num_list = nums.split()
            eq_list.append([result, num_list])

            line = file.readline()

    # Brute force
    count = 0
    true_result = 0
    for eq in eq_list:
        result, num_list = eq
        num_operators = len(num_list)-1
        op_list = []
        num_comb = (2**num_operators)
        for i in range(0, num_comb):
            bin_string = bin(i)
            bin_string = bin_string[2:]
            # Left pad
            if (len(bin_string) < num_operators):
                num_pad = num_operators - len(bin_string)
                for n in range(0, num_pad):
                    bin_string = "0" + bin_string

            # Permutations
            eq = ""
            for b in bin_string:
                eq = "(" + eq
            for idx, b in enumerate(bin_string):
                eq = eq + num_list[idx]
                if (idx > 0):
                    eq = eq + ")"

                op = OPS[int(b)]
                eq = eq + op
            eq = eq + num_list[-1]
            eq = eq + ")"

            # Evaluate
            test_result = eval(eq)
            if (int(result) == test_result):
                print(test_result)
                count += 1
                true_result += test_result
                break
            #eq = ""
            #for idx, b in enumerate(bin_string):
            #    op = OPS[int(b)]
            #    eq = num_list[idx] + op + num_list[idx+1]
            #    eq = str(eval(eq))
            #if (result == eq):
            #    count += 1
            #    true_result += int(eq)
            #    break

    print(count)
    output = true_result
    
    return output

def process_inputs2(in_file):
    output = 0

    eq_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            result, nums = line.split(": ")
            num_list = nums.split()
            eq_list.append([result, num_list])

            line = file.readline()

    # Brute force
    count = 0
    true_result = 0
    eq_count = 1
    for eq in eq_list:
        print(f'{eq_count} of {len(eq_list)}')
        eq_count += 1
        result, num_list = eq
        num_operators = len(num_list)-1
        op_list = []
        num_comb = (3**num_operators)

        # Optimal DFS
        eq_int = dfs(0, tuple(num_list), int(result))

        # Evaluate
        test_result = eq_int
        if (int(result) == test_result):
            count += 1
            true_result += test_result
        continue

        # Former brute-force linear search solution which was slower
        #for i in range(0, num_comb):
        #    # Convert to base 3 string
        #    #bin_string = bin(i)
        #    #bin_string = bin_string[2:]
        #    bin_string = np.base_repr(int(i), base=3)

        #    # Left pad
        #    if (len(bin_string) < num_operators):
        #        num_pad = num_operators - len(bin_string)
        #        for n in range(0, num_pad):
        #            bin_string = "0" + bin_string

        #    # Permutations
        #    #eq = num_list[0]
        #    eq_int = int(num_list[0])
        #    int_result = int(result)
        #    for idx, b in enumerate(bin_string):
        #        # Original solution, slow
        #        #op = OPS2[int(b)]

        #        #if (op != '|'):
        #        #    eq = eq + op + num_list[idx+1]
        #        #    eq = str(eval(eq))
        #        #else:
        #        #    eq = eq + num_list[idx+1]

        #        # Optimized solution
        #        if (eq_int > int_result):
        #            # Early exit if current test result is already larger than expected
        #            break
        #        num_str = num_list[idx+1]
        #        if (b == "0"):
        #            # Addition
        #            eq_int = eq_int + int(num_str)
        #        elif (b == "1"):
        #            # Multiplication
        #            eq_int = eq_int*int(num_str)
        #        elif (b == "2"):
        #            # Concatenation
        #            eq_int = eq_int*(10**len(num_str)) + int(num_str)

        #    # Evaluate
        #    #test_result = eval(eq)
        #    test_result = eq_int
        #    if (int(result) == test_result):
        #        count += 1
        #        true_result += test_result
        #        break

    print(count)
    output = true_result
    
    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
