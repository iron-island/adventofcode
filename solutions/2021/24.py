import math
import copy
import numpy as np
from frozendict import frozendict
from collections import defaultdict
from functools import cache

input_file = "../../inputs/2021/input24.txt"
example_file = "example24.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def get_z(prev_z: int, w: int, params: tuple):
    A, B, C = params

    x = (prev_z % 26) + B
    #x = int(np.fmod(prev_z, 26)) + B

    if (x != w):
        x = 1
    else:
        x = 0

    z = int(prev_z/A)*(25*x + 1) + (w + C)*x

    return z

def dfs_w(digit, params_dict, prev_z_dict, prev_z, PART1=False):
    if (digit < 14):
        required_z_set = prev_z_dict[digit+1]
    else:
        required_z_set = set()
        required_z_set.add(0)

    params = params_dict[digit]
    if (PART1):
        WRANGE = range(9, 0, -1)
    else:
        WRANGE = range(1, 10)
    for w in WRANGE:
        z = get_z(prev_z, w, params)

        if (z in required_z_set):
            # Base case
            if (digit == 14):
                return str(w), True
            else:
                next_w, is_valid = dfs_w(digit+1, params_dict, prev_z_dict, z, PART1)

                if (is_valid):
                    return str(w)+next_w, True

    return "", False

def alu(instr, var_dict, num):
    if ("inp" in instr):
        var = instr.split(" ")[1]

        var_dict[var] = num
    elif ("add" in instr):
        _, a, b = instr.split(" ")


        if (b in var_dict):
            num2 = var_dict[b]
        else:
            num2 = int(b)

        var_dict[a] += num2
    elif ("mul" in instr):
        _, a, b = instr.split(" ")

        if (b in var_dict):
            num2 = var_dict[b]
        else:
            num2 = int(b)

        var_dict[a] *= num2
    elif ("div" in instr):
        _, a, b = instr.split(" ")

        if (b in var_dict):
            num2 = var_dict[b]
        else:
            num2 = int(b)

        quotient = var_dict[a]/num2

        # Truncate towards 0
        if (quotient >= 0):
            var_dict[a] = math.floor(quotient)
        else:
            var_dict[a] = math.ceil(quotient)
    elif ("mod" in instr):
        _, a, b = instr.split(" ")

        if (b in var_dict):
            num2 = var_dict[b]
        else:
            num2 = int(b)

        var_dict[a] = var_dict[a] % num2
    elif ("eql" in instr):
        _, a, b = instr.split(" ")

        if (b in var_dict):
            num2 = var_dict[b]
        else:
            num2 = int(b)

        if (var_dict[a] == num2):
            var_dict[a] = 1
        else:
            var_dict[a] = 0

    return var_dict

@cache
def dfs_monad(instr_tuple, var_frozendict):
    model_num = ""
    for num in range(9, 0, -1):
        var_dict = defaultdict(int)
        for var in var_frozendict:
            var_dict[var] = var_frozendict[var]

        next_idx = None
        for idx, instr in enumerate(instr_tuple):
            #print(instr)

            if ("inp" in instr):
                var_dict = alu(instr, var_dict, num)
                next_idx = idx+1
                break
            else:
                var_dict = alu(instr, var_dict, num)
            #print(var_dict)

        # Base case: if last_idx is None, then instructions finished until the end and
        #            we can start checking if its a valid model number
        if (next_idx == None):
            if (var_dict['z'] == 0):
                return "", True
            else:
                return "", False

        instr_list = list(instr_tuple)
        next_instr_tuple = tuple(instr_list[next_idx:])

        # Recursion
        next_num, is_valid = dfs_monad(next_instr_tuple, frozendict(var_dict))

        if (is_valid):
            model_num = str(num) + next_num
            return model_num, True

    return model_num, False

def process_inputs(in_file):
    output = 0

    instr_list = []
    var_dict = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            instr_list.append(line)

            line = file.readline()

    # DFS
    #output, is_valid = dfs_monad(tuple(instr_list), frozendict(var_dict))
    #assert(is_valid == True)

    # Check if all instructions grouped by "inp w" have the same structure
    # Prepopulate first for digit 1
    prev_digit_instr_list = []
    for idx, instr in enumerate(instr_list):
        if (idx == 0):
            continue

        if ("inp" in instr):
            next_digit_start = idx + 1
            break
        else:
            op, a, b = instr.split(" ")

            if (b in var_dict):
                prev_digit_instr_list.append((op, a, b))
            else:
                prev_digit_instr_list.append((op, a))

    # Check remaining digits 2 to 14
    digit_instr_list = []
    digit = 2
    MAX_IDX = len(instr_list)-1
    for idx in range(next_digit_start, MAX_IDX+1):
        instr = instr_list[idx]

        if ("inp" in instr) or (idx == MAX_IDX):
            # Record last instruction before checking
            if (idx == MAX_IDX):
                op, a, b = instr.split(" ")
                if (b in var_dict):
                    digit_instr_list.append((op, a, b))
                else:
                    digit_instr_list.append((op, a))

            if (prev_digit_instr_list == digit_instr_list):
                print(f'Digit {digit} instructions same as digit {digit-1}!')
            else:
                print(f'Digit {digit} instructions different from digit {digit-1}!')
            prev_digit_instr_list = copy.deepcopy(digit_instr_list)
            digit_instr_list = []
            digit += 1
        else:
            op, a, b = instr.split(" ")
            if (b in var_dict):
                digit_instr_list.append((op, a, b))
            else:
                digit_instr_list.append((op, a))

    # Results show that instructions for all digits have the same structure
    # Record parameters for equation
    # There are 3 parameters A, B, C:
    #    A: comes from first "div z <A>" instruction
    #    B: comes from first "add x <B>" instruction
    #    C: comes from first "add y <C>" instruction directly after first "add y w"
    digit = 0
    params_dict = defaultdict(tuple)
    for instr in instr_list:
        if ("inp" in instr):
            digit += 1
            get_A = True
            get_B = False
            get_C = False
            params_list = []
        elif (get_A and ("div z" in instr)):
            op, a, A = instr.split(" ")

            if (A not in var_dict):
                params_list.append(int(A))
                get_A = False
                get_B = True
        elif (get_B and ("add x" in instr)):
            op, a, B = instr.split(" ")

            if (B not in var_dict):
                params_list.append(int(B))
                get_B = False
        elif ("add y w" == instr):
            get_C = True
        elif (get_C and ("add y" in instr)):
            op, a, C = instr.split(" ")

            if (C not in var_dict):
                params_list.append(int(C))
                get_C = False

                params_dict[digit] = tuple(params_list)
        else:
            continue
    print(params_dict)

    # Backtrack to get required z from previous digits
    prev_z_dict = defaultdict(set)
    MAX_PREV_Z = -math.inf
    for digit in range(14, 0, -1):
        prev_z_set = set()
        params = params_dict[digit]
        A = params[0]

        if (digit < 14):
            required_z_set = copy.deepcopy(prev_z_dict[digit+1])
        for w in range(9, 0, -1):
        #for w in range(1, 10):
            #for prev_z in range(-26, 26):
            #for prev_z in range(0, 1000000):
            for prev_z in range(0, 400000):
                z = get_z(prev_z, w, params)

                if (digit < 14):
                    if (z in required_z_set):
                        prev_z_set.add(prev_z)
                        MAX_PREV_Z = max(MAX_PREV_Z, prev_z)
                elif (z == 0):
                    prev_z_set.add(prev_z)
                    MAX_PREV_Z = max(MAX_PREV_Z, prev_z)

        assert(len(prev_z_set))
        prev_z_dict[digit] = prev_z_set
    print(prev_z_dict)
    print(f'Max prev_z: {MAX_PREV_Z}')

    # Compute w digits that satisfies values in prev_z_dict
    # Same DFS function can be used, only early exit condition would change
    #   since part 1 would start from 9 to 1 while part 2 starts from 1 to 9
    PART1 = True
    part1, is_valid = dfs_w(1, params_dict, prev_z_dict, 0, PART1)
    assert(is_valid == True)

    PART1 = False
    part2, is_valid = dfs_w(1, params_dict, prev_z_dict, 0, PART1)
    assert(is_valid == True)

    # Digit 14: Get possible z13
    #print("Possible values for w14 and z13:")
    #z13_set = set()
    #for w14 in range(9, 0, -1):
    #    for z13 in range(-26, 27):
    #        x14 = (z13 % 26) - 11

    #        if (x14 != w14):
    #            x14 = 1
    #        else:
    #            x14 = 0

    #        z14 = int(z13/26)*(25*x14 + 1) + (w14 + 9)*x14

    #        if (z14 == 0):
    #            print(f'w14 = {w14}, z13 = {z13}, x14 = {x14}')
    #            z13_set.add(z13)

    ## Digit 13
    #print("Possible values for w13 and z12:")
    #z12_set = set()
    #for w13 in range(9, 0, -1):
    #    for z12 in range(-26, 27):
    #        x13 = (z12 % 26) + 13

    #        if (x13 != w13):
    #            x13 = 1
    #        else:
    #            x13 = 0

    #        z13 = int(z12)*(25*x13 + 1) + (w13 + 10)*x13
    #        if (z13 in z13_set):
    #            print(f'w13 = {w13}, z12 = {z12}, z13 = {z13}')
    #            z12_set.add(z12)

    ## Digit 12
    #print("Possible values for w12 and z11:")
    #z11_set = set()
    #for w12 in range(9, 0, -1):
    #    for z11 in range(-26, 27):
    #        x12 = (z11 % 26) - 8

    #        if (x12 != w12):
    #            x12 = 1
    #        else:
    #            x12 = 0

    #        z12 = int(z11/26)*(25*x12 + 1) + (w12 + 4)*x12
    #        if (z12 in z12_set):
    #            print(f'w12 = {w12}, z11 = {z11}, z12 = {z12}')

    return part1, part2

part1, part2 = process_inputs(input_file)

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
