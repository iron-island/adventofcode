import re
input_file   = "input8.txt"
example_file = "example08_2.txt"
example_file = "example08.txt"
example_file = "example08_3.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

# Parsing numbers into list of strings from line
# number_list = re.findall(r'\d+', line)

def process_inputs(in_file):
    output = 0

    network_dict = {}
    with open(in_file) as file:
        line = file.readline()

        inst_string = line.strip()
        line = file.readline()
        line = file.readline()

        while line:
            line = line.strip()

            node, lr = line.split(" = ")

            l, r = lr[1:-1].split(", ")

            network_dict[node] = (l, r)

            line = file.readline()

    node = 'AAA'
    i = 0
    while (node != 'ZZZ'):
        inst = inst_string[i]

        if (inst == "L"):
            node = network_dict[node][0]
        elif (inst == "R"):
            node = network_dict[node][1]

        output += 1
        i = (i + 1) % len(inst_string)

    return output

def process_inputs2(in_file):
    output = 0

    network_dict = {}
    nodeA_list = []
    with open(in_file) as file:
        line = file.readline()

        inst_string = line.strip()
        line = file.readline()
        line = file.readline()

        while line:
            line = line.strip()

            node, lr = line.split(" = ")

            l, r = lr[1:-1].split(", ")

            network_dict[node] = (l, r)

            if (node[-1] == 'A'):
                nodeA_list.append(node)

            line = file.readline()

    #stop = False
    #i = 0
    #steps = 0
    #while (stop != True):
    #    inst = inst_string[i]

    #    for idx, node in enumerate(nodeA_list):
    #        node = nodeA_list[idx]

    #        if (inst == "L"):
    #            node = network_dict[node][0]
    #        elif (inst == "R"):
    #            node = network_dict[node][1]

    #        nodeA_list[idx] = node

    #    steps += 1
    #    i = (i + 1) % len(inst_string)

    #    if (steps % 1000000 == 0):
    #        print(steps)

    #    print(f'Step {steps}: {nodeA_list}')
    #    stop = True
    #    for node in nodeA_list:
    #        if (node[-1] != 'Z'):
    #            stop = False
  
    num_nodeZ = len(nodeA_list)
    nodeZ_dict = {} 
    min_steps_list = []
    for nodeA in nodeA_list:
        nodeZ_dict[nodeA] = {'nodeZ_traversed': [], 'steps': []}

    for node in nodeA_list:
        nodeA = node
        i = 0
        steps = 0
        prev_nodeZ = nodeA
        while (True):
            inst = inst_string[i]
            
            if (node[-1] == 'Z'):
                prev_nodeZ = node

            if (inst == "L"):
                node = network_dict[node][0]
            elif (inst == "R"):
                node = network_dict[node][1]

            steps += 1
            i = (i + 1) % len(inst_string)

            if (node[-1] == 'Z'):
                if (node in nodeZ_dict[nodeA]['nodeZ_traversed']):
                    nodeZ_dict[nodeA]['steps'].append((prev_nodeZ, node, steps))
                    break
                else:
                    nodeZ_dict[nodeA]['nodeZ_traversed'].append(node)
                    nodeZ_dict[nodeA]['steps'].append((prev_nodeZ, node, steps))

    print(nodeZ_dict)

    output = 1
    cycle_list = []
    for nodeA in nodeZ_dict:
        _,_,s1 = nodeZ_dict[nodeA]['steps'][0]
        _,_,s2 = nodeZ_dict[nodeA]['steps'][1]

        cycle_list.append(s2-s1)

    print(cycle_list) # solve for math.lcm()
    return output

#part1_example = process_inputs(example_file)
#part1         = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2         = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1        : {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2        : {part2}')

