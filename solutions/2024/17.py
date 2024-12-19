import numpy as np
from collections import defaultdict
from collections import deque
from functools import cache
import math

input_file = "input17.txt"
example_file = "example17.txt"
example2_file = "example17_2.txt"
example3_file = "example17_3.txt"
example4_file = "example17_4.txt"
example5_file = "example17_5.txt"
example6_file = "example17_6.txt"
example7_file = "example17_7.txt"
example8_file = "example17_8.txt" # actual input with part2 answer for verifying

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part1_example4 = 0
part1_example5 = 0
part1_example6 = 0
part1_example7 = 0
part1_example8 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part2_example7 = 0
part1 = 0
part2 = 0
# opcodes:
# 0: adv division A/2^combop, truncated to int -> A
# 1: bxl bitwisw XOR B ^ litop -> B
# 2: bst comop % 8 -> B
# 3: jnz nop if A = 0, else jump to litop
# 4: bxc bitwise XOR B ^ C -> B
# 5: out combop % 8 then output
# 6: bdv division A/2^combop, truncated to int -> B
# 7: cdv like adv, bdv but -> C
A = 0
B = 0
C = 0
ip = 0
prog_output = []
def getcombop(operand):
    global A
    global B
    global C

    if (operand in [0, 1, 2, 3]):
        return operand
    elif (operand == 4):
        return A
    elif (operand == 5):
        return B
    elif (operand == 6):
        return C
    else:
        print("Invalid operand!")

def alu(opcode, operand):
    global A
    global B
    global C
    global ip
    global prog_output

    if (opcode in [0, 6, 7]): # adv, bdv, cdv
        combop = getcombop(operand)
        
        result = int(A/(2**combop))
        if (opcode == 0):
            A = result
        elif (opcode == 6):
            B = result
        elif (opcode == 7):
            C = result
    elif (opcode in [1, 4]): # bitwise XOR
        if (opcode == 1):
            B = B ^ operand
        elif (opcode == 4):
            B = B ^ C
    elif (opcode == 2): # modulo 8
        combop = getcombop(operand)
        B = combop % 8
    #elif (opcode == 3): # jnz
    #    if (A > 0):
    #        ip = operand
    elif (opcode == 5): # out
        combop = getcombop(operand)
        prog_output.append(str(combop % 8))

    # Update instruction pointer
    if (opcode == 3) and (A > 0):
        ip = operand
    else:
        ip += 2

    # Check if A, B, C overflowed 32-bits
    #MAX = 4294967295
    #if (A > MAX):
    #    A = A & MAX
    #elif (B > MAX):
    #    B = B & MAX 
    #elif (C > MAX):
    #    C = C & MAX 

def process_inputs3(in_file):
    global A
    global B
    global C
    global ip
    global prog_output
    prog_output = []
    ip = 0

    output = 0
    prog = []

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if ("Register A" in line):
                A = int(line.split(": ")[1])
            elif ("Register B" in line):
                B = int(line.split(": ")[1])
            elif ("Register C" in line):
                C = int(line.split(": ")[1])
            elif ("Program" in line):
                prog = line.split(": ")[1]
                prog = prog.split(",")
                prog = [int(x) for x in prog]

            line = file.readline()

    # Alternative 3:
    A_list = []
    orig_A = 8**(len(prog)-1)
    for idx, p in enumerate(prog):
        idx_reverse = (len(prog)-1) - idx
        p_reverse = prog[idx_reverse]
        print(f'Checking idx = {idx_reverse} for {p_reverse}')
        modifier = 8**idx_reverse

        while True:
            # Reset
            A = orig_A
            B = 0
            C = 0
            ip = 0
            prog_output = []

            # Run program
            while (ip < len(prog)):
                opcode = prog[ip]
                operand = prog[ip+1]

                alu(opcode, operand)

            int_prog_output = [int(x) for x in prog_output]
            #if (len(int_prog_output) > idx) and (int_prog_output[idx_reverse] == p_reverse):
            if (int_prog_output[idx_reverse:] == prog[idx_reverse:]):
                A_list.append(orig_A)
                print(orig_A)
                print(int_prog_output)
                break
            orig_A += modifier
    print(A_list)
    output = A_list[-1]
    return output

def process_inputs(in_file):
    global A
    global B
    global C
    global ip
    global prog_output
    prog_output = []
    ip = 0

    output = 0
    prog = []

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if ("Register A" in line):
                A = int(line.split(": ")[1])
            elif ("Register B" in line):
                B = int(line.split(": ")[1])
            elif ("Register C" in line):
                C = int(line.split(": ")[1])
            elif ("Program" in line):
                prog = line.split(": ")[1]
                prog = prog.split(",")
                prog = [int(x) for x in prog]

            line = file.readline()


    # Run program
    while (ip < len(prog)):
        opcode = prog[ip]
        operand = prog[ip+1]

        alu(opcode, operand)
    print(f'Halted: program length is {len(prog)}, ip = {ip}')

    output = ",".join(prog_output)
    # Print
    print(f'A = {A}')
    print(f'B = {B}')
    print(f'C = {C}')
    print(f'Program = {prog}')

    return output

def process_inputs2(in_file):
    global A
    global B
    global C
    global ip
    global prog_output
    prog_output = []
    ip = 0

    output = 0
    prog = []

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if ("Register A" in line):
                A = int(line.split(": ")[1])
            elif ("Register B" in line):
                B = int(line.split(": ")[1])
            elif ("Register C" in line):
                C = int(line.split(": ")[1])
            elif ("Program" in line):
                prog = line.split(": ")[1]
                prog = prog.split(",")
                prog = [int(x) for x in prog]

            line = file.readline()

    # Alternative:
    A = 1
    # 2: 2
    # 4: 4
    # 1: 0
    # 7: 27
    # 5: 6
    # 0: 7
    # 3: 3
    #p = 3
    #A_list = []
    #for p in prog:
    #    A = 0
    #    while True:
    #        B1 = (A % 8) ^ 7
    #        out = int(A/(2**B1)) ^ B1
    #        out = (out ^ 7) % 8

    #        if (out == p):
    #            A_list.append(p)
    #            break

    #        A += 1
    #return A_list
    orig_A = 0
    A_list = []
    for p in prog: # works on all inputs except 7
        print(f'Checking p = {p}')
        orig_A = 0
        while True:
            # Reset
            A = orig_A
            B = 0
            C = 0
            ip = 0
            prog_output = []
            found_A = False

            # Run program
            while (ip < len(prog)):
                opcode = prog[ip]
                operand = prog[ip+1]

                alu(opcode, operand)
                found_A = False
            int_prog_output = [int(x) for x in prog_output]
            if (p != 7):
                if (len(prog_output) == 1) and (int(prog_output[0]) == p):
                    A_list.append(orig_A)
                    break
            elif (len(prog_output)):
                int_prog_output = [int(x) for x in prog_output]
                if (int_prog_output[0] == 7):
                    A_list.append(orig_A)
                    break
            orig_A += 1
            print(orig_A)
    print(A_list)
    print(f'Halted: program length is {len(prog)}, ip = {ip}')
    # Alternative 2
    #output = 0
    #p_dict = {
    #    2: 2,
    #    4: 4,
    #    1: 0,
    #    7: 27,
    #    5: 6,
    #    0: 7,
    #    3: 3
    #}
    #for idx, p in enumerate(prog):
    for idx, p in enumerate(A_list):
        computed = p*(8**(idx))
        output += computed
    return output

    # Run program
    orig_A = 0
    orig_B = B
    orig_C = C
    while True:
        while (ip < len(prog)):
            opcode = prog[ip]
            operand = prog[ip+1]

            alu(opcode, operand)

            if (orig_A == 117440):
                print(prog_output)                
            # Check
            next_A = False
            for idx, i in enumerate(prog_output):
                if (orig_A == 117440):
                    print(f'Compare {int(i)} with {prog[idx]}')

                if (int(i) != prog[idx]):
                    next_A = True
                    break

            if (next_A):
                break

        if (len(prog) == len(prog_output)) and (next_A == False):
            print(len(prog))
            print(len(prog_output))
            print(prog)
            print(prog_output)
            print(orig_A)
            # A was found
            break
        #if (orig_A == 117440):
        #    print(f'orig_A = {orig_A}')
        #    print(f'A = {A}')
        #    print(f'B = {B}')
        #    print(f'C = {C}')
        #    print(f'Program = {prog}')
        #    output = [int(x) for x in prog_output]
        #    print(f'Output  = {output}')
        #    break
        orig_A += 1
        if (orig_A % 1000) == 0:
            print(f'Trying A = {orig_A}')

        # Reset program
        A = orig_A
        B = orig_B
        C = orig_C
        ip = 0
        prog_output = []
    print(f'Halted: program length is {len(prog)}, ip = {ip}')

    output = orig_A
    # Print
    #print(f'A = {A}')
    #print(f'B = {B}')
    #print(f'C = {C}')
    #print(f'Program = {prog}')

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
#part1_example4 = process_inputs(example4_file)
#part1_example5 = process_inputs(example5_file)
#part1_example6 = process_inputs(example6_file)
#part1_example7 = process_inputs(example7_file)\

#part1_example8 = process_inputs(example8_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
#part2_example7 = process_inputs2(example7_file)
#part2 = process_inputs2(input_file)

part2 = process_inputs3(input_file)

print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
#print(f'Part 1 example4: {part1_example4}')
#print(f'Part 1 example5: {part1_example5}')
#print(f'Part 1 example6: {part1_example6}')
#print(f'Part 1 example7: {part1_example7}')
print(f'Part 1 example8: {part1_example8}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2 example7: {part2_example7}')
print(f'Part 2: {part2}')
