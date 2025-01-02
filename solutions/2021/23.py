import math
from collections import defaultdict
from collections import deque
from functools import cache

input_file = "../../inputs/2021/input23.txt"
example_file = "example23.txt"
example2_file = "example23_2.txt"
example3_file = "example23_3.txt"
example4_file = "example23_4.txt"

part1_example = 0
part1_example2 = 0
part1_example3 = 0
part1_example4 = 0
part2_example = 0
part1 = 0
part2 = 0

# Prepopulated data structures for easier operations
inner_room_dict = {
    'A': (3, 3),
    'B': (3, 5),
    'C': (3, 7),
    'D': (3, 9)
}
outer_room_dict = {
    'A': (2, 3),
    'B': (2, 5),
    'C': (2, 7),
    'D': (2, 9)
}
rooms_list = []
outer_rooms_list = []
inner_rooms_list = []
for a_type in ['A', 'B', 'C', 'D']:
    rooms_list.append(inner_room_dict[a_type])
    rooms_list.append(outer_room_dict[a_type])
    inner_rooms_list.append(inner_room_dict[a_type])
    outer_rooms_list.append(outer_room_dict[a_type])

hallway_list = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11)]
room_hall_list = [(1, 3), (1, 5), (1, 7), (1, 9)]

energy_dict = {
    'A' : 1,
    'B' : 10,
    'C' : 100,
    'D' : 1000
}

# Prepopulated data structures for part 2
# Rooms represented as:
# outer2
# outer1
# inner2
# inner1
outer2_room_dict = {
    'A': (2, 3),
    'B': (2, 5),
    'C': (2, 7),
    'D': (2, 9)
}
outer1_room_dict = {
    'A': (3, 3),
    'B': (3, 5),
    'C': (3, 7),
    'D': (3, 9)
}
inner2_room_dict = {
    'A': (4, 3),
    'B': (4, 5),
    'C': (4, 7),
    'D': (4, 9)
}
inner1_room_dict = {
    'A': (5, 3),
    'B': (5, 5),
    'C': (5, 7),
    'D': (5, 9)
}
rooms_list = []
outer2_rooms_list = []
outer1_rooms_list = []
inner2_rooms_list = []
inner1_rooms_list = []
for a_type in ['A', 'B', 'C', 'D']:
    rooms_list.append(outer2_room_dict[a_type])
    rooms_list.append(outer1_room_dict[a_type])
    rooms_list.append(inner2_room_dict[a_type])
    rooms_list.append(inner1_room_dict[a_type])

    outer2_rooms_list.append(outer2_room_dict[a_type])
    outer1_rooms_list.append(outer1_room_dict[a_type])
    inner2_rooms_list.append(inner2_room_dict[a_type])
    inner1_rooms_list.append(inner1_room_dict[a_type])

# For debugging
spaces_list_example4 = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (2, 3)]
amphipods_list_example4 = [('A', (3, 3)), ('A', (3, 9)), ('B', (2, 5)), ('B', (3, 5)), ('C', (2, 7)), ('C', (3, 7)), ('D', (1, 
6)), ('D', (2, 9))]

def get_cost_lists(spaces_list, amphipods_list, a_type, start_rc, end_rc):
    spaces_list.remove(end_rc)
    spaces_list.append(start_rc)

    amphipods_list.remove((a_type, start_rc))
    amphipods_list.append((a_type, end_rc))

    start_row, start_col = start_rc
    end_row, end_col = end_rc
    energy_cost = energy_dict[a_type]*(abs(end_row - start_row) + abs(end_col - start_col))

    spaces_list.sort()
    amphipods_list.sort()

    return energy_cost, spaces_list, amphipods_list

# DFS for part 2
@cache
def dfs_move2(spaces_tuple, amphipods_tuple):
    energy_cost = math.inf
    base_case = True
    for amphipod in amphipods_tuple:
        a_type, rc = amphipod
        outer2_room = outer2_room_dict[a_type]
        outer1_room = outer1_room_dict[a_type]
        inner2_room = inner2_room_dict[a_type]
        inner1_room = inner1_room_dict[a_type]

        # Base case 1
        if (rc == inner1_room):
            continue

        # Base case 2
        inner1_correct = ((a_type, inner1_room) in amphipods_tuple)
        if (rc == inner2_room) and (inner1_correct):
            continue

        # Base case 3
        inner2_correct = ((a_type, inner2_room) in amphipods_tuple)
        if (rc == outer1_room) and (inner2_correct) and (inner1_correct):
            continue

        # Base case 4
        outer1_correct = ((a_type, outer1_room) in amphipods_tuple)
        if (rc == outer2_room) and (outer1_correct) and (inner2_correct) and (inner1_correct):
            continue
        base_case = False

        # If amphipod is in hallway
        if (rc in hallway_list):
            # If it can go inside the appropriate room slot
            if (outer2_room in spaces_tuple) and (outer1_correct) and (inner2_correct) and (inner1_correct):
                end_rc = outer2_room
            elif (outer1_room in spaces_tuple) and (inner2_correct) and (inner1_correct):
                end_rc = outer1_room
            elif (inner2_room in spaces_tuple) and (inner1_correct):
                end_rc = inner2_room
            elif (inner1_room in spaces_tuple):
                end_rc = inner1_room
            else:
                continue

            # BFS to check that it has a path to its room
            q = deque()
            visited = set()
            q.append(rc)
            while len(q):
                row, col = q.popleft()

                if ((row, col) in visited):
                    continue
                visited.add((row, col))

                # down
                n_tuple = (row+1, col)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # left
                n_tuple = (row, col-1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # right
                n_tuple = (row, col+1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

            # If we are able to reach the room, proceed with movement
            if (end_rc in visited):
                spaces_list = list(spaces_tuple)
                amphipods_list = list(amphipods_tuple)
                curr_cost, spaces_list, amphipods_list = get_cost_lists(spaces_list, amphipods_list, a_type, rc, end_rc)

                # Prune if current cost is worse than best cost
                #if (curr_cost > energy_cost):
                #    continue

                # Recursion
                energy_cost = min(energy_cost, curr_cost + dfs_move2(tuple(spaces_list), tuple(amphipods_list)))
        # Else, need to move to hallway if able to get out
        elif (rc in rooms_list):
             #((rc in outer1_rooms_list) and (above_outer2)) or \
             #((rc in inner2_rooms_list) and (above_outer1) and (above_outer2)) or \
             #((rc in inner1_rooms_list) and (above_inner2) and (above_outer1) and (above_outer2)):
            # Do BFS to check reachable spaces in hallway
            q = deque()
            visited = set()
            q.append(rc)
            while len(q):
                row, col = q.popleft()

                if ((row, col) in visited):
                    continue
                visited.add((row, col))

                # up
                n_tuple = (row-1, col)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # left
                n_tuple = (row, col-1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # right
                n_tuple = (row, col+1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

            # Amphipod moves to available spaces except for spaces in rooms_list or room_hall_list
            for reachable in visited:
                if (reachable in rooms_list) or (reachable in room_hall_list):
                    continue

                # Update
                spaces_list = list(spaces_tuple)
                amphipods_list = list(amphipods_tuple)
                curr_cost, spaces_list, amphipods_list = get_cost_lists(spaces_list, amphipods_list, a_type, rc, reachable)

                # Prune if current cost is worse than best cost
                #if (curr_cost > energy_cost):
                #    continue

                # Debugging
                if (list(spaces_tuple) == spaces_list_example4) and \
                   (list(amphipods_tuple) == amphipods_list_example4):
                    print(a_type, curr_cost, energy_cost, spaces_list)

                # Recursion
                energy_cost = min(energy_cost, curr_cost + dfs_move2(tuple(spaces_list), tuple(amphipods_list)))

    # Return 0 if in base case
    if (base_case):
        return 0

    return energy_cost

# DFS for part 1
@cache
def dfs_move(spaces_tuple, amphipods_tuple):
    energy_cost = math.inf
    base_case = True
    for amphipod in amphipods_tuple:
        a_type, rc = amphipod
        inner_room = inner_room_dict[a_type]

        # Base case: amphipod already in inner room
        if (rc == inner_room):
            continue

        # Base case: amphipod already in outer room while same type is in inner room
        other_amphipod = (a_type, inner_room)
        outer_room = outer_room_dict[a_type]
        if (rc == outer_room) and (other_amphipod in amphipods_tuple):
            continue
        base_case = False

        row, col = rc
        above_rc = (row-1, col)

        # Get hallway space above the room
        room_hall = (1, col)

        # If amphipod is in hallway
        if (rc in hallway_list):
            # If it can go inside a room
            if (inner_room in spaces_tuple):
                end_rc = inner_room
            # If it can go only to outer room
            elif (outer_room in spaces_tuple) and (other_amphipod in amphipods_tuple):
                end_rc = outer_room
            # Else, no possible action for this amphipod
            else:
                continue

            # BFS to check that it has a path to its room
            q = deque()
            visited = set()
            #q.append(room_hall)
            q.append(rc)
            while len(q):
                row, col = q.popleft()

                if ((row, col) in visited):
                    continue
                visited.add((row, col))

                # down
                n_tuple = (row+1, col)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # left
                n_tuple = (row, col-1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # right
                n_tuple = (row, col+1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

            # If we are able to reach the room, proceed with movement
            if (end_rc in visited):
                spaces_list = list(spaces_tuple)
                amphipods_list = list(amphipods_tuple)
                curr_cost, spaces_list, amphipods_list = get_cost_lists(spaces_list, amphipods_list, a_type, rc, end_rc)

                # Prune if current cost is worse than best cost
                #if (curr_cost > energy_cost):
                #    continue

                # Recursion
                energy_cost = min(energy_cost, curr_cost + dfs_move(tuple(spaces_list), tuple(amphipods_list)))
        # Else, need to move to hallway if able to get out
        elif (rc in outer_rooms_list) or ((rc in inner_rooms_list) and (above_rc in spaces_tuple)):
            # Do BFS to check reachable spaces in hallway
            q = deque()
            visited = set()
            q.append(room_hall)
            while len(q):
                row, col = q.popleft()

                if ((row, col) in visited):
                    continue
                visited.add((row, col))

                # left
                n_tuple = (row, col-1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

                # right
                n_tuple = (row, col+1)
                if (n_tuple in spaces_tuple):
                    q.append(n_tuple)

            # Amphipod moves to available spaces except for spaces in room_hall_list
            for reachable in visited:
                if (reachable in room_hall_list):
                    continue

                # Update
                spaces_list = list(spaces_tuple)
                amphipods_list = list(amphipods_tuple)
                curr_cost, spaces_list, amphipods_list = get_cost_lists(spaces_list, amphipods_list, a_type, rc, reachable)

                # Prune if current cost is worse than best cost
                #if (curr_cost > energy_cost):
                #    continue

                # Debugging
                if (list(spaces_tuple) == spaces_list_example4) and \
                   (list(amphipods_tuple) == amphipods_list_example4):
                    print(a_type, curr_cost, energy_cost, spaces_list)

                # Recursion
                energy_cost = min(energy_cost, curr_cost + dfs_move(tuple(spaces_list), tuple(amphipods_list)))

                # Debugging
                if (list(spaces_tuple) == spaces_list_example4) and \
                   (list(amphipods_tuple) == amphipods_list_example4):
                    print(energy_cost)

    # Return 0 if in base case
    if (base_case):
        return 0

    return energy_cost

def process_inputs(in_file):
    output = 0

    spaces_list = []
    amphipods_list = []
    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            #line = line.strip()

            col = 0
            for tile in line:
                if (tile == '.'):
                    spaces_list.append((row, col))
                elif (tile in ['A', 'B', 'C', 'D']):
                    amphipods_list.append((tile, (row, col)))
                col += 1

            row += 1

            line = file.readline()

    spaces_list.sort()
    amphipods_list.sort()
    print(spaces_list)
    print(amphipods_list)

    output = dfs_move(tuple(spaces_list), tuple(amphipods_list))

    return output

def process_inputs2(in_file):
    output = 0

    spaces_list = []
    amphipods_list = []
    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            #line = line.strip()

            col = 0
            for tile in line:
                if (tile == '.'):
                    spaces_list.append((row, col))
                elif (tile in ['A', 'B', 'C', 'D']):
                    # Append with higher row to give way to extra parts of diagram
                    if (row == 3):
                        amphipods_list.append((tile, (5, col)))
                    else:
                        amphipods_list.append((tile, (row, col)))
                col += 1

            row += 1

            line = file.readline()

    # Insert extra parts of diagram
    amphipods_list.append(('D', (3, 3)))
    amphipods_list.append(('D', (4, 3)))
    amphipods_list.append(('C', (3, 5)))
    amphipods_list.append(('B', (4, 5)))
    amphipods_list.append(('B', (3, 7)))
    amphipods_list.append(('A', (4, 7)))
    amphipods_list.append(('A', (3, 9)))
    amphipods_list.append(('C', (4, 9)))

    spaces_list.sort()
    amphipods_list.sort()
    print(spaces_list)
    print(amphipods_list)

    output = dfs_move2(tuple(spaces_list), tuple(amphipods_list))

    return output

part1_example = process_inputs(example_file)
#part1_example2 = process_inputs(example2_file)
#part1_example3 = process_inputs(example3_file) # should be 8+7000=7008
#part1_example4 = process_inputs(example4_file) # should be 7008+2003=90011
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1 example2: {part1_example2}')
print(f'Part 1 example3: {part1_example3}')
print(f'Part 1 example4: {part1_example4}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
