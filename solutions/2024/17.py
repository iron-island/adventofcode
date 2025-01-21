from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input17.txt"

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
prog = []

# NOTE: Runtime is minimal (<30ms) with and without cache,
#       so caching wasn't added to avoid overheads
def dfs_quine(A_tuple, idx):
    global A
    global B
    global C
    global ip
    global prog_output

    # Regenerate orig_A
    orig_A = 0
    for i in range(idx+1, 16):
        orig_A += A_tuple[i]*(8**i)

    # Iterate through possible 3-bit values that gets
    #   the desired program output
    A_list = list(A_tuple)
    for i in range(0, 8):
        curr_A = orig_A + i*(8**idx)

        # Reset
        A = curr_A
        B = 0
        C = 0
        ip = 0
        prog_output = []
        
        # Run program
        while (ip < len(prog)):
            opcode = prog[ip]
            operand = prog[ip+1]

            alu(opcode, operand)

        # Check program output
        int_prog_output = [int(x) for x in prog_output]
        if (int_prog_output[idx:] == prog[idx:]):
            # Base case
            if (idx == 0):
                return curr_A, True

            # Recursion
            A_list[idx] = i
            next_curr_A, early_exit = dfs_quine(tuple(A_list), idx-1)

            # Early exit
            if (early_exit):
                return next_curr_A, True

    # Default return if there are no program outputs across all possible
    #   3-bit values for current index
    return 0, False

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
    #else:
    #    print("Invalid operand!")

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

def part1_part2(in_file):
    global A
    global B
    global C
    global ip
    global prog_output
    global prog
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

    # Part 1
    # Run program
    while (ip < len(prog)):
        opcode = prog[ip]
        operand = prog[ip+1]

        alu(opcode, operand)
    part1 = ",".join(prog_output)

    # Part 2
    part2, _ = dfs_quine(tuple(16*[0]), 15)

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 17: Chronospatial Computer ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
