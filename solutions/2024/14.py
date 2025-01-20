from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input14.txt"

MAX_ROW = 102
MAX_COL = 100

def part1_part2(in_file):
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

    # Part 1
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

    # Part 2
    #NUM = 0
    #final_pos_list = []
    #while (True):
    #    NUM += 1
    #    final_pos_list = []
    #    invalid = False
    #    for idx, robot in enumerate(robots_list):
    #        x, y = robot[0]
    #        vx, vy = robot[1]

    #        x = x + NUM*vx
    #        y = y + NUM*vy

    #        n_x = x % (MAX_COL+1)
    #        n_y = y % (MAX_ROW+1)

    #        if ((n_x, n_y) in final_pos_list):
    #            invalid = True
    #            break

    #        final_pos_list.append((n_x, n_y))

    #    if (not invalid):
    #        part2 = NUM
    #        break

    # Part 2
    # Optimized by finding the minimum steps needed for minimum variance
    #   across x and y axes (corresponds to repeated horizontal and
    #   vertical patterns, compute steps where both patterns appear
    #   (can be mathematically modelled as 2 congruencies)
    # I didn't think of this at all, this is from Reddit:
    #   https://www.reddit.com/r/adventofcode/comments/1hts3v2/comment/m5ht5o2/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # Congruencies can be solved with the Chinese Remainder Theorem or
    #   alternatively with a closed-form expression based on Reddit:
    #   https://www.reddit.com/r/adventofcode/comments/1hts3v2/comment/m5i7uan/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

    # Simulate max(LEN_X, LEN_Y) times, computing the variance for each iteration
    #   across x and y axes:
    LEN_X = MAX_COL+1
    LEN_Y = MAX_ROW+1
    MAX_STEPS = max(LEN_X, LEN_Y)
    NUM_ROBOTS = len(robots_list)
    step = 0
    min_var_x = 100000000
    min_var_y = 100000000
    while (step < MAX_STEPS):
        # Simulate
        sum_x = 0
        sum_y = 0
        for idx in range(0, NUM_ROBOTS):
            x, y = robots_list[idx][0]
            vx, vy = robots_list[idx][1]

            x = x + vx
            y = y + vy

            n_x = x % LEN_X
            n_y = y % LEN_Y

            # Precompute mean (without division) to be used for variance computation later
            sum_x += n_x
            sum_y += n_y

            # Update values
            robots_list[idx][0] = (n_x, n_y)

        # Compute variances (without division)
        mean_x = sum_x/NUM_ROBOTS
        mean_y = sum_y/NUM_ROBOTS
        var_x = 0
        var_y = 0
        for robot in robots_list:
            x, y = robot[0]

            var_x += (x - mean_x)**2
            var_y += (y - mean_y)**2

        # Update steps since robots already moved
        step += 1

        # Check minimum variances (without division)
        if (var_x < min_var_x):
            min_x = step
            min_var_x = var_x

        if (var_y < min_var_y):
            min_y = step
            min_var_y = var_y

    # Mod to try to cover other available puzzle inputs,
    #   since steps were simulated at max(LEN_X, LEN_Y)
    min_x = min_x % LEN_X
    min_y = min_y % LEN_Y

    part2 = (51*(min_x*LEN_Y + min_y*LEN_X)) % (LEN_Y*LEN_X)

    return part1, part2

part1, part2 = part1_part2(input_file)

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
