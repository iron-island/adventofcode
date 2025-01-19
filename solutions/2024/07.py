from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input07.txt"

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

def part1_part2(in_file):
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
    part2 = 0
    for eq in eq_list:
        result, num_tuple = eq

        # Brute-force via DFS with no memoization
        test_result = dfs_part1(num_tuple[0], num_tuple[1:], result)

        # Evaluate Part 1
        if (result == test_result):
            part1 += test_result
        else:
            test_result = dfs(num_tuple[0], num_tuple[1:], result)

            if (result == test_result):
                part2 += test_result

    # Since Part 1 equations were skipped in Part 2, increment Part 2 answer with Part 1 answer
    part2 += part1

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 7: Bridge Repair ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
