from collections import defaultdict
from collections import deque
import math

input_file = "../../inputs/2021/input15.txt"
example_file = "example15.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def move_dir(rc, direction):
    row, col = rc

    assert(direction in ["up", "down", "left", "right"])
    if (direction == "up"):
        n_row = row-1
        n_col = col
    elif (direction == "down"):
        n_row = row+1
        n_col = col
    elif (direction == "left"):
        n_row = row
        n_col = col-1
    elif (direction == "right"):
        n_row = row
        n_col = col+1

    return (n_row, n_col)

def process_inputs(in_file):
    output = 0

    grid_dict = defaultdict(int)
    cost_dict = defaultdict(tuple)
    with open(in_file) as file:
        line = file.readline()
    
        row = 0
        MAX_ROW = 0
        MAX_COL = 0
        while line:
            line = line.strip()

            rowline = [int(x) for x in line]

            for col, risk in enumerate(rowline):
                rc = (row, col)
                grid_dict[rc] = risk
                if (rc == (0, 0)):
                    cost_dict[rc] = [risk, None]
                else:
                    cost_dict[rc] = (math.inf, None)

                MAX_ROW = max(row, MAX_ROW)
                MAX_COL = max(col, MAX_COL)

            row += 1
            line = file.readline()

    # DFS
    q = []
    visited = set()
    q.append((0, 0, 0))
    min_risk = math.inf
    while len(q):
        # Priority queue
        q.sort()
        cost, row, col = q.pop(0)
        rc = (row, col)

        if (rc == (MAX_ROW, MAX_COL)):
            min_risk = cost
            break

        if (rc in visited):
            continue
        visited.add(rc)

        # up
        n_tuple = move_dir(rc, "up")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))

        # down
        n_tuple = move_dir(rc, "down")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))

        # left
        n_tuple = move_dir(rc, "left")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))

        # right
        n_tuple = move_dir(rc, "right")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))
    output = min_risk

    return output

def process_inputs2(in_file):
    output = 0

    grid_dict = defaultdict(int)
    cost_dict = defaultdict(tuple)
    with open(in_file) as file:
        line = file.readline()
    
        row = 0
        MAX_ROW = 0
        MAX_COL = 0
        while line:
            line = line.strip()

            rowline = [int(x) for x in line]

            for col, risk in enumerate(rowline):
                rc = (row, col)
                grid_dict[rc] = risk
                if (rc == (0, 0)):
                    cost_dict[rc] = [risk, None]
                else:
                    cost_dict[rc] = (math.inf, None)

                MAX_ROW = max(row, MAX_ROW)
                MAX_COL = max(col, MAX_COL)

            row += 1
            line = file.readline()

    # Expand to the right first
    for i in range(1, 5):
        for row in range(0, MAX_ROW+1):
            for col in range(0, MAX_COL+1):
                risk = grid_dict[(row, col)]
                n_tuple = (row, col + i*(MAX_COL+1))

                n_risk = risk + i
                if (n_risk > 9):
                    n_risk = n_risk - 9
                grid_dict[n_tuple] = n_risk
                cost_dict[n_tuple] = (math.inf, None)

    # Expand down
    for i in range(1, 5):
        for row in range(0, MAX_ROW+1):
            for col in range(0, 5*(MAX_COL+1)):
                risk = grid_dict[(row, col)]
                n_tuple = (row + i*(MAX_ROW+1), col)

                n_risk = risk + i
                if (n_risk > 9):
                    n_risk = n_risk - 9
                grid_dict[n_tuple] = n_risk
                cost_dict[n_tuple] = (math.inf, None)

    # DFS
    q = []
    visited = set()
    q.append((0, 0, 0))
    min_risk = math.inf
    EXP_MAX_ROW = 5*(MAX_ROW+1) - 1
    EXP_MAX_COL = 5*(MAX_COL+1) - 1
    while len(q):
        # Priority queue
        q.sort()
        cost, row, col = q.pop(0)
        rc = (row, col)

        if (rc == (EXP_MAX_ROW, EXP_MAX_COL)):
            min_risk = cost
            break

        if (rc in visited):
            continue
        visited.add(rc)

        # up
        n_tuple = move_dir(rc, "up")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))

        # down
        n_tuple = move_dir(rc, "down")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))

        # left
        n_tuple = move_dir(rc, "left")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))

        # right
        n_tuple = move_dir(rc, "right")
        if (n_tuple in grid_dict):
            n_cost = cost + grid_dict[n_tuple]
            curr_cost, _ = cost_dict[n_tuple]

            if (n_cost < curr_cost):
                n_row, n_col = n_tuple
                cost_dict[n_tuple] = (n_cost, rc)
                q.append((n_cost, n_row, n_col))
    output = min_risk

    # Print grid
    #for row in range(0, EXP_MAX_ROW+1):
    #    for col in range(0, EXP_MAX_COL+1):
    #        print(grid_dict[(row, col)], end="")
    #    print("")

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
