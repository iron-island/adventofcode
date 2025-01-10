from collections import defaultdict

# Ref: https://stackoverflow.com/questions/6358481/using-functools-lru-cache-with-dictionary-arguments
#from frozendict import frozendict
#
#def freezeargs(func):
#    """Convert a mutable dictionary into immutable.
#    Useful to be compatible with cache
#    """
#
#    @functools.wraps(func)
#    def wrapped(*args, **kwargs):
#        args = (frozendict(arg) if isinstance(arg, dict) else arg for arg in args)
#        kwargs = {k: frozendict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
#        return func(*args, **kwargs)
#    return wrapped

input_file = "../../inputs/2024/input24.txt"
example_file = "example24.txt"
example2_file = "example24_2.txt"
example3_file = "example24_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

wires_dict = defaultdict(int)
gates_dict = defaultdict(tuple)
idx_dict = defaultdict(int)
outwire_list = []

def and_gate(x, y):
    return x & y

def or_gate(x, y):
    return x | y

def xor_gate(x, y):
    return x ^ y

def get_bit_diff(expected, actual):
    i_list = []
    for i in range(0, 46):
        exp_bit = (expected >> i) & 1
        actual_bit = (actual >> i) & 1

        if (exp_bit != actual_bit):
            i_list.append(i)

    return i_list

def dfs_swap(swap_set):
    return 0
    # Swap
    #for subset in swap_set:
    #    wire1, wire2 = subset

    #    idx1 = idx_dict[wire1]
    #    idx2 = idx_dict[wire2]
    #    w1, x1, op1, y1 = gates_list[idx1]
    #    w2, x2, op2, y2 = gates_list[idx2]

    #    gates_list[idx1] = (w1, x2, op2, y2)
    #    gates_list[idx2] = (w2, x1, op1, y1)

    # Simulate

def sim_eval(new_gates_dict, new_wires_dict):
    # Simulate
    cycles = 0
    invalid = False
    while True:
        val_changed = False
        for wire in new_gates_dict:
            x, op, y = new_gates_dict[wire]

            x_val = new_wires_dict[x]
            y_val = new_wires_dict[y]
            new_val = op(x_val, y_val)
            old_val = new_wires_dict[wire]

            if (new_val != old_val):
                new_wires_dict[wire] = new_val
                val_changed = True

        if not (val_changed):
            break

        cycles += 1
        # If it takes too long to settle, we hit a combo loop
        if (cycles > 100):
            invalid = True
            break

    # Evaluate
    output = 0
    for wire in new_gates_dict:
        if ("z" in wire) and new_wires_dict[wire]:
            bit = int(wire[1:])
            output += 2**bit

    return output, invalid

def process_inputs(in_file):
    output = 0

    wires_dict = defaultdict(int)
    gates_dict = defaultdict(tuple)
    and_input_list = []
    xor_input_list = []
    or_input_list = []
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
                elif (op == "OR"):
                    op = or_gate
                elif (op == "XOR"):
                    op = xor_gate
                gates_dict[outwire] = (x, op, y)

            line = file.readline()

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
    output = 0
    for wire in gates_dict:
        if ("z" in wire) and wires_dict[wire]:
            bit = int(wire[1:])
            output += 2**bit

    return output

def process_inputs3(in_file):
    output = 0

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

    # Find incorrect wires
    xor_list = []
    
    # Sum should be z* and output of XOR,
    # except for z45 which is carry bit
    for wire in gates_dict:
        x, op, y = gates_dict[wire]
        if (wire[0] == 'z') and (op != xor_gate) and (wire != 'z45'):
            xor_list.append((wire, op))
    # The only XOR outputs should be z and outputs of x and y that contribute to z
    #swap_with_xor_list = []
    #for wire in gates_dict:
    #    x, op, y = gates_dict[wire]
    #    if ((x[0] == "x") and (y[0] == "y")) or \
    #       ((x[0] == "y") and (y[0] == "x")):
    #        if (op == xor_gate) and (wire[0] != "z"):
    #            # Get bit
    #            bit = x[1:]

    #            sx, sop, sy = gates_dict["z" + bit]
    #            if (wire not in [sx, sy]):
    #                swap_with_xor_list.append((wire, op))
    # Find Cin used as XOR output
    incorrect_cin_list = []
    for wire in xor_input_list:
        if (wire in and_input_list) and (wire[0] not in ["x", "y"]):
            x, op, y = gates_dict[wire]
            if (op == xor_gate) and (x[0] not in ["x", "y"]) and (y[0] not in ["x", "y"]):
                incorrect_cin_list.append(wire)

    # Find AND output not used as OR input for Cout
    # jcq is Cout of bit 0 so exclude it
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

    #print(xor_list)
    #print(incorrect_cin_list)
    #print(incorrect_and_out_list)
    #print(incorrect_AxorB_list)

    # Evaluate
    incorrect_z_list = []
    for t in xor_list:
        z, _ = t
        incorrect_z_list.append(z)
    output = incorrect_z_list + incorrect_cin_list + incorrect_and_out_list + incorrect_AxorB_list
    output.sort()
    output = ','.join(output)
    return output

    ###########################################

    #x_list = []
    #y_list = []
    #z_list = [] # 46 bits
    #x_val = 0
    #y_val = 0
    #for i in range(44, -1, -1):
    #    next_index = False
    #    for wire in wires_dict:
    #        num = wires_dict[wire]
    #        if (str(i) in wire):
    #            if ("x" in wire):
    #                x_list.append(num)
    #                x_val += num*(2**i)
    #                next_index = True
    #                break
    #            elif ("y" in wire):
    #                y_list.append(num)
    #                y_val += num*(2**i)
    #                next_index = True
    #                break
    #        if (next_index):
    #            break
    #        
    #expected_z_val = x_val + y_val
    #print(f'expected: {expected_z_val}')

    #output, invalid = sim_eval(gates_dict, wires_dict)
    #print(f'actual  : {output}')

    ## Get bit differences
    #diff_bit_list = get_bit_diff(expected_z_val, output)

    ##############################################
    ## Sure swaps:
    ##   z09 with gwh
    ##   (z21, z39) with (wbw, jcq)
    ##     based on test: ('z21', 'jcq') ('z39', 'wbw')
    #sure_swap = ("z09", "gwh")
    #wire1_list = ["z21", "z39"]
    #wire2_list = ["wbw", "jcq"]
    #swap_list = [[("z21", "wbw"), ("z39", "jcq")],[("z21", "jcq"), ("z39", "wbw")]]
    #BEST_DIFF = len(diff_bit_list)
    #print(f'BEST_DIFF = {BEST_DIFF}')
    #for swap in swap_list:
    #    pair1, pair2 = swap
    #    wire1, wire2 = pair1
    #    wire3, wire4 = pair2

    #    new_wires_dict = copy.deepcopy(wires_dict)
    #    new_gates_dict = copy.deepcopy(gates_dict)
    #    # Do the swaps
    #    # pair 1
    #    tuple1 = gates_dict[wire1]
    #    tuple2 = gates_dict[wire2]

    #    new_gates_dict[wire1] = tuple2
    #    new_gates_dict[wire2] = tuple1

    #    # pair 2
    #    tuple1 = gates_dict[wire3]
    #    tuple2 = gates_dict[wire4]

    #    new_gates_dict[wire3] = tuple2
    #    new_gates_dict[wire4] = tuple1

    #    # Sure swaps
    #    s1, s2 = sure_swap
    #    tuple1 = gates_dict[s1]
    #    tuple2 = gates_dict[s2]

    #    new_gates_dict[s1] = tuple2
    #    new_gates_dict[s2] = tuple1

    #    # Check
    #    output, invalid = sim_eval(new_gates_dict, new_wires_dict)
    #    if (invalid):
    #        continue
    #    new_diff_bit_list = get_bit_diff(expected_z_val, output)

    #    if (len(new_diff_bit_list) < BEST_DIFF):
    #        print("NEW BEST DIFF")
    #        #print(output)
    #        #print(new_diff_bit_list)
    #        BEST_DIFF = len(new_diff_bit_list)
    #        print(BEST_DIFF, pair1, pair2)

    #output = []

    #return output

def process_inputs2(in_file):
    global wires_dict
    global idx_dict
    global gates_dict
    global outwire_list
    output = 0

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
                elif (op == "OR"):
                    op = or_gate
                elif (op == "XOR"):
                    op = xor_gate
                gates_dict[outwire] = (x, op, y)

            line = file.readline()

    # Create list versoin of gates_dict for memoization
    gates_list = []
    idx = 0
    outwire_list = list(gates_dict.keys())
    for outwire in gates_dict:
        x, op, y = gates_dict[outwire]
        gates_list.append((outwire, x, op, y))
        idx_dict[outwire] = idx

    x_list = []
    y_list = []
    z_list = [] # 46 bits
    x_val = 0
    y_val = 0
    for i in range(44, -1, -1):
        for wire in wires_dict:
            num = wires_dict[wire]
            if (str(i) in wire):
                if ("x" in wire):
                    x_list.append(num)
                    x_val += num*(2**i)
                elif ("y" in wire):
                    y_list.append(num)
                    y_val += num*(2**i)
    expected_z_val = x_val + y_val
    print(expected_z_val)

    output, invalid = sim_eval(gates_dict, wires_dict)
    print(output)

    # Get bit differences
    diff_bit_list = get_bit_diff(expected_z_val, output)
    print(diff_bit_list)

    # Only wires contributing to z{diff_bit_list} needs to be swapped so find them
    visited = set()
    for bit in diff_bit_list:
        if (bit == 0):
            wire = "z00"
        elif (bit < 10):
            wire = "z0" + str(bit)
        else:
            wire = "z" + str(bit)

        # BFS
        q = deque()
        q.append(wire)
        while len(q):
            wire = q.popleft()

            if (wire[0] == "x") or (wire[0] == "y"):
                continue

            if (wire in visited):
                continue
            visited.add(wire)

            x, op, y = gates_dict[wire]
            q.append(x)
            q.append(y)
    # Pruned search space is in visited

    # Check which 1 pair of swaps improves diff_bit_list
    swap_list = list(visited)
    cand_list = []
    cand_set = set()
    INIT_LENGTH = len(diff_bit_list)
    for idx1, wire1 in enumerate(swap_list):
        print(f'Trying idx1 {idx1} of {len(swap_list)-1}')
        for wire2 in swap_list[idx1+1:]:
            new_gates_dict = copy.deepcopy(gates_dict)
            new_wires_dict = copy.deepcopy(wires_dict)

            # Do swap
            tuple1 = gates_dict[wire1]
            tuple2 = gates_dict[wire2]
            new_gates_dict[wire1] = tuple2
            new_gates_dict[wire2] = tuple1

            output, invalid = sim_eval(new_gates_dict, new_wires_dict)
            if (invalid):
                continue
            new_diff_bit_list = get_bit_diff(expected_z_val, output)

            if (len(new_diff_bit_list) < INIT_LENGTH):
                cand_list.append((wire1, wire2))
    print(len(cand_list))

    # From cand_list pick 2 pairs of swaps from cand_list
    cand2_list = []
    for idx1, pair1 in enumerate(cand_list):
        print(f'Trying idx1 {idx1} of {len(cand_list)-1}')
        for pair2 in cand_list[idx1+1:]:
            new_gates_dict = copy.deepcopy(gates_dict)
            new_wires_dict = copy.deepcopy(wires_dict)

            wire1, wire2 = pair1
            wire3, wire4 = pair2

            if (len(set([wire1, wire2, wire3, wire4])) < 4):
                continue

            # Do swap
            for pair in [pair1, pair2]:
                wire1, wire2 = pair

                tuple1 = gates_dict[wire1]
                tuple2 = gates_dict[wire2]
                new_gates_dict[wire1] = tuple2
                new_gates_dict[wire2] = tuple1

            output, invalid = sim_eval(new_gates_dict, new_wires_dict)
            if (invalid):
                continue
            new_diff_bit_list = get_bit_diff(expected_z_val, output)

            if (len(new_diff_bit_list) < INIT_LENGTH):
                cand2_list.append((pair1, pair2))
    print(len(cand2_list)) #3.5M

    # Swap
    #for idx1, wire1 in enumerate(outwire_list):
    #    for idx2, wire2 in enumerate(outwire_list):
    #        if (idx1 == idx2):
    #            continue

    #        subset = frozenset([wire1, wire2])
    #        swap_set = frozenset([subset])
    #        new_swap_set = dfs_swap(swap_set)

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
#part2 = process_inputs2(input_file)
part2 = process_inputs3(input_file)

#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
