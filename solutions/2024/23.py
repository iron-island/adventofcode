import numpy as np
from collections import defaultdict
from collections import deque
from functools import cache

input_file = "../../inputs/2024/input23.txt"
example_file = "example23.txt"
example2_file = "example23_2.txt"
example3_file = "example23_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

conn_dict = defaultdict(list)

def check_conn(c1, network):
    valid = True
    for c in network:
        if not (c1 in conn_dict[c]):
            valid = False
            break

    # Base case
    if (valid == False):
        return network

    if (valid):
        network.append(c1)
        for c2 in conn_dict[c1]:
            if (c2 not in network):
                network = check_conn(c2, network)

        return network

def process_inputs(in_file):
    output = 0

    conn_list = []
    conn_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            c1, c2 = line.split("-")
            conn_list.append((c1, c2))
            conn_dict[c1].append(c2)
            conn_dict[c2].append(c1)

            line = file.readline()

    output = 0

    lan_set = set()
    for c1 in conn_dict:
        if (c1[0] == "t"):
            c2_list = conn_dict[c1]
            for idx2, c2 in enumerate(c2_list):
                for idx3 in range(idx2+1, len(c2_list)):
                    c3 = c2_list[idx3]

                    if (c2 in conn_dict[c3]):
                        #output += 1
                        lan_list = [c1, c2, c3]
                        lan_list.sort()
                        lan_set.add(tuple(lan_list))

            if (c1 == "td"):
                print(output)
    output = len(lan_set)

            # Check connections by BFS
            #num = 0
            #q = deque()
            #visited = set()
            #q.append((c1, num))
            #while len(q):
            #    c2, num = q.popleft()

            #    #if (num > 3):
            #    #    break

            #    #if (c2 in visited):
            #    #    break
            #    #visited.add(c2)

            #    if (num == 3) and (c2 == c1):
            #        output += 1
            #        continue

            #    if (num < 3):
            #        for c3 in conn_dict[c2]:
            #            q.append((c3, num+1))

            #if (c1 == "ta"):
            #    print(output)

    print(conn_dict)

    return output

def process_inputs2(in_file):
    global conn_dict
    output = 0

    conn_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            c1, c2 = line.split("-")
            conn_list.append((c1, c2))
            conn_dict[c1].append(c2)
            conn_dict[c2].append(c1)

            line = file.readline()

    output = 0

    MAX_NUM = 0
    max_network = []
    for c1 in conn_dict:
        network = check_conn(c1, [])
        if (len(network) > MAX_NUM):
            MAX_NUM = len(network)
            max_network = network

    # Evaluate
    max_network.sort()
    output = ','.join(max_network)

        # Check connections by BFS
        #q = deque()
        #visited = set()
        #q.append(c1)
        #network_list = []
        #network_list.append(c1)
        #while len(q):
        #    c2 = q.popleft()

        #    if (c2 in visited):
        #        continue
        #    visited.add(c2)

        #    for c3 in conn_dict[c2]:
        #        valid = True
        #        for n in network_list:
        #            if not (c3 in conn_dict[n]):
        #                valid = False
        #                break

        #        if (valid):
        #            q.append(c3)

        #if (c1 == "co"):
        #    print(visited)

        #if (len(visited) > MAX_VISITED):
        #    MAX_VISITED = len(visited)
        #    most_visited = visited

    # Postprocess
    #visited_list = list(most_visited)
    #visited_list.sort()
    #output = ",".join(visited_list)

    return output

part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
