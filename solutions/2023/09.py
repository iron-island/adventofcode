import re
input_file = "../../inputs/2023/input09.txt"
example_file = "example09.txt"
#example_file = "example09_2.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            seq_list = []
            line = line.strip()

            history = line.split()
            #history = re.findall(r'\d+', line)
            # for negative numbers, should be: re.findall(r'[+-]?\d+', line)

            h_list = [int(h) for h in history]
            print(h_list)

            again = True
            curr_seq = h_list
            count = 0
            while again:
                seq = []
                for idx, c in enumerate(curr_seq[:-1]):
                    #if (idx == 3):
                    #    print(curr_seq[idx+1])
                    #    print(c)
                    seq.append(curr_seq[idx+1]-c)

                seq_list.append(seq)

                if (len(set(seq)) != 1):
                    again = True
                else:
                    again = False

                curr_seq = seq

            for i in range(len(seq_list)-1, 0, -1):
                new_val = seq_list[i][-1] + seq_list[i-1][-1]
                seq_list[i-1].append(new_val)

            add_output = seq_list[0][-1] + h_list[-1]
            #print(seq_list)
            #print(add_output)
            output = output + add_output

            line = file.readline()

    return output

def process_inputs2(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            seq_list = []
            line = line.strip()

            history = line.split()
            #history = re.findall(r'\d+', line)

            h_list = [int(h) for h in history]

            again = True
            curr_seq = h_list
            count = 0
            while again:
                seq = []
                for idx, c in enumerate(curr_seq[:-1]):
                    seq.append(curr_seq[idx+1]-c)

                seq_list.append(seq)

                if (len(set(seq)) != 1):
                    again = True
                else:
                    again = False

                curr_seq = seq

            #for i in range(len(seq_list)-1, 0, -1):
            #    new_val = seq_list[i][-1] + seq_list[i-1][-1]
            #    seq_list[i-1].append(new_val)

            for i in range(len(seq_list)-1, 0, -1):
                new_val = seq_list[i-1][0] - seq_list[i][0]
                print(new_val)
                seq_list[i-1].insert(0, new_val)
            print(seq_list)

            add_output = h_list[0] - seq_list[0][0]
            print(add_output)
            output = output + add_output

            line = file.readline()

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
