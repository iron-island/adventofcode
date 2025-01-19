from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input14.txt"

def process_inputs(in_file, MAX_ROW, MAX_COL):
    part1 = 0

    grid = []
    robots_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            p_str, v_str = line.split()

            x, y = p_str[2:].split(",")
            x = int(x)
            y = int(y)

            vx, vy = v_str[2:].split(",")
            vx = int(vx)
            vy = int(vy)

            robots_list.append([(x, y), (vx, vy)])

            line = file.readline()

    # Simulate
    NUM = 100
    final_pos_list = []
    for idx, robot in enumerate(robots_list):
        x, y = robot[0]
        vx, vy = robot[1]

        x = x + NUM*vx
        y = y + NUM*vy

        n_x = x % (MAX_COL+1)
        n_y = y % (MAX_ROW+1)

        final_pos_list.append((n_x, n_y))

    # Check quadrants
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    X_MID = MAX_COL/2
    Y_MID = MAX_ROW/2
    for pos in final_pos_list:
        x, y = pos

        if (x < X_MID) and (y < Y_MID):
            q1 += 1
        elif (x > X_MID) and (y < Y_MID):
            q2 += 1
        elif (x < X_MID) and (y > Y_MID):
            q3 += 1
        elif (x > X_MID) and (y > Y_MID):
            q4 += 1

    part1 = q1*q2*q3*q4

    return part1

def process_inputs2(in_file, MAX_ROW, MAX_COL):
    part2 = 0

    grid = []
    robots_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            p_str, v_str = line.split()

            x, y = p_str[2:].split(",")
            x = int(x)
            y = int(y)

            vx, vy = v_str[2:].split(",")
            vx = int(vx)
            vy = int(vy)

            robots_list.append([(x, y), (vx, vy)])

            line = file.readline()

    # Simulate
    NUM = 0
    final_pos_list = []
    while (True):
        NUM += 1
        final_pos_list = []
        invalid = False
        for idx, robot in enumerate(robots_list):
            x, y = robot[0]
            vx, vy = robot[1]

            x = x + NUM*vx
            y = y + NUM*vy

            n_x = x % (MAX_COL+1)
            n_y = y % (MAX_ROW+1)

            if ((n_x, n_y) in final_pos_list):
                invalid = True
                break

            final_pos_list.append((n_x, n_y))

        if (not invalid):
            part2 = NUM
            return part2

part1 = process_inputs(input_file, 102, 100)
part2 = process_inputs2(input_file, 102, 100)

print("")
print("--- Advent of Code 2024 Day 14: Restroom Redoubt ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
