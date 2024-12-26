from collections import defaultdict
from collections import deque
from functools import cache
import copy

input_file = "../../inputs/2021/input12.txt"
example_file = "example12.txt"
example2_file = "example12_2.txt"
example3_file = "example12_3.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part2_example = 0
part2_example2 = 0
part2_example3 = 0
part1 = 0
part2 = 0

caves_dict = defaultdict(list)
new_caves_dict = defaultdict(list)
paths_set = set()

# Memoization not required since its fast enough
#@cache
def dfs_caves(cave, visited):
    # Base case
    if (cave == "end"):
        return 1

    if (cave.islower()):
        visited = set(visited)
        visited.add(cave)

    # Recursive calls
    num_paths = 0
    for next_cave in caves_dict[cave]:
        if (next_cave in visited):
            continue

        num_paths += dfs_caves(next_cave, frozenset(visited))

    return num_paths

paths_set = set()
def dfs_caves2(cave, visited):
    global paths_set

    # Base case
    if (cave == "end"):
        visited = list(visited)
        visited.append(cave)

        # String of visited caves would show unique paths so remove the 1 and 2 suffixes
        #   for the duplicated small cave
        visited_str = ','.join(visited)
        visited_str = visited_str.replace("1", "")
        visited_str = visited_str.replace("2", "")
        paths_set.add(visited_str)
        return 1

    visited = list(visited)
    visited.append(cave)

    # Recursive calls
    num_paths = 0
    for next_cave in new_caves_dict[cave]:
        if (next_cave == "start"):
            continue

        if (next_cave in visited) and (next_cave.islower()):
            #if (cave_twice[0] == next_cave) and (cave_twice[1] == False):
            #    cave_twice = (next_cave, True)
            #else:
            continue

        num_paths += dfs_caves2(next_cave, tuple(visited))

    return num_paths

def process_inputs(in_file):
    global caves_dict
    caves_dict = defaultdict(list)

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            a, b = line.split("-")
            caves_dict[a].append(b)
            caves_dict[b].append(a)

            line = file.readline()

    visited = frozenset()
    output = dfs_caves("start", visited)
    #dfs_caves.cache_clear()

    return output

def process_inputs2(in_file):
    global caves_dict
    global new_caves_dict
    global paths_set
    caves_dict = defaultdict(list)

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            a, b = line.split("-")
            caves_dict[a].append(b)
            caves_dict[b].append(a)

            line = file.readline()

    # BFS
    #q = deque()
    #q.append(("start", [], False))
    #output = 0
    #while len(q):
    #    cave, visited, twice = q.popleft()

    #    if (cave == "end"):
    #        output += 1
    #        visited.append(cave)
    #        print(visited)
    #        continue

    #    is_small = cave.islower()
    #    if (cave != "start") and (is_small) and (cave in visited):
    #        if (twice):
    #            continue
    #        else:
    #            twice = True
    #    visited.append(cave)

    #    for adj_cave in caves_dict[cave]:
    #        if (adj_cave != "start"):
    #            q.append((adj_cave, visited, twice))
            
    # Find a small cave and duplicate it
    visited = frozenset()
    paths_set = set()
    for cave in caves_dict:
        if (cave.islower()) and (cave not in ["start", "end"]):
            new_caves_dict = copy.deepcopy(caves_dict)
            adj_caves_list = new_caves_dict[cave]
            new_caves_dict[cave + "1"] = adj_caves_list
            new_caves_dict[cave + "2"] = adj_caves_list

            # Go through adjacent caves and update their connections
            idx_old_cave = 0
            for adj_cave in adj_caves_list:
                old_caves_list = new_caves_dict[adj_cave]
                for idx, old_cave in enumerate(old_caves_list):
                    if (old_cave == cave):
                        idx_old_cave = idx
                        break
                new_caves_dict[adj_cave].append(cave + "2")
                new_caves_dict[adj_cave][idx_old_cave] = cave + "1"

            # Recursion
            #visited = frozenset()
            #output += dfs_caves2("start", visited, (cave, False))
            dfs_caves2("start", ())
            #dfs_caves2.cache_clear()

    output = len(paths_set)

    return output

part1_example = process_inputs(example_file)
part1_example2 = process_inputs(example2_file)
part1_example3 = process_inputs(example3_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2_example2 = process_inputs2(example2_file)
part2_example3 = process_inputs2(example3_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2 example2: {part2_example2}')
print(f'Part 2 example3: {part2_example3}')
print(f'Part 2: {part2}')
