#from collections import defaultdict
from array import array

input_file = "../../inputs/2024/input22.txt"

def process_inputs2(in_file, t):
    init_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            init_list.append(int(line))

            line = file.readline()

    #banana_dict = defaultdict(int)
    part1 = 0

    # Idea of using arrays which would be faster than the dictionary
    #   is from Reddit user u/notrom11
    # Comment: https://www.reddit.com/r/adventofcode/comments/1hjroap/comment/m3cdba8/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # Repo: https://github.com/APMorto/aoc2024/blob/master/day_22_monkey_market/monkey_market.py
    ARRAY_SIZE = 18*(19**3 + 19**2 + 19 + 1)
    banana_array = array('H', [0]*ARRAY_SIZE)
    seq_array = array('H', [0]*ARRAY_SIZE)
    #changes_list = [0, 0, 0, 0]
    for idx_s, secret_num in enumerate(init_list):
        next_idx_s = idx_s+1
        new_secret = secret_num
        #changes_list = []
        #changes_list = deque([], 4)
        #changes_set = set()
        prev_idx_array = 0
        for i in range(0, t):
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

            # Record
            #digit_list.append(new_secret % 10)

            # Get changes
            d = (new_secret % 10)
            if (i == 0):
                change = 0
            else:
                change = (d - prev_d) + 9
            prev_d = d

            #changes_list.append(change)

            # Shift register via deque, slower than manual shift register
            #changes_list.append(change)

            # Instead of shifting the sequence of changes which we end up just using
            #   as an index, we instead compute the index straight away, and shifting
            #   is done by simply dividing the previous index by 19
            idx_array = change*(19**3) + (prev_idx_array//19)
            prev_idx_array = idx_array
            if (i >= 4):
                # Manual shift register, faster than deque for maxlen=4
                #changes_list[0] = changes_list[1]
                #changes_list[1] = changes_list[2]
                #changes_list[2] = changes_list[3]
                #changes_list[3] = change

                #seq = tuple(changes_list[(i-3):(i+1)])

                if (seq_array[idx_array] <= idx_s):
                    seq_array[idx_array] = next_idx_s
                    banana_array[idx_array] += d
                # If its the first time that the sequence is seen,
                #   increment the bananas
                #seq = tuple(changes_list)
                #if (seq not in changes_set):
                #    changes_set.add(seq)

                #    # Only increment if difference is non-zero to save some operations
                #    if (d > 0):
                #        banana_dict[seq] += d

        # Part 1 is a subset of Part 2 so immediately compute Part 1 here
        part1 += new_secret

        # Get changes
        #for idx, d in enumerate(digit_list):
        #    if (idx == 0):
        #        change = inf
        #    else:
        #        change = d - (digit_list[idx-1])

        #    changes_list.append(change)

        #    if (idx >= 4):
        #        seq = tuple(changes_list[(idx-3):(idx+1)])
        #        if (seq not in changes_set):
        #            banana_dict[seq] += d
        #            changes_set.add(seq)

        # Record
        #digit_array.append(digit_list)
        #changes_array.append(changes_list)

    #part2 = max(banana_dict.values())
    part2 = max(banana_array)
    
    return part1, part2

    # Evaluate
    #max_banana = 0
    #for seq in banana_dict:
    #    max_banana = max(max_banana, banana_dict[seq])
    #output = max_banana

    # Sliding window
    #max_bananas = 0
    ## Iterate through possible change sequences
    #for change_seq in changes_set:
    #    # Iterate through digit_list and changes_list
    #    for idx_array, digit_list in enumerate(digit_array):

    #return part1, output

#part1_example = process_inputs(example_file,10)
#part1_example2 = process_inputs(example2_file,2000)
#part1 = process_inputs(input_file, 2000)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file, 2000)
part1, part2 = process_inputs2(input_file, 2000)

print("")
print("--- Advent of Code 2024 Day 22: Monkey Market ---")
#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
