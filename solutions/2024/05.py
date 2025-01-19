from time import perf_counter, process_time

# Get start time using both perf_counter() for wall clock time
#   and process_time() for the time of only this process
t_s_perf = perf_counter()
t_s_proc = process_time()

input_file = "../../inputs/2024/input05.txt"

def part1(in_file):
    part1 = 0

    rules_list = []
    inv_rules_list = []
    state = 0
    updates_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if (state == 0) and (line != ""):
                x, y = line.split("|")
                rules_list.append([x, y])
            elif (state == 0) and (line == ""):
                state = 1
            elif (state == 1):
                updates_list.append(line)

            line = file.readline()

    # Process updates
    valid_updates_list = []
    for update in updates_list:
        valid = True
        for rules in rules_list:
            x, y = rules

            y_find = update.find(y)
            x_find = update.find(x)

            if (y_find >= 0) and (x_find >= 0):
                if (y_find > x_find):
                    # valid
                    valid = True
                else:
                    valid = False
                    break

        # Evaluate
        if (valid):
            valid_updates_list.append(update)

    for valid_updates in valid_updates_list:
        pages = valid_updates.split(",")
        length = len(pages)
        middle_page = int(pages[int(length/2)])
        part1 += middle_page

    return part1

def test_validity(rules_list, update):
    valid = True
    for rules in rules_list:
        x, y = rules
        
        y_find = update.find(y)
        x_find = update.find(x)
        
        if (y_find >= 0) and (x_find >= 0):
            if (y_find > x_find):
                # valid
                valid = True
            else:
                valid = False
                break

    return (valid, x, y)

def part2(in_file):
    part2 = 0

    rules_list = []
    inv_rules_list = []
    state = 0
    updates_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            if (state == 0) and (line != ""):
                x, y = line.split("|")
                rules_list.append([x, y])
            elif (state == 0) and (line == ""):
                state = 1
            elif (state == 1):
                updates_list.append(line)

            line = file.readline()

    # Process updates
    valid_updates_list = []
    invalid_updates_list = []
    corrected_updates_list = []
    x = 0
    y = 0
    for update in updates_list:
        valid = True
        for rules in rules_list:
            x, y = rules

            y_find = update.find(y)
            x_find = update.find(x)

            if (y_find >= 0) and (x_find >= 0):
                if (y_find > x_find):
                    # valid
                    valid = True
                else:
                    valid = False
                    break

        # Evaluate
        if (valid):
            valid_updates_list.append(update)
        else:
            invalid_update = update

            valid = False
            while (not valid):
                # Correct
                y_find = invalid_update.find(y)
                x_find = invalid_update.find(x)
                invalid_update = invalid_update.replace(x, "yy")
                invalid_update = invalid_update.replace(y, x)
                invalid_update = invalid_update.replace("yy", y)

                valid, x, y = test_validity(rules_list, invalid_update)

            corrected_updates_list.append(invalid_update)

    # Compute
    for corrected_updates in corrected_updates_list:
        pages = corrected_updates.split(",")
        length = len(pages)
        middle_page = int(pages[int(length/2)])
        part2 += middle_page

    return part2

part1 = part1(input_file)
part2 = part2(input_file)

print("")
print("--- Advent of Code 2024 Day 5: Print Queue ---")
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# End timers
t_e_perf = perf_counter()
t_e_proc = process_time()

print("")
print(f'perf_counter (seconds): {t_e_perf - t_s_perf}')
print(f'process_time (seconds): {t_e_proc - t_s_proc}')
print("")
