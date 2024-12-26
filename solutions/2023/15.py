input_file = "../../inputs/2023/input15.txt"
example_file = "example15.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    hash_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            sequence = line.split(",")

            line = file.readline()

    for idx, s in enumerate(sequence):
        curr_hash = 0
        for i in s:
            curr_hash = ((curr_hash + ord(i))*17)%256

        hash_list.append(curr_hash)

    for h in hash_list:
        #print(h)
        output += h

    return output

def myhash(label):

    curr_hash = 0
    for l in label:
        curr_hash = ((curr_hash + ord(l))*17)%256

    return curr_hash

def process_inputs2(in_file):
    output = 0

    hash_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            sequence = line.split(",")

            line = file.readline()

    box_dict = {}
    for i in range(0, 256):
        box_dict[i] = {'labels': {}, 'ordering': []}

    for idx, s in enumerate(sequence):
        if ("-" in s):
            label, b = s.split("-")
            curr_hash = myhash(label)

            if label in box_dict[curr_hash]['labels']:
                # remove lens
                box_dict[curr_hash]['labels'].pop(label)
                box_dict[curr_hash]['ordering'].remove(label)
        elif ("=" in s):
            label, focal = s.split("=")
            curr_hash = myhash(label)

            if (label in box_dict[curr_hash]['labels']):
                # replace
                box_dict[curr_hash]['labels'][label] = focal
            else:
                # add and insert
                box_dict[curr_hash]['labels'][label] = focal
                box_dict[curr_hash]['ordering'].append(label)
        else:
            print("Error!")
            return 0

        #curr_hash = 0
        #for i in s:
        #    curr_hash = ((curr_hash + ord(i))*17)%256

        #hash_list.append(curr_hash)

    for b in box_dict:
        for idx, label in enumerate(box_dict[b]['ordering']):
            slot = idx + 1
            focal = int(box_dict[b]['labels'][label])

            output += (b+1)*(slot)*(focal)

    for h in hash_list:
        #print(h)
        output += h

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
