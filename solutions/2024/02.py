input_file = "input2.txt"
example_file = "example2.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    safe_reports = []
    num = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            report = line.split()

            orig_rep = [r for r in report]

            safe = True
            if (int(orig_rep[0]) == int(orig_rep[1])):
                safe = False
            elif (int(orig_rep[0]) > int(orig_rep[1])):
                higher = False
            else:
                higher = True

            if (safe):
                for idx, r in enumerate(orig_rep):
                    if (idx):
                        if (higher) and (int(r) > (int(orig_rep[idx-1]))):
                            diff = abs(int(r) - int(orig_rep[idx-1]))
                        elif (not higher) and (int(r) < (int(orig_rep[idx-1]))):
                            diff = abs(int(r) - int(orig_rep[idx-1]))
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
                num += 1

            line = file.readline()

    output = len(safe_reports)
    output = num
    return output

def process_inputs2(in_file):
    output = 0

    safe_reports = []
    num = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            report = line.split()

            orig_rep = [r for r in report]

            safe = True
            if (int(orig_rep[0]) == int(orig_rep[1])):
                safe = False
            elif (int(orig_rep[0]) > int(orig_rep[1])):
                higher = False
            else:
                higher = True

            if (safe):
                for idx, r in enumerate(orig_rep):
                    if (idx):
                        if (higher) and (int(r) > (int(orig_rep[idx-1]))):
                            diff = abs(int(r) - int(orig_rep[idx-1]))
                        elif (not higher) and (int(r) < (int(orig_rep[idx-1]))):
                            diff = abs(int(r) - int(orig_rep[idx-1]))
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
                num += 1
            else:
                for idx2, level in enumerate(report):
                    orig_rep = [r for r in report]    
                    orig_rep.pop(idx2)

                    safe = True
                    if (int(orig_rep[0]) == int(orig_rep[1])):
                        safe = False
                    elif (int(orig_rep[0]) > int(orig_rep[1])):
                        higher = False
                    else:
                        higher = True

                    if (safe):
                        for idx, r in enumerate(orig_rep):
                            if (idx):
                                if (higher) and (int(r) > (int(orig_rep[idx-1]))):
                                    diff = abs(int(r) - int(orig_rep[idx-1]))
                                elif (not higher) and (int(r) < (int(orig_rep[idx-1]))):
                                    diff = abs(int(r) - int(orig_rep[idx-1]))
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
                        num += 1
                        break

            line = file.readline()

    output = len(safe_reports)
    output = num
    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
