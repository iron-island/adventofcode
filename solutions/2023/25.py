from copy import deepcopy
import graphviz

input_file = "../../inputs/2023/input25.txt"
example_file = "example25.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def top3_edges(comp_dict, edge_count):

    edges = list(edge_count.keys())
    for c in comp_dict:
        # BFS
        queue = set()
        visited = set()
        queue.add(c)

        while len(queue):
            q = queue.pop()

            if q in visited:
                continue

            for t in comp_dict[c]:
                if (t not in visited):
                    queue.add(t)

                    if ((c,t) in edges):
                        edge_count[(c, t)] += 1
                    elif ((t, c) in edges):
                        edge_count[(t, c)] += 1

            visited.add(q)

def remove_comps(comp_dict, comps_list):
    new_dict = deepcopy(comp_dict)

    for c in comps_list:
        new_dict.pop(c)
    for c in comps_list:
        for n in new_dict:
            if (c in new_dict[n]):
                new_dict[n].remove(c)

    # BFS
    group1 = set() 
    group2 = set() 
    unvisited = list(new_dict.keys())
    queue = set()
    queue.add(unvisited[0]) # arbitrary
    while len(queue):
        q = queue.pop()

        if q in group1:
            continue

        for c in new_dict[q]:
            queue.add(c)

        group1.add(q)
        unvisited.remove(q)

    if len(unvisited):
        queue = set()
        queue.add(unvisited[0]) # arbitrary
        while len(queue):
            q = queue.pop()

            if q in group2:
                continue

            for c in new_dict[q]:
                queue.add(c)

            group2.add(q)
            unvisited.remove(q)

        if len(unvisited) == 0:
            g1 = len(group1)
            g2 = len(group2)
            print(f'Group 1: {group1}')
            print(f'Group 2: {group2}')
            return g1, g2
        else:
            return 0, 0
    else:
        return 0, 0

def cut1_wire(comp_dict, wire):
    new_dict = deepcopy(comp_dict)
    comp1, comp2 = wire

    new_dict[comp1].remove(comp2)
    new_dict[comp2].remove(comp1)

    # BFS
    group1 = set() 
    group2 = set() 
    unvisited = list(new_dict.keys())
    queue = set()
    queue.add(wire[0]) # arbitrary
    #print(f'Cut wires {wire1} and {wire2}')
    while len(queue):
        q = queue.pop()

        if q in group1:
            continue

        for c in new_dict[q]:
            queue.add(c)

        if (len(new_dict[q]) == 2):
            print(f'    Potential wire to cut: {q}-{new_dict[q]}')

        #if (wire1 == ('hfx', 'pzl')) and (wire2 == ('bvb', 'cmg')):
        #if (wire1 == ('pzl', 'hfx')) and (wire2 == ('bvb', 'cmg')):
        #    if (q == 'nvd'):
        #        print(f'    Looking at potential component {q}: {new_dict[q]}')
        #    elif (q == 'jqt'):
        #        print(f'    Looking at potential component {q}: {new_dict[q]}')
        #    elif (q in ['hfx', 'pzl', 'bvb', 'cmg']):
        #        print(f'    Already cut component {q}: {new_dict[q]}')

        group1.add(q)
        unvisited.remove(q)

def cut2_wires(comp_dict, wire1, wire2):
    new_dict = deepcopy(comp_dict)
    for wire in [wire1, wire2]:
        comp1, comp2 = wire

        new_dict[comp1].remove(comp2)
        new_dict[comp2].remove(comp1)

    # BFS
    group1 = set() 
    group2 = set() 
    unvisited = list(new_dict.keys())
    queue = set()
    queue.add(wire1[0]) # arbitrary
    #print(f'Cut wires {wire1} and {wire2}')
    while len(queue):
        q = queue.pop()

        if q in group1:
            continue

        for c in new_dict[q]:
            queue.add(c)

        if (len(new_dict[q]) == 1):
            print(f'    Potential wire to cut: {q}-{new_dict[q]}')

        #if (wire1 == ('hfx', 'pzl')) and (wire2 == ('bvb', 'cmg')):
        #if (wire1 == ('pzl', 'hfx')) and (wire2 == ('bvb', 'cmg')):
        #    if (q == 'nvd'):
        #        print(f'    Looking at potential component {q}: {new_dict[q]}')
        #    elif (q == 'jqt'):
        #        print(f'    Looking at potential component {q}: {new_dict[q]}')
        #    elif (q in ['hfx', 'pzl', 'bvb', 'cmg']):
        #        print(f'    Already cut component {q}: {new_dict[q]}')

        group1.add(q)
        unvisited.remove(q)

def cut_wire(comp_dict, wire1, wire2, wire3):
    DEBUG = False
    if (wire1 == ('cmg', 'bvb')) and (wire2 == ('pzl','hfx')) and (wire3 == ('nvd', 'jqt')):
        print(f'Expected solution!')
        DEBUG = True

    new_dict = deepcopy(comp_dict)

    #print(f'Cutting wires: {wire1}, {wire2}, {wire3}')
    for wire in [wire1, wire2, wire3]:
        comp1, comp2 = wire
        #print(f'wire: {comp1}-{comp2}')
        #print(f'    {comp1} connections: {new_dict[comp1]}')
        #print(f'    {comp2} connections: {new_dict[comp2]}')

        new_dict[comp1].remove(comp2)
        new_dict[comp2].remove(comp1)

    if DEBUG:
        for n in new_dict:
            print(f'{n}: {new_dict[n]}')

    # BFS
    group1 = set() 
    group2 = set() 
    unvisited = list(new_dict.keys())
    if DEBUG:
        print(f'Initial unvisited length: {len(unvisited)}')
    queue = set()
    queue.add(wire1[0]) # arbitrary
    while len(queue):
        if DEBUG:
            print(queue)
        q = queue.pop()

        if q in group1:
            continue

        for c in new_dict[q]:
            queue.add(c)

        group1.add(q)
        unvisited.remove(q)
    if DEBUG:
        print(f'First group length: {len(group1)}, unvisited length: {len(unvisited)}')

    if len(unvisited):
        queue = set()
        queue.add(unvisited[0]) # arbitrary
        while len(queue):
            q = queue.pop()

            if q in group2:
                continue

            for c in new_dict[q]:
                queue.add(c)

            group2.add(q)
            unvisited.remove(q)

        if len(unvisited) == 0:
            g1 = len(group1)
            g2 = len(group2)
            if DEBUG:
                print(f'Groups: {g1}, {g2}')
            print(f'Group 1: {group1}')
            print(f'Group 2: {group2}')
            return g1, g2
        else:
            if DEBUG:
                print("Groups: 0, 0")
            return 0, 0
    else:
        if DEBUG:
            print("Groups: 0, 0")
        return 0, 0

def process_inputs(in_file):
    output = 0

    comp_dict = {}
    right_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            left, right = line.split(": ")
            comp_dict[left] = set(right.split())
            right_list.append(right.split())

            line = file.readline()

    # Extend configurations
    for idx_rl, rl in enumerate(right_list):
        for r in rl:
            if (r not in comp_dict):
                comp_dict[r] = set()

            for c in comp_dict:
                if (r in comp_dict[c]):
                    comp_dict[r].add(c)
    print(comp_dict)
    print(f'No. of components: {len(comp_dict)}')

    # HEURISTIC: Top 3 components with most 1st and 2nd degree connections have wires to cut

    # Test script to check for number of 1st and 2nd degree connections each component
    num_conn_list = []
    num_conn_dict = {}
    for c in comp_dict:
        # 1st degree connections
        temp_set = set(comp_dict[c])

        # 2nd degree connections
        #for d in comp_dict:
        #    if (d == c):
        #        continue

        #    if (c in comp_dict[d]):
        #        temp_set.add(d)
        #        temp_set = temp_set.union(comp_dict[d])

        num_conn = len(temp_set) - 1

        print(f'{c} components: {num_conn} connections')
        num_conn_list.append(num_conn)
        num_conn_dict[c] = num_conn
    print(sorted(num_conn_list))

    # Get top 3
    top1 = 0
    top2 = 0
    top3 = 0
    top3_list = ['', '', '']
    for c in num_conn_dict:
        num_conn = num_conn_dict[c]
        if (num_conn > top1):
            top1 = num_conn
            top3_list.insert(0, c)
            top3_list.pop(3)
        elif (num_conn > top2):
            top2 = num_conn
            top3_list.insert(1, c)
            top3_list.pop(3)
        elif (num_conn > top3):
            top3 = num_conn
            top3_list.insert(2, c)
            top3_list.pop(3)

    ''' Find top 3 one at a time and should not be 1st/2nd degree connections to each other
    # Find top 1 first
    top1_conn = 0
    top3_list = ['', '', '']
    for c in num_conn_dict:
        num_conn = num_conn_dict[c]
        if (num_conn > top1_conn):
            top1_conn = num_conn
            top3_list[0] = c
    # Find top 2
    top2_conn = 0
    top1, _, _ = top3_list
    for c in num_conn_dict:
        if (c in comp_dict[top1]) or (c in top3_list):
            continue

        num_conn = num_conn_dict[c]
        if (num_conn > top2_conn):
            top2_conn = num_conn
            top3_list[1] = c
    # Find top 3
    top3_conn = 0
    top1, top2, _ = top3_list
    for c in num_conn_dict:
        if (c in comp_dict[top1]) or (c in comp_dict[top2]) or (c in top3_list):
            continue

        num_conn = num_conn_dict[c]
        if (num_conn > top3_conn):
            top3_conn = num_conn
            top3_list[2] = c
    '''

    print(f'Top 3 components are {top3_list}')

    # Test script to check for number of connections under specific components
    #num_conn_list = []
    #for c in comp_dict["cmg"]:
    #for c in comp_dict["pzl"]:
    #for c in comp_dict["nvd"]:
    #    if (c in top3_list):
    #        continue

    #    temp_set = set(comp_dict[c])

    #    for d in comp_dict:
    #        if (d == c):
    #            continue

    #        if (c in comp_dict[d]):
    #            temp_set.add(d)
    #            temp_set = temp_set.union(set(comp_dict[d]))

    #    num_conn = len(temp_set) - 1
    #    print(f'{c} components: {num_conn} connections')
    #    num_conn_list.append(num_conn)
    #print(sorted(num_conn_list))

    ''' Based only on top 3
    top1, top2, top3 = top3_list
    for t1 in comp_dict[top1]:
        if (t1 in top3_list) or (t1 in comp_dict[top2]) or (t1 in comp_dict[top3]):
            continue
        for t2 in comp_dict[top2]:
            if (t2 in top3_list) or (t2 in comp_dict[top1]) or (t2 in comp_dict[top3]):
                continue
            for t3 in comp_dict[top3]:
                if (t3 in top3_list) or (t3 in comp_dict[top1]) or (t3 in comp_dict[top2]):
                    continue

                wire1 = (top1, t1)
                wire2 = (top2, t2)
                wire3 = (top3, t3)

                g1, g2 = cut_wire(comp_dict, wire1, wire2, wire3)
                if (g2 > 0):
                    return g1*g2
    '''

    '''# Vertex removal based on top 3
    g1, g2 = remove_comps(comp_dict, top3_list)
    return g1*g2
    '''

    ''' Check most frequently used edges
    # Get unique edges
    edges = set()
    reversed_edges = set()
    for c in comp_dict:
        for d in comp_dict[c]:
            if ((d, c) not in edges):
                edges.add((c, d))
                reversed_edges.add((d, c))

    edge_count = {}
    for e in edges:
        edge_count[e] = 0

    top3_edges(comp_dict, edge_count)

    top1 = 0
    top2 = 0
    top3 = 0
    top3_list = ['', '', '']
    edge_count_list = []
    for e in edge_count:
        count = edge_count[e]
        edge_count_list.append(count)
        if (count > top1):
            top1 = count
            top3_list[0] = e
        elif (count > top2):
            top2 = count
            top3_list[1] = e
        elif (count > top3):
            top3 = count
            top3_list[2] = e
    print(sorted(edge_count_list))
    print(f'Top edges are {top3_list}')
    '''

    # Graphviz
    #dot = graphviz.Graph()
    #for c in comp_dict:
    #    dot.node(c)

    #for e in edges:
    #    c1, c2 = e
    #    dot.edge(c1, c2)
    #dot.engine = 'neato'
    #dot.render(directory='doctest-output', view=True)
    # Hardcoded based on Graphviz neato visualization
    g1, g2 = cut_wire(comp_dict, ('jbz', 'sqh'), ('vfj', 'nvg'), ('fch', 'fvh'))
    output = g1*g2
    
    return output

#part1_example = process_inputs(example_file) # disconnect hfx/pzl, bvb/cmg, nvd/jqt
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
