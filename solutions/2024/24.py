from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

from collections import defaultdict

input_file = "../../inputs/2024/input24.txt"

wires_dict = defaultdict(int)
gates_dict = defaultdict(tuple)

def and_gate(x, y):
    return x & y

def or_gate(x, y):
    return x | y

def xor_gate(x, y):
    return x ^ y

def part1_part2(in_file):
    wires_dict = defaultdict(int)
    gates_dict = defaultdict(tuple)
    and_input_list = []
    or_input_list = []
    xor_input_list = []
    with open(in_file) as file:
        line = file.readline()
    
        get_gates = False
        while line:
            line = line.strip()

            if (line == ""):
                get_gates = True
            elif not (get_gates):
                wire, init = line.split(": ")
                wires_dict[wire] = int(init)
            else:
                operation, outwire = line.split(" -> ")
                x, op, y = operation.split(" ")
                if (op == "AND"):
                    op = and_gate
                    and_input_list.append(x)
                    and_input_list.append(y)
                elif (op == "OR"):
                    op = or_gate
                    or_input_list.append(x)
                    or_input_list.append(y)
                elif (op == "XOR"):
                    op = xor_gate
                    xor_input_list.append(x)
                    xor_input_list.append(y)
                gates_dict[outwire] = (x, op, y)

            line = file.readline()

    # Part 1
    # Simulate
    while True:
        val_changed = False
        for wire in gates_dict:
            x, op, y = gates_dict[wire]

            x_val = wires_dict[x]
            y_val = wires_dict[y]
            new_val = op(x_val, y_val)
            old_val = wires_dict[wire]

            if (new_val != old_val):
                wires_dict[wire] = new_val
                val_changed = True

        if not (val_changed):
            break

    # Evaluate
    part1 = 0
    for wire in gates_dict:
        if ("z" in wire) and wires_dict[wire]:
            bit = int(wire[1:])
            part1 += 2**bit

    # Part 2
    # Find incorrect wires
    xor_list = []
    
    # Sum should be z* and output of XOR,
    # except for z45 which is carry bit
    for wire in gates_dict:
        x, op, y = gates_dict[wire]
        if (wire[0] == 'z') and (op != xor_gate) and (wire != 'z45'):
            xor_list.append((wire, op))
    # Find Cin used as XOR output
    incorrect_cin_list = []
    for wire in xor_input_list:
        if (wire in and_input_list) and (wire[0] not in ["x", "y"]):
            x, op, y = gates_dict[wire]
            if (op == xor_gate) and (x[0] not in ["x", "y"]) and (y[0] not in ["x", "y"]):
                incorrect_cin_list.append(wire)

    # Find AND output not used as OR input for Cout
    # jcq is Cout of bit 0 so exclude it
    # TODO: programmatically exclude jcq instead of hardcoding to generalize across other puzzle inputs
    incorrect_and_out_list = []
    for wire in gates_dict:
        x, op, y = gates_dict[wire]
        if (op == and_gate) and (wire[0] != "z") and (wire != "jcq"):
            if (wire not in or_input_list) or (wire in and_input_list) or (wire in xor_input_list):
                incorrect_and_out_list.append(wire)

    # Find A XOR B output that is not used as AND input and XOR input
    incorrect_AxorB_list = []
    for wire in gates_dict:
        x, op, y = gates_dict[wire]
        if (op == xor_gate) and (wire[0] != "z"):
            if (wire not in and_input_list) or (wire not in xor_input_list):
                incorrect_AxorB_list.append(wire)

    # Evaluate
    incorrect_z_list = []
    for t in xor_list:
        z, _ = t
        incorrect_z_list.append(z)
    incorrect_wires_list = incorrect_z_list + incorrect_cin_list + incorrect_and_out_list + incorrect_AxorB_list
    incorrect_wires_list.sort()
    part2 = ','.join(incorrect_wires_list)

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 24: Crossed Wires ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
