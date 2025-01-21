from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input23.txt"

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

def part1_part2(in_file):
    global conn_dict

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

    # Part 1
    part1 = 0
    lan_set = set()
    for c1 in conn_dict:
        if (c1[0] == "t"):
            c2_list = conn_dict[c1]
            for idx2, c2 in enumerate(c2_list):
                for idx3 in range(idx2+1, len(c2_list)):
                    c3 = c2_list[idx3]

                    if (c2 in conn_dict[c3]):
                        lan_list = [c1, c2, c3]
                        lan_list.sort()
                        lan_set.add(tuple(lan_list))

    part1 = len(lan_set)

    # Part 2
    part2 = 0
    MAX_NUM = 0
    max_network = []
    for c1 in conn_dict:
        network = check_conn(c1, [])
        if (len(network) > MAX_NUM):
            MAX_NUM = len(network)
            max_network = network

    # Evaluate
    max_network.sort()
    part2 = ','.join(max_network)

    return part1, part2

#part1 = part1(input_file)
#part2 = part2(input_file)
part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 23: LAN Party ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
