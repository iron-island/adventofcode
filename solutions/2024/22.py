#from collections import defaultdict
from array import array

input_file = "../../inputs/2024/input22.txt"

def process_inputs2(in_file):
    init_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            init_list.append(int(line))

            line = file.readline()

    part1 = 0

    # Idea of using arrays which would be faster than the dictionary
    #   is from Reddit user u/notrom11
    # Comment: https://www.reddit.com/r/adventofcode/comments/1hjroap/comment/m3cdba8/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # Repo: https://github.com/APMorto/aoc2024/blob/master/day_22_monkey_market/monkey_market.py
    ARRAY_SIZE = 18*(19**3 + 19**2 + 19 + 1)
    banana_array = array('H', [0]*ARRAY_SIZE)
    seq_array = array('H', [0]*ARRAY_SIZE)
    for idx_s, secret_num in enumerate(init_list):
        next_idx_s = idx_s+1
        new_secret = secret_num
        prev_idx_array = 0
        for i in range(0, 2000):
            # Compute secret in-line to remove function call overheads
            #new_secret = evolve(new_secret)

            # Original bitwise operations
            #new_secret = (new_secret^(new_secret <<  6)) & 16777215
            #new_secret = (new_secret^(new_secret >>  5)) & 16777215
            #new_secret = (new_secret^(new_secret << 11)) & 16777215

            # Optimize bitwise operations such that there is no single operation result that has more than 24 bits:
            #   1. Bit mask by (24-6) = 18 bits first before left shifting and XORing
            #   2. No need to bit mask since right shifting ensures that it is always 24 bits
            #   3. Bit mask by (24-11) = 13 bits first before left shifting and XORing
            new_secret = new_secret^((new_secret & 262143) << 6)
            new_secret = (new_secret^(new_secret >>  5))
            new_secret = new_secret^((new_secret & 8191) << 11)

            # TODO: Numbers repeat so we can skip some iterations?
            #if (new_secret in init_set):
            #    num_repeat += 1
            #    print(f'{new_secret} with index {i}  already in init_list! {num_repeat}')

            # Instead of shifting the sequence of changes which we end up just using
            #   as an index, we instead compute the index straight away, and shifting
            #   is done by simply dividing the previous index by 19
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
                # Instead of saving change, immediately set index value to 0
                #change = 0
                idx_array = 0
            else:
                # Instead of saving change, directly compute the index
                #change = (d - prev_d) + 9
                idx_array = ((d - prev_d)+9)*(19**3) + (prev_idx_array//19)
            prev_d = d
            prev_idx_array = idx_array

            # If there have been a sequence of 4 changes, and the sequence hasn't been seen
            if (i >= 4) and (seq_array[idx_array] <= idx_s):
                seq_array[idx_array] = next_idx_s

                banana_array[idx_array] += d

        # Part 1 is a subset of Part 2 so immediately compute Part 1 here
        part1 += new_secret

    part2 = max(banana_array)
    
    return part1, part2

part1, part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 22: Monkey Market ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
