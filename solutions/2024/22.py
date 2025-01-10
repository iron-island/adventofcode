#from collections import defaultdict
from math import inf
from array import array

input_file = "../../inputs/2024/input22.txt"
example_file = "example22.txt"
example2_file = "example22_2.txt"
example3_file = "example22_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

def move_dir(rc, direction):
    row, col = rc

    #assert(direction in ["up", "down", "left", "right"])
    if (direction == "up"):
        n_row = row-1
        n_col = col
    elif (direction == "down"):
        n_row = row+1
        n_col = col
    elif (direction == "left"):
        n_row = row
        n_col = col-1
    elif (direction == "right"):
        n_row = row
        n_col = col+1

    return (n_row, n_col)

def mix(secret_num, val):
    new_secret = secret_num ^ val
    return new_secret

def prune(secret_num):
    # Get lowest 24 bits

    # Through modulus
    #new_secret = secret_num % 16777216
    # Through bitmask
    new_secret = secret_num & 16777215
    return new_secret

def evolve(secret_num):
    # Right shift by 6 bits before mixing and pruning
    #val = secret_num*64
    #new_secret = mix(secret_num, val)
    #new_secret = prune(new_secret)
    new_secret = (secret_num^(secret_num << 6)) & 16777215

    # Right shift by 5 bits before mixing and pruning
    #val = int(new_secret/32)
    #new_secret = mix(new_secret, val)
    #new_secret = prune(new_secret)
    new_secret = (new_secret^(new_secret >> 5)) & 16777215
   
    # Left shift by 11 bits before mixing and pruning
    #val = new_secret*2048
    #new_secret = mix(new_secret, val)
    #new_secret = prune(new_secret)
    new_secret = (new_secret^(new_secret << 11)) & 16777215

    return new_secret

def process_inputs(in_file, t):
    output = 0

    init_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            init_list.append(int(line))

            line = file.readline()

    last_secret_list = []
    for secret_num in init_list:
        new_secret = secret_num
        for i in range(0, t):
            new_secret = evolve(new_secret)

        # Record
        last_secret_list.append(new_secret)

    # Evaluate
    for s in last_secret_list:
        output += s

    return output

def process_inputs2(in_file, t):
    output = 0

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
    for idx_s, secret_num in enumerate(init_list):
        next_idx_s = idx_s+1
        new_secret = secret_num
        #changes_list = []
        changes_list = [0, 0, 0, 0]
        #changes_list = deque([], 4)
        #changes_set = set()
        for i in range(0, t):
            # Compute secret in-line to remove function call overheads
            #new_secret = evolve(new_secret)
            new_secret = (new_secret^(new_secret <<  6)) & 16777215
            new_secret = (new_secret^(new_secret >>  5)) & 16777215
            new_secret = (new_secret^(new_secret << 11)) & 16777215

            # TODO: Numbers repeat so we can skip some iterations?
            #if (new_secret in init_set):
            #    num_repeat += 1
            #    print(f'{new_secret} with index {i}  already in init_list! {num_repeat}')

            # Record
            #digit_list.append(new_secret % 10)

            # Get changes
            d = (new_secret % 10)
            if (i == 0):
                change = inf
            else:
                change = d - prev_d
            prev_d = d

            #changes_list.append(change)

            # Manual shift register, faster than deque for maxlen=4
            changes_list[0] = changes_list[1]
            changes_list[1] = changes_list[2]
            changes_list[2] = changes_list[3]
            changes_list[3] = change

            # Shift register via deque, slower than manual shift register
            #changes_list.append(change)

            if (i >= 4):
                #seq = tuple(changes_list[(i-3):(i+1)])

                idx_array = changes_list[3]*19**3 + \
                            changes_list[2]*19**2 + \
                            changes_list[1]*19 + \
                            changes_list[0]
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

#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
