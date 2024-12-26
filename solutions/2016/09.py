from functools import cache

input_file = "../../inputs/2016/input09.txt"
example_file = "example09.txt"
example2_file = "example09_2.txt"
example3_file = "example09_3.txt"
example4_file = "example09_4.txt"
example5_file = "example09_5.txt"
example6_file = "example09_6.txt"
example7_file = "example09_7.txt"
example8_file = "example09_8.txt"
example9_file = "example09_9.txt"
example10_file = "example09_10.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part1_example4 = 0
part1_example5 = 0
part1_example6 = 0

part2_example7 = 0
part2_example8 = 0
part2_example9 = 0
part2_example10 = 0
part1 = 0
part2 = 0

@cache
def dfs(seq):
    length = 0
    num = None
    repeat = None
    s_idx = None
    e_idx = None
    idx = 0
    while (idx < len(seq)):
        s = seq[idx]
        if (s == "(") and (s_idx == None):
            s_idx = idx
        elif (s == ")") and (e_idx == None):
            e_idx = idx

            # Parse numbers
            marker = seq[s_idx+1:e_idx]
            num, repeat = marker.split("x")
            num = int(num)
            repeat = int(repeat)
        elif (num != None):
            subsequent = seq[idx:idx+num]

            length += dfs(repeat*subsequent)

            # Move index
            idx += num

            # Reinitialize
            num = None
            repeat = None
            s_idx = None
            e_idx = None

            continue
        elif (s_idx, e_idx) == (None, None):
            length += 1

        idx += 1

    return length

def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            seq = line

            line = file.readline()

    decomp = ""
    num = None
    repeat = None
    s_idx = None
    e_idx = None
    idx = 0
    while (idx < len(seq)):
        s = seq[idx]
        if (s == "(") and (s_idx == None):
            s_idx = idx
        elif (s == ")") and (e_idx == None):
            e_idx = idx

            # Parse numbers
            marker = seq[s_idx+1:e_idx]
            num, repeat = marker.split("x")
            num = int(num)
            repeat = int(repeat)
        elif (num != None):
            print(num, repeat)
            subsequent = seq[idx:idx+num]
            print(subsequent)
            print(decomp)

            decomp += repeat*subsequent

            # Move index
            idx += num

            # Reinitialize
            num = None
            repeat = None
            s_idx = None
            e_idx = None

            continue
        elif (s_idx, e_idx) == (None, None):
            decomp += s

        idx += 1

    print(decomp)

    output = len(decomp)

    return output

def process_inputs2(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            seq = line

            line = file.readline()

    # DFS
    output = dfs(seq)

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
#part1_example4 = process_inputs(example4_file)
#part1_example5 = process_inputs(example5_file)
#part1_example6 = process_inputs(example6_file)
#part1 = process_inputs(input_file)

part2_example7 = process_inputs2(example7_file)
part2_example8 = process_inputs2(example8_file)
part2_example9 = process_inputs2(example9_file)
part2_example10 = process_inputs2(example10_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1 example4: {part1_example4}')
print(f'Part 1 example5: {part1_example5}')
print(f'Part 1 example6: {part1_example6}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example7: {part2_example7}')
print(f'Part 2 example8: {part2_example8}')
print(f'Part 2 example9: {part2_example9}')
print(f'Part 2 example10: {part2_example10}')
print(f'Part 2: {part2}')
