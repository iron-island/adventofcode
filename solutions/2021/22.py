import math
from collections import defaultdict

input_file = "../../inputs/2021/input22.txt"
example_file = "example22.txt"
example2_file = "example22_2.txt"
example3_file = "example22_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example3 = 0
part1 = 0
part2 = 0

def get_regions(min_n, max_n, num_regions):
    diff_n = int(((max_n - min_n) + 1)/num_regions) + 1

    n_regions_list = []
    lower = min_n
    for i in range(0, num_regions):
        upper = lower + diff_n
        if (upper > max_n):
            upper = max_n
        n_regions_list.append((lower, upper))
        lower = upper + 1

    return n_regions_list

def get_bounds(axis):
    axis_min, axis_max = axis.split("=")[1].split("..")
    return (int(axis_min), int(axis_max))

def limit_bounds(n_tuple, lower, upper):
    n_min, n_max = n_tuple

    if (n_min < lower):
        n_min = lower
    if (n_max > upper):
        n_max = upper

    return (n_min, n_max)

def is_inside_bounds(n_tuple, n1, n2):
    n_min, n_max = n_tuple
    if ((n1 <= n_min <= n2) or (n1 <= n_max <= n2)):
        return True
    else:
        return False

def update_bounds(bounds_list, n):
    LEN = len(bounds_list)

    if (LEN == 0):
        return [n]

    MAX_IDX = LEN-1
    if (n not in bounds_list):
        bounds_list.append(n)
        bounds_list.sort()
    #idx_insertion = None
    #for idx, bounds in enumerate(bounds_list):
    #    if (idx == 0):
    #        if (n < bounds):
    #            idx_insertion = 0
    #            break
    #        elif (n > bounds):
    #            idx_insertion = -1
    #            break
    #    elif (idx < MAX_IDX):
    #        if (bounds < n) and (n < bounds_list[idx+1]):
    #            idx_insertion = idx+1
    #            break
    #    elif (idx == MAX_IDX):
    #        if (bounds < n):
    #            idx_insertion = -1
    #            break

    #if (idx_insertion == None):
    #    # No update to bounds needed
    #    return bounds_list
    #elif (idx_insertion == -1):
    #    bounds_list.append(n)
    #else:
    #    bounds_list.insert(idx_insertion, n)

    return bounds_list

def expand_bounds(bounds_list, n_tuple):
    n_min, n_max = n_tuple

    idx_min = bounds_list.index(n_min)
    idx_max = bounds_list.index(n_max)

    subbounds_list = bounds_list[idx_min:idx_max+1]

    subbounds_set = set()
    MAX_IDX = len(subbounds_list)-1
    for idx, subbound in enumerate(subbounds_list):
        # Add boundary first
        subbounds_set.add((subbound, subbound))

        if (0 < idx):
            prev_subbound = subbounds_list[idx-1]
            if (subbound - prev_subbound) > 1:
                subbounds_set.add((prev_subbound+1, subbound-1))

        if (idx < MAX_IDX):
            next_subbound = subbounds_list[idx+1]
            if (next_subbound - subbound) > 1:
                subbounds_set.add((subbound+1, next_subbound-1))

    #if (len(subbounds_set) == 0):
    #    print(n_min, n_max)
    #    print(idx_min, idx_max)

    return subbounds_set

def process_inputs(in_file):
    output = 0

    reboot_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            state, coords = line.split(" ")
            x, y, z = coords.split(",")
            x_tuple = get_bounds(x)
            y_tuple = get_bounds(y)
            z_tuple = get_bounds(z)

            reboot_list.append((state, x_tuple, y_tuple, z_tuple))

            line = file.readline()

    # Reboot
    cubes_dict = defaultdict(str)
    for step in reboot_list:
        state, x_tuple, y_tuple, z_tuple = step

        x_min, x_max = limit_bounds(x_tuple, -50, 50)
        y_min, y_max = limit_bounds(y_tuple, -50, 50)
        z_min, z_max = limit_bounds(z_tuple, -50, 50)

        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                for z in range(z_min, z_max+1):
                    coords = (x, y, z)
                    cubes_dict[(coords)] = state

    # Evaluate
    for cube in cubes_dict:
        state = cubes_dict[cube]

        if (state == "on"):
            output += 1

    return output

def process_inputs2(in_file):
    output = 0

    reboot_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            state, coords = line.split(" ")
            x, y, z = coords.split(",")
            x_tuple = get_bounds(x)
            y_tuple = get_bounds(y)
            z_tuple = get_bounds(z)

            reboot_list.append((state, x_tuple, y_tuple, z_tuple))

            line = file.readline()

    # Check pairs of steps and see if there are steps that have no overlap with any other step
    #independent_steps_list = []
    #for idx1, step in enumerate(reboot_list):
    #    overlaps = 0
    #    for idx2, step in enumerate(reboot_list):
    #        state1, x1, y1, z1 = reboot_list[idx1]
    #        state2, x2, y2, z2 = reboot_list[idx2]

    #        x1_min, x1_max = x1
    #        x2_min, x2_max = x2
    #        y1_min, y1_max = y1
    #        y2_min, y2_max = y2
    #        z1_min, z1_max = z1
    #        z2_min, z2_max = z2

    #        if (is_inside_bounds(x1, x2_min, x2_max)) and \
    #           (is_inside_bounds(y1, y2_min, y2_max)) and \
    #           (is_inside_bounds(z1, z2_min, z2_max)):
    #            overlaps += 1

    #    if (overlaps < 10):
    #        independent_steps_list.append(idx1)

    #print(len(independent_steps_list))
    #print(independent_steps_list)
    #return 0
    #independent_steps_list = []

    # Precompute independent steps
    #output = 0
    #for idx in independent_steps_list:
    #    state, x, y, z = reboot_list[idx]

    #    if (state == "off"):
    #        continue

    #    x_min, x_max = x
    #    y_min, y_max = y
    #    z_min, z_max = z

    #    x_side = (x_max - x_min) + 1
    #    y_side = (y_max - y_min) + 1
    #    z_side = (z_max - z_min) + 1

    #    output += x_side*y_side*z_side
    #return output

    # Find minimum and maximum boundaries
    MIN_X = math.inf
    MIN_Y = math.inf
    MIN_Z = math.inf
    MAX_X = -math.inf
    MAX_Y = -math.inf
    MAX_Z = -math.inf
    for idx, step in enumerate(reboot_list):
        state, x, y, z = step

        x_min, x_max = x
        y_min, y_max = y
        z_min, z_max = z

        MIN_X = min(MIN_X, x_min)
        MIN_Y = min(MIN_Y, y_min)
        MIN_Z = min(MIN_Z, z_min)

        MAX_X = max(MAX_X, x_max)
        MAX_Y = max(MAX_Y, y_max)
        MAX_Z = max(MAX_Z, z_max)

    print(MIN_X, MAX_X)
    print(MIN_Y, MAX_Y)
    print(MIN_Z, MAX_Z)

    # Divide the space into regions so we compute smaller regions first
    x_regions_list = []
    y_regions_list = []
    z_regions_list = []
    #x_regions_list.append((MIN_X, MAX_X))
    #y_regions_list.append((MIN_Y, MAX_Y))
    #z_regions_list.append((MIN_Z, MAX_Z))
    NUM_REGIONS = 10
    x_regions_list = get_regions(MIN_X, MAX_X, NUM_REGIONS)
    y_regions_list = get_regions(MIN_Y, MAX_Y, NUM_REGIONS)
    z_regions_list = get_regions(MIN_Z, MAX_Z, NUM_REGIONS)

    regions_list = []
    for x_lim in x_regions_list:
        for y_lim in y_regions_list:
            for z_lim in z_regions_list:
                regions_list.append((x_lim, y_lim, z_lim))

    for idx_region, region in enumerate(regions_list):
        x_lim, y_lim, z_lim = region
        lower_x, upper_x = x_lim
        lower_y, upper_y = y_lim
        lower_z, upper_z = z_lim

        # Find all possible bounds
        x_bounds_list = []
        y_bounds_list = []
        z_bounds_list = []
        for idx, step in enumerate(reboot_list):
            state, x_tuple, y_tuple, z_tuple = step

            x_min, x_max = limit_bounds(x_tuple, lower_x, upper_x)
            y_min, y_max = limit_bounds(y_tuple, lower_y, upper_y)
            z_min, z_max = limit_bounds(z_tuple, lower_z, upper_z)

            #x_bounds_list = update_bounds(x_bounds_list, x_min-1)
            x_bounds_list = update_bounds(x_bounds_list, x_min)
            x_bounds_list = update_bounds(x_bounds_list, x_max)
            #x_bounds_list = update_bounds(x_bounds_list, x_max+1)
            #y_bounds_list = update_bounds(y_bounds_list, y_min-1)
            y_bounds_list = update_bounds(y_bounds_list, y_min)
            y_bounds_list = update_bounds(y_bounds_list, y_max)
            #y_bounds_list = update_bounds(y_bounds_list, y_max+1)
            #z_bounds_list = update_bounds(z_bounds_list, z_min-1)
            z_bounds_list = update_bounds(z_bounds_list, z_min)
            z_bounds_list = update_bounds(z_bounds_list, z_max)
            #z_bounds_list = update_bounds(z_bounds_list, z_max+1)

        #print(len(x_bounds_list))
        #print(len(y_bounds_list))
        #print(len(z_bounds_list))

        # Reboot
        cubes_set = set()
        if (idx_region % NUM_REGIONS*10) == 0:
            print(f'Trying region {idx_region+1} of {len(regions_list)}')
        for idx, step in enumerate(reboot_list):
            #print(f'Trying region {idx_region+1} of {len(regions_list)}, step {idx+1} of {len(reboot_list)}')
            #print(len(cubes_set))

            state, x_tuple, y_tuple, z_tuple = step

            x_tuple = limit_bounds(x_tuple, lower_x, upper_x)
            y_tuple = limit_bounds(y_tuple, lower_y, upper_y)
            z_tuple = limit_bounds(z_tuple, lower_z, upper_z)

            #assert(x_min in x_bounds_list)
            #assert(y_min in y_bounds_list)
            #assert(z_min in z_bounds_list)
            #assert(x_max in x_bounds_list)
            #assert(y_max in y_bounds_list)
            #assert(z_max in z_bounds_list)

            # Expand the boundaries based on *_bounds_list
            x_subbounds_set = expand_bounds(x_bounds_list, x_tuple)
            y_subbounds_set = expand_bounds(y_bounds_list, y_tuple)
            z_subbounds_set = expand_bounds(z_bounds_list, z_tuple)
            #print(len(x_subbounds_set))
            #print(len(y_subbounds_set))
            #print(len(z_subbounds_set))
            for x in x_subbounds_set:
                for y in y_subbounds_set:
                    for z in z_subbounds_set:
                        #if (x, y, z) in cubes_dict:
                        #    print("Already exists")

                        coords = (x, y, z)
                        if (state == "on"):
                            #cubes_dict[(x, y, z)] = state
                            cubes_set.add(coords)
                        elif (state == "off") and (coords in cubes_set):
                            #del cubes_dict[(x, y, z)]
                            cubes_set.remove(coords)

        # Evaluate
        for xyz in cubes_set:
            #state = cubes_dict[xyz]

            #if (state == "on"):
            if (True):
                x, y, z = xyz
                x_min, x_max = x
                y_min, y_max = y
                z_min, z_max = z

                x_side = (x_max - x_min) + 1
                y_side = (y_max - y_min) + 1
                z_side = (z_max - z_min) + 1

                output += x_side*y_side*z_side

    return output

#part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file)
#part1 = process_inputs(input_file)

#part2_example3 = process_inputs2(example3_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
#print(f'Part 2 example: {part2_example}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
