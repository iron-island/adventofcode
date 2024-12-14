import math

input_file = "input18.txt"
example_file = "example18.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

VERTICAL = ['U', 'D']
HORIZONTAL = ['L', 'R']
hex2dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

def process_inputs(in_file, init_floodfill=(0, 0)):
    output = 0

    with open(in_file) as file:
        line = file.readline()

        plan_list = []
        while line:
            line = line.strip()

            direction, num, color = line.split()
            plan_list.append((direction, int(num), color))

            line = file.readline()

    trench_coords = set()
    trench_coords.add((0, 0))

    x = 0
    y = 0
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for p in plan_list:
        direction, num, color = p

        if (direction == 'U'):
            for i in range(y, y+num+1):
                trench_coords.add((x, i))
            y = y+num
        elif (direction == 'D'):
            for i in range(y, y-num-1, -1):
                trench_coords.add((x, i))
            y = y-num
        elif (direction == 'R'):
            for i in range(x, x+num+1):
                trench_coords.add((i, y))
            x = x+num
        elif (direction == 'L'):
            for i in range(x, x-num-1, -1):
                trench_coords.add((i, y))
            x = x-num

        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)

    print(f'Max: {max_x, max_y}')
    print(f'Min: {min_x, min_y}')

    output = len(trench_coords)

    # PIP
    output = 0
    for y in range(max_y, min_y-1, -1):
        row_num = 0
        last_was_edge = False
        for x in range(min_x, max_x+1):
            if (x, y) == (0, 0):
                print('S', end="")
            elif (x, y) in trench_coords:
                print('#', end="")
                output += 1
                if (not last_was_edge):
                    row_num += 1
                    last_was_edge = True
            else:
                last_was_edge = False
                if (row_num % 2 == 1):
                    print("x", end="")
                    output += 1
                else:
                    print(".", end="")
        print("")

    # BFS
    queue = set()
    visited = set()

    queue.add(init_floodfill)

    while len(queue):
        q = queue.pop()
        x, y = q

        if q in visited:
            continue

        if (x+1, y) not in trench_coords:
            queue.add((x+1, y))

        if (x-1, y) not in trench_coords:
            queue.add((x-1, y))

        if (x, y+1) not in trench_coords:
            queue.add((x, y+1))

        if (x, y-1) not in trench_coords:
            queue.add((x, y-1))

        visited.add(q)

    output = len(trench_coords) + len(visited)

    return output

def process_inputs2(in_file, init_floodfill=(0, 0)):
    output = 0

    with open(in_file) as file:
        line = file.readline()

        plan_list = []
        while line:
            line = line.strip()

            direction, num, color = line.split()
            plan_list.append((direction, int(num), color))

            line = file.readline()

    trench_coords = []
    trench_coords.append((0, 0))

    x = 0
    y = 0
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    edge_area = 0
    num_up = 0
    num_down = 0
    num_left = 0
    num_right = 0
    for p in plan_list:
        direction, num, color = p

        color = color[2:-1]
        direction = hex2dir[color[-1]]
        num = int(color[0:-1], 16)
        print(f'{direction} {num}, {color[0:-1]}')

        if (direction == 'U'):
            y = y+num
            num_up += 1
        elif (direction == 'D'):
            y = y-num
            num_down += 1
        elif (direction == 'R'):
            x = x+num
            num_right += 1
        elif (direction == 'L'):
            x = x-num
            num_left += 1
        trench_coords.append((x, y))
        last_dir = direction

        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)

        edge_area += num

    print(f'Max: {max_x, max_y}')
    print(f'Min: {min_x, min_y}')

    # shoelace formula
    output = 0

    max_idx = len(trench_coords)-1

    for i in range(0, max_idx):
        x, y = trench_coords[i]
        next_x, next_y = trench_coords[i+1]
        #output = output + (y + next_y)*(x - next_x)
        output = output + x*next_y - next_x*y
    x1, y1 = trench_coords[0]
    last_x, last_y = trench_coords[-1]
    #output = 0.5*(output + (last_y + y1)*(last_x - x1))
    output = 0.5*(output + last_x*y1 - x1*last_y)

    #output = abs(output) + (edge_area + abs(num_up - num_down) + abs(num_left - num_right))/2
    # Tried to find pattern, not sure yet how (edge_area + 2)/2 comes about
    output = abs(output) + (edge_area + 2)/2

    return output

#part1_example = process_inputs(example_file, (1, -1))
#part1 = process_inputs(input_file, (1, 0))

part2_example = process_inputs2(example_file, (1, -1))
part2 = process_inputs2(input_file, (1,0))

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
