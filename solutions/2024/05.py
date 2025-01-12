import itertools

input_file = "../../inputs/2024/input05.txt"
example_file = "example05.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

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

            #if (x == "97") and (y == "75") and (update == "75,97,47,61,53"):
            #    print(x_find) # 3
            #    print(y_find) # 0

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
        #print(valid_updates)
        pages = valid_updates.split(",")
        length = len(pages)
        middle_page = int(pages[int(length/2)])
        #print(middle_page)
        output += middle_page

    return output

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

def process_inputs2(in_file):
    output = 0

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
                #print(invalid_update)
                #print(valid)
                #print(x)
                #print(y)

            corrected_updates_list.append(invalid_update)

    # Correct (permutations)
    #for idx, invalid_update in enumerate(invalid_updates_list):
    #    print(f'idx {idx} of {len(invalid_updates_list)}')
    #    invalid_list = invalid_update.split(",")
    #    perms = itertools.permutations(invalid_list)
    #    print(f'Go through {len(list(perms))} permutations')
    #    for perm in perms:
    #        mylist = list(perm)
    #        mystring = ','.join(mylist)

    #        # Test for validity
    #        valid = True
    #        for rules in rules_list:
    #            x, y = rules

    #            y_find = mystring.find(y)
    #            x_find = mystring.find(x)

    #            if (y_find >= 0) and (x_find >= 0):
    #                if (y_find > x_find):
    #                    # valid
    #                    valid = True
    #                else:
    #                    valid = False
    #                    break

    #        if (valid):
    #            corrected_updates_list.append(mystring)
    #            break

    # Compute
    for corrected_updates in corrected_updates_list:
        #print(corrected_updates)
        pages = corrected_updates.split(",")
        length = len(pages)
        middle_page = int(pages[int(length/2)])
        #print(middle_page)
        output += middle_page

    return output

#part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 5: Print Queue ---")
#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
