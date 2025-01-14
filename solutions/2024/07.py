input_file = "../../inputs/2024/input07.txt"
#example_file = "example07.txt"

#part1_example = 0
#part2_example = 0
#part1 = 0
#part2 = 0

# Note: Adding a cache slows down the DFS, since this is already fast
def dfs_part1(eq, num_tuple, result):
    # Early exit if current test result is already larger than expected
    if (eq > result):
        return 0

    # Base case since there are no more numbers to operate on
    if (len(num_tuple) == 0):
        if (eq == result):
            return eq
        else:
            return 0

    # Get next number to operate on, while remaining numbers
    #   in num_tuple[1:] will be used on further calls
    num = num_tuple[0]
    next_num_tuple = num_tuple[1:]

    # Addition
    eq1 = dfs_part1(eq + num, next_num_tuple, result)

    if (eq1 == result):
        return result

    # Multiplication
    eq2 = dfs_part1(eq*num, next_num_tuple, result)

    if (eq2 == result):
        return result

    # If did not become equal to result, return 0 so it fails test equality
    return 0

# Note: Adding a cache slows down the DFS, since this is already fast
def dfs(eq, num_tuple, result):
    # Early exit if current test result is already larger than expected
    if (eq > result):
        return 0

    # Base case since there are no more numbers to operate on
    if (len(num_tuple) == 0):
        if (eq == result):
            return eq
        else:
            return 0

    # Get next number to operate on, while remaining numbers
    #   in num_tuple[1:] will be used on further calls
    num = num_tuple[0]
    next_num_tuple = num_tuple[1:]

    # Addition
    if (dfs(eq + num, next_num_tuple, result) == result):
        return result

    # Multiplication
    if (dfs(eq*num, next_num_tuple, result) == result):
        return result

    # Concatenation
    if (num >= 100):
        num_digits = 3
    elif (num >= 10):
        num_digits = 2
    else:
        num_digits = 1
    #NUM_DIGITS = len(str(num))
    if (dfs(eq*(10**num_digits) + num, next_num_tuple, result) == result):
        return result

    # If did not become equal to result, return 0 so it fails test equality
    return 0

def process_inputs2(in_file):
    output = 0

    eq_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            result, nums = line.split(": ")
            num_tuple = tuple([int(x) for x in nums.split()])
            eq_list.append(tuple([int(result), num_tuple]))

            line = file.readline()

    # Part 1:
    part1 = 0
    skip_eq_set = set()
    for eq in eq_list:
        result, num_tuple = eq

        # Brute-force via DFS with no memoization
        test_result = dfs_part1(num_tuple[0], num_tuple[1:], result)

        # Evaluate
        if (result == test_result):
            part1 += test_result
            skip_eq_set.add(eq)

    # Part 2:
    true_result = part1
    #eq_count = 1
    #MAX_EQ_COUNT = len(eq_list)
    for eq in eq_list:
        #print(f'{eq_count} of {MAX_EQ_COUNT}')
        #eq_count += 1
        result, num_tuple = eq

        # If equation was already true in Part 1, skip it
        if (eq in skip_eq_set):
            continue

        # Brute-force via DFS with no memoization
        test_result = dfs(num_tuple[0], num_tuple[1:], result)

        # Evaluate
        if (result == test_result):
            true_result += test_result

    return part1, true_result

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part1, part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 7: Bridge Repair ---")
#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
