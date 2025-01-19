from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input03.txt"

def mul(x,y):
    
    return int(x)*int(y)

def part1_part2(in_file):
    with open(in_file) as file:
        line = file.readline()
        nextline = line

        while nextline:
            line = line.strip()
            nextline = file.readline()
            line = line + nextline

    # Part 1
    part1 = 0
    i = 0
    part1_line = line
    while i != -1:
        i = part1_line.find("mul(")
        if (i > 0):
            subline = part1_line[i+1:]
            j = subline.find(")")

            if (j > 0):
                try:
                    product = eval(part1_line[i:(i+j+2)])
                    part1 += product
                except:
                    product = 0

                part1_line = part1_line[i+1:]

    # Part 2
    # Find do() and don't()
    part2 = 0
    i = 0
    enabled_line = ""
    dont_split = line.split("don't()")
    enabled_line = dont_split[0]
    dont_split = dont_split[1:]
    for d in dont_split:
        if ("do()" in d):
            d_split = d.split("do()")
            enabled_strings = ''.join(d_split[1:])
            enabled_line = enabled_line + enabled_strings

    i = 0
    line = enabled_line
    while i != -1:
        i = line.find("mul(")
        if (i > 0):
            subline = line[i+1:]
            j = subline.find(")")

            if (j > 0):
                try:
                    product = eval(line[i:(i+j+2)])
                    part2 += product
                except:
                    product = 0

                line = line[i+1:]

    return part1, part2

part1, part2 = part1_part2(input_file)

print("")
print("--- Advent of Code 2024 Day 3: Mull It Over ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
