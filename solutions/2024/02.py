from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input02.txt"

def part1_part2(in_file):
    part1 = 0
    part2 = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            report = line.split()

            orig_rep = [int(r) for r in report]

            # Early check for the trend of the levels
            safe = True
            if (orig_rep[0] == orig_rep[1]):
                safe = False
            elif (orig_rep[0] > orig_rep[1]):
                higher = False
            else:
                higher = True

            # Check if unmodified levels are safe
            if (safe):
                for idx in range(1, len(orig_rep)):
                    r  = orig_rep[idx]
                    r2 = orig_rep[idx-1]
                    if (higher) and (r > r2):
                        diff = abs(r - r2)
                    elif (not higher) and (r < r2):
                        diff = abs(r - r2)
                    else:
                        safe = False
                        break

                    if (diff >= 1) and (diff <= 3):
                        safe = True
                        continue
                    else:
                        safe = False
                        break

            # Part 1: Count number of safe levels
            # Part 2: Count number of unsafe levels that can be turned safe
            if (safe):
                part1 += 1
            else:
                for idx2, level in enumerate(report):
                    orig_rep = [int(r) for r in report]    
                    orig_rep.pop(idx2)

                    safe = True
                    if (orig_rep[0] == orig_rep[1]):
                        safe = False
                    elif (orig_rep[0] > orig_rep[1]):
                        higher = False
                    else:
                        higher = True

                    if (safe):
                        for idx in range(1, len(orig_rep)):
                            r  = orig_rep[idx]
                            r2 = orig_rep[idx-1]
                            if (higher) and (r > r2):
                                diff = abs(r - r2)
                            elif (not higher) and (r < r2):
                                diff = abs(r - r2)
                            else:
                                safe = False
                                break

                            if (diff >= 1) and (diff <= 3):
                                safe = True
                                continue
                            else:
                                safe = False
                                break

                    if (safe):
                        part2 += 1
                        break

            line = file.readline()

    # Add the originally safe levels to the safe levels after modification
    part2 += part1

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 2: Red-Nosed Reports ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
