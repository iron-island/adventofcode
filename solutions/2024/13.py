from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input13.txt"
example_file = "example13.txt"
example2_file = "example13_2.txt"
example3_file = "example13_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0

part2_example = 0
part2_example2 = 0
part2_example3 = 0

part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    machines = []
    with open(in_file) as file:
        line = file.readline()
   
        a_list = []
        b_list = []
        p_list = []
        anum = 0
        bnum = 0
        pnum = 0
        ax = 0
        ay = 0
        bx = 0
        by = 0
        px = 0
        py = 0 
        while line:
            line = line.strip()
            curr_machine = []

            if ("Button A" in line):
                a_list = line.split(": ")
                anum = a_list[1].split(", ")
                ax = int(anum[0].split("+")[1])
                ay = int(anum[1].split("+")[1])
            elif ("Button B" in line):
                b_list = line.split(": ")
                bnum = b_list[1].split(", ")
                bx = int(bnum[0].split("+")[1])
                by = int(bnum[1].split("+")[1])
            elif ("Prize" in line):
                p_list = line.split(": ")
                pnum = p_list[1].split(", ")
                px = int(pnum[0].split("=")[1])
                py = int(pnum[1].split("=")[1])
            elif (line == ""):
                machines.append([(ax, ay), (bx, by), (px, py)])

            line = file.readline()

        # Last machine
        machines.append([(ax, ay), (bx, by), (px, py)])

    # Compute for each machine
    A_COST = 3
    B_COST = 1
    for m in machines:
        a_tuple, b_tuple, p_tuple = m
        ax, ay = a_tuple
        bx, by = b_tuple
        px, py = p_tuple

        INIT_TOK = A_COST*101 + B_COST*101
        candidate_tok = INIT_TOK
        b_limit = 100
        for a_press in range(0, 101):
            for b_press in range(0, b_limit+1):
                curr_x = ax*a_press + bx*b_press
                curr_y = ay*a_press + by*b_press

                if (curr_x > px):
                    b_limit = b_press 
                    break
                elif (curr_y > py):
                    b_limit = b_press
                    break
                elif ((curr_x, curr_y) == p_tuple):
                    candidate_tok = min(candidate_tok, A_COST*a_press + B_COST*b_press)
                    b_limit = b_press
                    break

        if (candidate_tok < INIT_TOK):
            output += candidate_tok

    return output

def process_inputs2(in_file):
    output = 0

    machines = []
    with open(in_file) as file:
        line = file.readline()
   
        a_list = []
        b_list = []
        p_list = []
        anum = 0
        bnum = 0
        pnum = 0
        ax = 0
        ay = 0
        bx = 0
        by = 0
        px = 0
        py = 0 
        while line:
            line = line.strip()
            curr_machine = []

            if ("Button A" in line):
                a_list = line.split(": ")
                anum = a_list[1].split(", ")
                ax = int(anum[0].split("+")[1])
                ay = int(anum[1].split("+")[1])
            elif ("Button B" in line):
                b_list = line.split(": ")
                bnum = b_list[1].split(", ")
                bx = int(bnum[0].split("+")[1])
                by = int(bnum[1].split("+")[1])
            elif ("Prize" in line):
                p_list = line.split(": ")
                pnum = p_list[1].split(", ")
                px = int(pnum[0].split("=")[1]) + 10000000000000
                py = int(pnum[1].split("=")[1]) + 10000000000000
            elif (line == ""):
                machines.append([(ax, ay), (bx, by), (px, py)])

            line = file.readline()

        # Last machine
        machines.append([(ax, ay), (bx, by), (px, py)])

    # Optimization problem:
    # minimize 3*a_press + b_press for:
    # ax*a_press + bx*b_press = px
    # ay*a_press + by*b_press = py
    # 

    # Compute for each machine
    A_COST = 3
    B_COST = 1
    for m in machines:
        a_tuple, b_tuple, p_tuple = m
        ax, ay = a_tuple
        bx, by = b_tuple
        px, py = p_tuple

        # Compute
        b_press = (ax*py - ay*px)/(ax*by - ay*bx)
        a_press = (px - bx*b_press)/ax

        int_b_press = int(b_press)
        int_a_press = int(a_press)

        if (int_b_press == b_press) and (int_a_press == a_press):
            output += 3*a_press + b_press

        #print(a_press, b_press)

        #INIT_TOK = A_COST*101 + B_COST*101
        #candidate_tok = INIT_TOK
        #b_limit = 100
        #for a_press in range(0, 101):
        #    for b_press in range(0, b_limit+1):
        #        curr_x = ax*a_press + bx*b_press
        #        curr_y = ay*a_press + by*b_press

        #        if (curr_x > px):
        #            b_limit = b_press 
        #            break
        #        elif (curr_y > py):
        #            b_limit = b_press
        #            break
        #        elif ((curr_x, curr_y) == p_tuple):
        #            candidate_tok = min(candidate_tok, A_COST*a_press + B_COST*b_press)
        #            b_limit = b_press
        #            break

        #if (candidate_tok < INIT_TOK):
        #    output += candidate_tok

    return int(output)

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2_example2 = process_inputs2(example2_file)
#part2_example3 = process_inputs2(example3_file)
part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 13: Claw Contraption ---")
#print(f'Part 1 example: {part1_example}')
#print(f'Part 1 example2: {part1_example2}')
#print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
#print(f'Part 2 example2: {part2_example2}')
#print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
