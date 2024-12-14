input_file = "input19.txt"
example_file = "example19.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
LETTER_DICT = {'x': 0, 'm': 1, 'a': 2, 's': 3}

def check_flow(workflow, rating):
    next_flow = None

    for flow in workflow:
        if (":" in flow):
            rule, if_true = flow.split(":")
    
            letter = rule[0]
            inequality = rule[1]
            val = int(rule[2:])
    
            r_val = rating[LETTER_DICT[letter]]
    
            # Process rule
            if (inequality == '<'):
                if (r_val < val):
                    next_flow = if_true
                    break
                else:
                    continue
            else:
                if (r_val > val):
                    next_flow = if_true
                    break
                else:
                    continue
        else:
            next_flow = flow

    return next_flow

def count_combo(rating_bounds):
    count = 0
    combo = 1

    for bounds in rating_bounds:
        min_val, max_val = bounds
        count = max_val - min_val - 1

        combo = combo*count

    return combo

def recursive_flow(wf_dict, rules, rating_bounds):
    combo = 0

    for r in rules:
        if ":" in r:
            rule, if_true = r.split(":")

            letter = rule[0]
            inequality = rule[1]
            val = int(rule[2:])

            idx = LETTER_DICT[letter]
            r_bounds = rating_bounds[idx]
            min_bounds, max_bounds = r_bounds
            #assert(min_bounds < max_bounds)

            # Process rule
            if (inequality == "<"):
                if (max_bounds <= val): 
                    # Bounds stay the same, move to next workflow
                    if (if_true not in ['A', 'R']):
                        combo = combo + recursive_flow(wf_dict, wf_dict[if_true], rating_bounds)
                    elif (if_true == 'A'):
                        combo = combo + count_combo(rating_bounds)
                    break
                else:
                    # Split the bounds
                    if_true_bounds = list(rating_bounds)
                    if_true_bounds[idx] = (min_bounds, val)

                    if_false_bounds = list(rating_bounds)
                    if_false_bounds[idx] = (val-1, max_bounds)
                    rating_bounds = tuple(if_false_bounds)

                    # Move the split bounds to next workflow
                    if (if_true not in ['A', 'R']):
                        combo = combo + recursive_flow(wf_dict, wf_dict[if_true], tuple(if_true_bounds))
                    elif (if_true == 'A'):
                        combo = combo + count_combo(if_true_bounds)
                    continue
            else: # inequality is ">"
                if (min_bounds >= val):
                    # Bounds stay the same, move to next workflow
                    if (if_true not in ['A', 'R']):
                        combo = combo + recursive_flow(wf_dict, wf_dict[if_true], rating_bounds)
                    elif (if_true == 'A'):
                        combo = combo + count_combo(rating_bounds)
                    break
                else:
                    # Split the bounds
                    if_true_bounds = list(rating_bounds)
                    if_true_bounds[idx] = (val, max_bounds)

                    if_false_bounds = list(rating_bounds)
                    if_false_bounds[idx] = (min_bounds, val+1)
                    rating_bounds = tuple(if_false_bounds)

                    # Move the split bounds to next workflow
                    if (if_true not in ['A', 'R']):
                        combo = combo + recursive_flow(wf_dict, wf_dict[if_true], tuple(if_true_bounds))
                    elif (if_true == 'A'):
                        combo = combo + count_combo(if_true_bounds)
                    continue
        elif (r == 'A'):
            combo = combo + count_combo(rating_bounds)
            break
        elif (r != 'R'):
            combo = combo + recursive_flow(wf_dict, wf_dict[r], rating_bounds)
            break
        else: # rejected
            break

    return combo

def process_inputs(in_file):
    output = 0

    wf_dict = {}
    ratings = []
    with open(in_file) as file:
        line = file.readline()
   
        get_ratings = False 
        while line:
            line = line.strip()

            if (line == ""):
                get_ratings = True
                line = file.readline()
                continue

            line = line[:-1]
            if get_ratings:
                x, m, a, s = line[1:].split(",")
                xmas = (int(x[2:]), int(m[2:]), int(a[2:]), int(s[2:]))
                ratings.append(xmas)
            else:
                rule, conds = line.split("{")
                wf_dict[rule] = conds.split(",")

            line = file.readline()

    accepted = set()
    rejected = set()
    for idx, r in enumerate(ratings):
        next_flow = check_flow(wf_dict["in"], r)

        while (next_flow not in ['A', 'R']):
            next_flow = check_flow(wf_dict[next_flow], r)

        if (next_flow == 'A'):
            accepted.add(idx)
        else:
            rejected.add(idx)

    for idx in accepted:
        output += sum(ratings[idx])

    return output

def process_inputs2(in_file):
    output = 0

    wf_dict = {}
    ratings = []
    with open(in_file) as file:
        line = file.readline()
   
        get_ratings = False 
        while line:
            line = line.strip()

            if (line == ""):
                get_ratings = True
                line = file.readline()
                continue

            line = line[:-1]
            if get_ratings:
                x, m, a, s = line[1:].split(",")
                xmas = (int(x[2:]), int(m[2:]), int(a[2:]), int(s[2:]))
                ratings.append(xmas)
            else:
                rule, conds = line.split("{")
                wf_dict[rule] = conds.split(",")

            line = file.readline()

    # Construct graph of workflow
    #graph = {}
    #for wf in wf_dict:
    #    adjacent_flows = set()
    #    for rule in wf_dict[wf]:
    #        if (":" in rule):
    #            _, flow = rule.split(":")
    #            adjacent_flows.add(flow)
    #        else:
    #            adjacent_flows.add(rule)

    #    graph[wf] = adjacent_flows

    # Recursive workflow using only bounds
    bounds = (0, 4001)
    rating_bounds = (bounds, bounds, bounds, bounds)
    output = recursive_flow(wf_dict, wf_dict["in"], rating_bounds)

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file) # expected answer is 167409079868000
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}, error from expected = {167409079868000 - part2_example}')
print(f'Part 2: {part2}')
