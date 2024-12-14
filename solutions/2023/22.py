from copy import deepcopy

input_file = "input22.txt"
example_file = "example22.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    bricks = []
    z_buf = []
    z2idx_dict = {}
    idx = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            start, end = line.split("~")
            start_tuple = tuple([int(x) for x in start.split(",")])
            end_tuple   = tuple([int(x) for x in end.split(",")])
            bricks.append([start_tuple, end_tuple])

            z = min(start_tuple[2], end_tuple[2])
            if (z not in z2idx_dict):
                z2idx_dict[z] = idx
            else:
                while (z in z2idx_dict):
                    z = z + 0.01
                z2idx_dict[z] = idx
            z_buf.append(z)

            idx += 1
            line = file.readline()

    # Sort bricks first based on starting z
    idx_order = []
    for z in sorted(z_buf):
        idx_order.append(z2idx_dict[z])

    # Stack bricks
    # stack is dictionary of coordinates with brick indices as values
    stack = {}
    idx2coord_dict = {}
    for idx in idx_order:
        start, end = bricks[idx]
        x_s, y_s, z_s = start
        x_e, y_e, z_e = end

        brick_coord = set()
        for x in range(x_s, x_e+1):
            for y in range(y_s, y_e+1):
                for z in range(z_s, z_e+1):
                    brick_coord.add((x, y, z))

        # Check for collisions while dropping brick
        next_z = z_s-1
        no_collision = True
        while True:
            for c in brick_coord:
                x, y, z = c
                if (x, y, next_z) in stack:
                    no_collision = False
                    break

            if (no_collision) and (next_z > 0):
                next_z -= 1
            else:
                break

        # Stack the brick
        drop_z = z_s - next_z - 1
        idx2coord_dict[idx] = []
        for c in brick_coord:
            x, y, z = c
            stack[(x, y, z-drop_z)] = idx
            idx2coord_dict[idx].append((x, y, z-drop_z))

    # Disintegrate via BFS
    cannot_disintegrate = 0
    for idx in idx_order:
        supported_idx = set()
        for coord in idx2coord_dict[idx]:
            x, y, z = coord
            supported_coord = (x, y, z+1)
            if (supported_coord in stack) and (stack[supported_coord] != idx):
                supported_idx.add(stack[supported_coord])

        # If its not supporting anything, then it is safe to disintegrate
        if (len(supported_idx)):
            for idx_s in supported_idx:
                supporting_bricks = []
                for coord in idx2coord_dict[idx_s]:
                    x, y, z = coord
                    supporting_coord = (x, y, z-1)
                    if (supporting_coord in stack):
                        supporting_idx = stack[supporting_coord]
                        if (supporting_idx != idx) and (supporting_idx != idx_s):
                            supporting_bricks.append(supporting_idx)
                            break

                if (len(supporting_bricks) == 0):
                    cannot_disintegrate += 1
                    break
    output = len(bricks) - cannot_disintegrate

    return output

def process_inputs2(in_file):
    output = 0

    bricks = []
    z_buf = []
    z2idx_dict = {}
    idx = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            start, end = line.split("~")
            start_tuple = tuple([int(x) for x in start.split(",")])
            end_tuple   = tuple([int(x) for x in end.split(",")])
            bricks.append([start_tuple, end_tuple])

            z = min(start_tuple[2], end_tuple[2])
            if (z not in z2idx_dict):
                z2idx_dict[z] = idx
            else:
                while (z in z2idx_dict):
                    z = z + 0.01
                z2idx_dict[z] = idx
            z_buf.append(z)

            idx += 1
            line = file.readline()

    # Sort bricks first based on starting z
    idx_order = []
    for z in sorted(z_buf):
        idx_order.append(z2idx_dict[z])

    # Stack bricks
    # stack is dictionary of coordinates with brick indices as values
    stack = {}
    idx2coord_dict = {}
    for idx in idx_order:
        start, end = bricks[idx]
        x_s, y_s, z_s = start
        x_e, y_e, z_e = end

        brick_coord = set()
        for x in range(x_s, x_e+1):
            for y in range(y_s, y_e+1):
                for z in range(z_s, z_e+1):
                    brick_coord.add((x, y, z))

        # Check for collisions while dropping brick
        next_z = z_s-1
        no_collision = True
        while True:
            for c in brick_coord:
                x, y, z = c
                if (x, y, next_z) in stack:
                    no_collision = False
                    break

            if (no_collision) and (next_z > 0):
                next_z -= 1
            else:
                break

        # Stack the brick
        drop_z = z_s - next_z - 1
        idx2coord_dict[idx] = []
        for c in brick_coord:
            x, y, z = c
            stack[(x, y, z-drop_z)] = idx
            idx2coord_dict[idx].append((x, y, z-drop_z))

    # Disintegrate via BFS
    cannot_disintegrate = 0
    brick_disintegrate = []
    for idx in idx_order:
        supported_idx = set()
        for coord in idx2coord_dict[idx]:
            x, y, z = coord
            supported_coord = (x, y, z+1)
            if (supported_coord in stack) and (stack[supported_coord] != idx):
                supported_idx.add(stack[supported_coord])

        # If its not supporting anything, then it is safe to disintegrate
        if (len(supported_idx)):
            for idx_s in supported_idx:
                supporting_bricks = []
                for coord in idx2coord_dict[idx_s]:
                    x, y, z = coord
                    supporting_coord = (x, y, z-1)
                    if (supporting_coord in stack):
                        supporting_idx = stack[supporting_coord]
                        if (supporting_idx != idx) and (supporting_idx != idx_s):
                            supporting_bricks.append(supporting_idx)
                            break

                if (len(supporting_bricks) == 0):
                    cannot_disintegrate += 1
                    brick_disintegrate.append(idx)
                    break

    # Record minimum heights for each brick
    idx2minz_dict = {}
    for idx in idx2coord_dict:
        brick_coord = idx2coord_dict[idx]
        min_z = 1000000
        for c in brick_coord:
            x, y, z = c
            min_z = min(z, min_z)
        idx2minz_dict[idx] = min_z

    # Get what supports each brick
    idx2support_dict = {}
    support2idx_dict = {}
    for idx in idx_order:
        # Record what each brick is supported by
        support = set()
        brick_coords = idx2coord_dict[idx]
        for c in brick_coords:
            x, y, z = c
            down_coord = (x, y, z-1)
            if (down_coord in stack) and (stack[down_coord] != idx):
                support.add(stack[down_coord])

        idx2support_dict[idx] = support

        # Record what each brick is supporting
        support2idx_dict[idx] = set()
        for c in brick_coords:
            x, y, z = c
            up_coord = (x, y, z+1)
            if (up_coord in stack) and (stack[up_coord] != idx):
                support2idx_dict[idx].add(stack[up_coord])

    # Count falling bricks
    for idx in brick_disintegrate:
        i2s_copy = deepcopy(idx2support_dict)

        queue = set()
        visited = set()
        queue.add(idx)

        while len(queue):
            q = queue.pop()

            if q in visited:
                continue

            for i in support2idx_dict[q]:
                # Remove from list of supports, so that if list of supports is empty,
                #   the brick will fall
                i2s_copy[i].remove(q)
                if (len(i2s_copy[i]) == 0):
                    queue.add(i)

            visited.add(q)

        output += len(visited)-1

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file) # 113700 is too high, 5037 too low

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
