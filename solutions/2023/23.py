import sys
import functools
from copy import deepcopy

sys.setrecursionlimit(50000)

input_file = "../../inputs/2023/input23.txt"
example_file = "example23.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
global_grid = []

def get_edges(v, vertices, finish):
    queue = []
    visited = []
    queue.append([v, 0])
    edges_dict = {}

    while len(queue):
        coord, steps = queue.pop(0)
        r, c = coord

        if coord in visited:
            continue

        CAN_UP = (r > 0) and (global_grid[r-1][c] != '#') and ((r-1, c) not in visited)
        CAN_DOWN = (global_grid[r+1][c] != '#') and ((r+1, c) not in visited)
        CAN_LEFT = (global_grid[r][c-1] != '#') and ((r, c-1) not in visited)
        CAN_RIGHT = (global_grid[r][c+1] != '#') and ((r, c+1) not in visited)

        #if (coord in vertices) and (coord not in [(0, 1), finish]) and (coord != v):
        if (coord in vertices) and (coord != v):
            edges_dict[coord] = steps
            continue

        next_steps = steps + 1
        if CAN_UP:
            queue.append([(r-1, c), next_steps])
        if CAN_DOWN:
            queue.append([(r+1, c), next_steps])
        if CAN_LEFT:
            queue.append([(r, c-1), next_steps])
        if CAN_RIGHT:
            queue.append([(r, c+1), next_steps])

        visited.append(coord)

    return edges_dict

#@functools.cache
def simpler_dfs(coord, visited, finish, graph, steps):

    if (coord == finish):
        return steps

    valid_neighbors = 0
    returned_steps = 0
    next_visited = visited + [coord]
    for next_coord in graph[coord]:
        next_steps = graph[coord][next_coord]

        if next_coord not in visited:
            returned_steps = max(returned_steps, simpler_dfs(next_coord, next_visited, finish, graph, next_steps))
            valid_neighbors += 1

    if (valid_neighbors == 0):
        return 0
    else:
        if (returned_steps):
            return steps + returned_steps
        else:
            return 0

mycache = {}
@functools.cache
def dfs(grid, coord, visited, finish):
    grid = list(grid)
    #mykey = coord
    #if mykey in mycache:
    #    return mycache[mykey]

    r, c = coord

    if coord == finish:
        #return steps
        return 1

    CAN_UP = (r > 0) and (grid[r-1][c] != '#') and ((r-1, c) not in visited)
    CAN_DOWN = (grid[r+1][c] != '#') and ((r+1, c) not in visited)
    CAN_LEFT = (grid[r][c-1] != '#') and ((r, c-1) not in visited)
    CAN_RIGHT = (grid[r][c+1] != '#') and ((r, c+1) not in visited)

    curr_step = 0
    up_step = 0
    down_step = 0
    left_step = 0
    right_step = 0
    next_visited = tuple(list(visited) + [coord])
    grid = tuple(grid)
    if CAN_UP:
        #max_steps = max(max_steps, dfs(grid, (r-1, c), visited, finish, steps+1))
        up_step = dfs(grid, (r-1, c), next_visited, finish)
    if CAN_DOWN:
        #max_steps = max(max_steps, dfs(grid, (r+1, c), visited, finish, steps))
        down_step = dfs(grid, (r+1, c), next_visited, finish)
    if CAN_LEFT:
        left_step = dfs(grid, (r, c-1), next_visited, finish)
    if CAN_RIGHT:
        #max_steps = max(max_steps, dfs(grid, (r, c+1), visited, finish, steps))
        right_step = dfs(grid, (r, c+1), next_visited, finish)

    max_step = max(up_step, down_step, left_step, right_step)

    if not (CAN_UP or CAN_DOWN or CAN_LEFT or CAN_RIGHT):
        #if mykey in mycache:
        #    mycache[mykey] = max(mycache[mykey], 0)
        #else:
        #    mycache[mykey] = 0
        return 0
    elif max_step:
        #if mykey in mycache:
        #    mycache[mykey] = max(mycache[mykey], max_step + 1)
        #else:
        #    mycache[mykey] = max_step + 1
        return max_step + 1
    else:
        #if mykey in mycache:
        #    mycache[mykey] = max(mycache[mykey], 0)
        #else:
        #    mycache[mykey] = 0
        return 0

def process_inputs(in_file):
    output = 0

    grid = []
    line_length = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_length = len(line)
            grid.append(line)

            line = file.readline()

    finish = (len(grid)-1, line_length-2)

    # Add extra '#' line at end of grid
    grid.append('#'*line_length)

    # Represent as graph to shorted BFS later on
    # DFS
    queue = []
    visited = []

    # format: (current coordinates), (start of path), steps
    queue.append([(0, 1), (0, 1), 0])
    paths_list = []
    forks = set()
    max_steps = 0
    while len(queue):
        q = queue.pop(0)
        coord, start, steps = q
        r, c = coord

        if [coord, start] in visited:
            continue

        if coord == finish:
            max_steps = max(max_steps, steps)
            continue

        curr_tile = grid[r][c]

        next_steps = steps+1
        if (curr_tile == 'v'):
            queue.insert(0, [(r+1, c), start, next_steps])
            visited.append([coord, start])
            continue
        elif (curr_tile == '^'):
            queue.insert(0, [(r-1, c), start, next_steps])
            visited.append([coord, start])
            continue
        elif (curr_tile == '>'):
            queue.insert(0, [(r, c+1), start, next_steps])
            visited.append([coord, start])
            continue
        elif (curr_tile == '<'):
            queue.insert(0, [(r, c-1), start, next_steps])
            visited.append([coord, start])
            continue

        CAN_UP = (grid[r-1][c] != '#') and (grid[r-1][c] != 'v') and ([(r-1, c), start] not in visited)
        CAN_DOWN = (grid[r+1][c] != '#') and (grid[r+1][c] != '^') and ([(r+1, c), start] not in visited)
        CAN_LEFT = (grid[r][c-1] != '#') and (grid[r][c-1] != '>') and ([(r, c-1), start] not in visited)
        CAN_RIGHT = (grid[r][c+1] != '#') and (grid[r][c+1] != '<') and ([(r, c+1), start] not in visited)

        # Create a branch if can traverse multiple paths
        #if ([CAN_UP, CAN_DOWN, CAN_LEFT, CAN_RIGHT].count(True) > 1):
        if ([CAN_UP, CAN_DOWN, CAN_LEFT, CAN_RIGHT].count(True) > 1) or ((r, c) == finish):
            paths_list.append([(r, c), start, next_steps])
            start = (r, c)
            forks.add((r, c))

        if CAN_UP:
            queue.insert(0, [(r-1, c), start, next_steps])
        if CAN_DOWN:
            queue.insert(0, [(r+1, c), start, next_steps])
        if CAN_LEFT:
            queue.insert(0, [(r, c-1), start, next_steps])
        if CAN_RIGHT:
            queue.insert(0, [(r, c+1), start, next_steps])

        visited.append([coord, start])

    print(f'{len(forks)} Forking tiles are: {forks}')
    print(f'{len(paths_list)} Paths are: {paths_list}')

    output = max_steps

    return output

def process_inputs2(in_file):
    global global_grid
    output = 0

    grid = []
    line_length = 0
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            line_length = len(line)
            grid.append(line)

            line = file.readline()

    finish = (len(grid)-1, line_length-2)

    # Add extra '#' line at end of grid
    grid.append('#'*line_length)

    global_grid = deepcopy(grid)

    # Condense graph via BFS
    queue = []
    visited = []
    queue.append((0, 1))
    vertices = []

    while len(queue):
        coord = queue.pop(0)
        r, c = coord

        if (coord in visited):
            continue

        CAN_UP = (r > 0) and (grid[r-1][c] != '#')
        CAN_DOWN = (grid[r+1][c] != '#')
        CAN_LEFT = (grid[r][c-1] != '#')
        CAN_RIGHT = (grid[r][c+1] != '#')

        # Forks are considered vertices
        if ([CAN_UP, CAN_DOWN, CAN_LEFT, CAN_RIGHT].count(True) > 2):
            vertices.append(coord)

        if CAN_UP and ((r-1, c) not in visited):
            queue.append((r-1, c))
        if CAN_DOWN and ((r+1, c) not in visited):
            queue.append((r+1, c))
        if CAN_LEFT and ((r, c-1) not in visited):
            queue.append((r, c-1))
        if CAN_RIGHT and ((r, c+1) not in visited):
            queue.append((r, c+1))

        visited.append(coord)

    # Add start and ending node to vertices
    vertices.insert(0, (0, 1))
    vertices.append(finish)

    print(f'{len(vertices)} Vertices: {vertices}')
    # BFS again to get edges
    graph = {}
    for v in vertices:
        edges_dict = get_edges(v, vertices, finish)

        graph[v] = edges_dict

    for v in graph:
        print(f'Vertex {v} has edges {graph[v]}')

    '''

    queue.append([(0, 1), 0])
    forks = []
    max_steps = 0
    while (len(forks) or (max_steps == 0)):
        #print(f'Queu: {queue}, forks: {forks}, visited: {visited}')
        #if len(queue) == 0:
        #    # Encountered deadend, so backtrack?
        #    print(f'Found deadend, backtracking, forks = {forks}, queue = {queue}')
        #    while (forks[-1] != visited[-1]):
        #        v_popped = visited.pop(-1)
        #    forks.pop(-1)

        #    continue
        coord, steps = queue.pop(0)
        r, c = coord

        if coord == finish:
            max_steps = max(max_steps, steps)

            # Backtrack
            #print(f'Found finish, backtracking, forks = {forks}')
            while (forks[-1] != visited[-1]):
                v_popped = visited.pop(-1)
            forks.pop(-1)

            continue

        next_steps = steps+1

        CAN_UP = (grid[r-1][c] != '#') and ((r-1, c) not in visited)
        CAN_DOWN = (grid[r+1][c] != '#') and ((r+1, c) not in visited)
        CAN_LEFT = (grid[r][c-1] != '#') and ((r, c-1) not in visited)
        CAN_RIGHT = (grid[r][c+1] != '#') and ((r, c+1) not in visited)

        # Create a branch if can traverse multiple paths
        if ([CAN_UP, CAN_DOWN, CAN_LEFT, CAN_RIGHT].count(True) > 1):
        #if ([CAN_UP, CAN_DOWN, CAN_LEFT, CAN_RIGHT].count(True) > 1) or ((r, c) == finish):
            forks.append((r, c))
        elif ([CAN_UP, CAN_DOWN, CAN_LEFT, CAN_RIGHT].count(False) == 4):
            # Backtrack
            #print(f'Found deadend, backtracking, forks = {forks}')
            while (forks[-1] != visited[-1]):
                v_popped = visited.pop(-1)
            forks.pop(-1)

            continue

        if CAN_UP:
            queue.insert(0, [(r-1, c), next_steps])
        if CAN_DOWN:
            queue.insert(0, [(r+1, c), next_steps])
        if CAN_LEFT:
            queue.insert(0, [(r, c-1), next_steps])
        if CAN_RIGHT:
            queue.insert(0, [(r, c+1), next_steps])

        visited.append(coord)

    print(f'Last stop: {coord}')
    '''

    #output = dfs(tuple(grid), (0, 1), tuple(visited), finish)
    #output = dfs(grid, finish, visited, (0, 1))

    visited = []
    output = simpler_dfs((0, 1), visited, finish, graph, 0)

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
mycache = {}
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
