from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
time_start = perf_counter()
time_start_process = process_time()

input_file = "../../inputs/2024/input22.txt"

def part1_part2(in_file):
    # Reading the file in one line is marginally faster,
    #   but otherwise runtime savings weren't significant
    with open(in_file) as file:
        init_list = [int(x) for x in file.read().split()]

    # Idea of using arrays with base-19 index which would be
    #   faster than the dictionary is from Reddit user u/notrom11,
    #   though in Python 3.11, 3.12, 3.13 lists are faster
    #   so reverted them to lists
    # Comment: https://www.reddit.com/r/adventofcode/comments/1hjroap/comment/m3cdba8/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # Repo: https://github.com/APMorto/aoc2024/blob/master/day_22_monkey_market/monkey_market.py
    ARRAY_SIZE = 130320 #18*(19**3 + 19**2 + 19 + 1)
    #banana_array = array('H', [0]*ARRAY_SIZE)
    #seq_array = array('H', [0]*ARRAY_SIZE)
    banana_array = [0]*ARRAY_SIZE
    seq_array = [0]*ARRAY_SIZE

    part1 = 0
    for idx_s, secret_num in enumerate(init_list):
        next_idx_s = idx_s+1
        new_secret = secret_num
        for i in range(0, 2000):
            # Original bitwise operations
            #new_secret = (new_secret^(new_secret <<  6)) & 16777215
            #new_secret = (new_secret^(new_secret >>  5)) & 16777215
            #new_secret = (new_secret^(new_secret << 11)) & 16777215

            # Optimize bitwise operations such that there is no single operation result that has more than 24 bits,
            #   and implement shifts as multiplication/integer division:
            #   1. Bit mask by (24-6) = 18 bits first before left shifting and XORing
            #      Bit mask as bitwise operation seems to be marginally faster than modulo for this value
            #   2. No need to bit mask since right shifting ensures that it is always 24 bits
            #   3. Bit mask by (24-11) = 13 bits first before left shifting and XORing
            #      Bit mask implemented as modulo seems to be marginally faster for this value
            new_secret = new_secret^((new_secret & 0b111111111111111111) * 64)
            new_secret = new_secret^(new_secret // 32)
            new_secret = new_secret^((new_secret % 8192) * 2048)

            # TODO: Numbers repeat so we can skip some iterations?
            #if (new_secret in init_set):
            #    num_repeat += 1
            #    print(f'{new_secret} with index {i}  already in init_list! {num_repeat}')

            # Instead of shifting the sequence of changes which we end up just using
            #   as an index, we instead compute the index straight away, and shifting
            #   is done by simply dividing the previous index by 19, and then adding
            #   the new change scaled by 19**3
            # This is equivalent to the following:
            #   changes_list[0] = changes_list[1]
            #   changes_list[1] = changes_list[2]
            #   changes_list[2] = changes_list[3]
            #   changes_list[3] = change
            #   idx_array = changes_list[3]*(19**3) + \
            #               changes_list[2]*(19**2) + \
            #               changes_list[1]*19 + \
            #               changes_list[0]
            d = (new_secret % 10)
            if (i == 0):
                # change = 0
                idx_array = 0
            else:
                # Offset by 9 since change is -9 to +9, still works
                #   without offsets due to negative indices but is slower
                # change = (d - prev_d) + 9
                # Scale by 19**3 = 6859
                idx_array = ((d - prev_d)+9)*(6859) + (prev_idx_array//19)
            prev_d = d
            prev_idx_array = idx_array

            # If there have been a sequence of 4 changes, and the sequence hasn't been seen
            # Instead of marking the sequence as seen or not and clearing them for each new
            #   secret_num, set it to the index+1 whenever its seen to prevent need for clearing
            if (i >= 4):
                if (seq_array[idx_array] <= idx_s):
                    seq_array[idx_array] = next_idx_s

                    # Originally += but was marginally slower for some reason
                    banana_array[idx_array] = banana_array[idx_array] + d

        # Part 1 is a subset of Part 2 so immediately compute Part 1 here
        part1 += new_secret

    part2 = max(banana_array)

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 22: Monkey Market ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

time_end = perf_counter()
time_end_process = process_time()

print("")
print(f'perf_counter (seconds): {time_end - time_start}')
print(f'process_time (seconds): {time_end_process - time_start_process}')
print("")
