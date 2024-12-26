import pprint
import itertools
from tqdm import tqdm

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# DFS w/ cache based on hyper-neutrino's walkthrough
# Ref: https://www.youtube.com/watch?v=bLMj50cpOug

indices = {}
cache = {}

def get_max_pressure(node, t, bitmask, nodes, edges_dict, rates_dict):
  if (node, t, bitmask) in cache:
    return cache[(node, t, bitmask)]

  pressure = 0

  for edge in edges_dict[node]:
    next_node = edge[0]
    dist = edge[1]

    if (next_node == 'AA'):
      continue

    bit = 1 << indices[next_node]
    if (bitmask & bit):
      continue

    # open valve
    t_remaining = t - dist - 1

    if (t <= 0):
      continue
    
    pressure = max(pressure, get_max_pressure(next_node, t_remaining, bitmask | bit, nodes, edges_dict, rates_dict) + t_remaining*rates_dict[next_node])

  cache[(node, t, bitmask)] = pressure

  return pressure

# initialize variables
input_file = "../../inputs/2022/input16.txt"
#input_file = "example16.txt"

GREEDY = 0
BRUTE_FORCE = 0
DFS = 1

valves = []
rates_dict = {}
connections_dict = {}

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(" ")
    if ("valves" in txtfile_line):
      connections_csv = txtfile_line.split("valves ")
    else:
      connections_csv = txtfile_line.split("valve ")
    parsed_connections = connections_csv[1].split(", ")

    valves.append(parsed_line[1])
    rates_dict[parsed_line[1]] = int(parsed_line[4].split("rate=")[1][:-1])
    connections_dict[parsed_line[1]] = parsed_connections

    # read next line
    txtfile_line = txtfile.readline() 

# initialize list of valves with non-zero flow rates, but include 'AA', the starting node
nodes = []
edges_dict = {}
for v in valves:
  if (v != 'AA') and (rates_dict[v] == 0):
    continue
  else:
    nodes.append(v)
print(rates_dict)

# prepopulate edges_dict with empty list of edges
for n in nodes:
  edges_dict[n] = []

# BFS to construct graph of valves with non-zero flow rate, but include 'AA'
for idx_n, n in enumerate(nodes): 
  queue = []
  visited = []
  for c in connections_dict[n]:
    queue.append((c, 1))
  visited.append(n)

  while len(queue):
    q, d = queue[0]
    if (q not in visited):
      # add connections to queue      
      for c in connections_dict[q]:
        queue.append((c, d+1))

      visited.append(q)

      if (q in nodes):
        edges_dict[n].append((q, d))

    queue.pop(0)

print(nodes)
pretty_print = pprint.PrettyPrinter()
pretty_print.pprint(edges_dict)


# greedy algo
t = 30
relieved_pressure = 0
curr_node = 'AA'
opened_set = set()
while GREEDY:
  edge_list = edges_dict[curr_node]

  max_relieved_pressure = 0
  min_distance = 1000000
  max_time_remaining = -1
  max_relieved_pressure_w_cost = 0
  for idx_edge, edge in enumerate(edge_list):
    potential_node, distance = edge

    if (potential_node in opened_set):
      continue

    potential_time_remaining = t - distance - 1
    potential_relieved_pressure = potential_time_remaining*rates_dict[potential_node]

    # compute opportunity cost if other valves were opened first instead
    max_opportunity_cost = 0
    for idx_other_edge, other_edge in enumerate(edge_list):
      other_node, other_distance = other_edge
    
      if (other_node in opened_set) or (idx_other_edge == idx_edge) or (other_distance >= distance):
        continue 

      # take into account travel gain
      for pn in edges_dict[other_node]:
        if (pn[0] == potential_node):
          travel_gain = pn[1]
          break

      #opportunity_cost = (distance - other_distance)*rates_dict[other_node] + (travel_gain+1)*rates_dict[other_node]
      opportunity_cost = (t - other_distance - 1)*rates_dict[other_node] # works in sample but does not work in test

      max_opportunity_cost = max(max_opportunity_cost, opportunity_cost)

    if (potential_relieved_pressure-max_opportunity_cost > max_relieved_pressure_w_cost): # takes care of negative time remaining
      max_relieved_pressure_w_cost = potential_relieved_pressure - max_opportunity_cost
      min_distance = distance
      max_relieved_pressure = potential_relieved_pressure
      opened_node = potential_node
    elif (potential_relieved_pressure-max_opportunity_cost == max_relieved_pressure_w_cost) and (distance < min_distance):
      min_distance = distance
      max_relieved_pressure = potential_relieved_pressure
      opened_node = potential_node

  # open valve
  opened_set.add(opened_node)

  # update time, pressure, and current node
  if (max_relieved_pressure == 0):
    break
  else:
    relieved_pressure = relieved_pressure + max_relieved_pressure
    t = t - min_distance - 1
    curr_node = opened_node
    print(f'Valve {curr_node} opened at minute {30 - t}')

max_pressure = relieved_pressure

# brute force
if BRUTE_FORCE:
  opened_set.add('AA')
  max_pressure = 0
  curr_node = 'AA'
  for n_order in tqdm(itertools.permutations(nodes)):
    pressure = 0
    t = 30
    next_permutation = 0
    for n in n_order:
      if (n == 'AA'):
        continue

      edge_list = edges_dict[curr_node]
      for next_node, distance in edge_list:
        if (next_node == n) and (t - distance - 1) < 0:
          next_permutation = 1
          break
        elif (next_node == n):
          # open valve
          t = t - distance - 1
          curr_node = next_node
          pressure = pressure + t*rates_dict[next_node]

      if (next_permutation):
        break

    if (pressure > max_pressure):  
      max_pressure = pressure
      print(f'current max pressure: {max_pressure}')

# DFS
max_pressure_p2 = 0
if DFS:
  for idx, n in enumerate(nodes):
    if (n != 'AA'):
      indices[n] = idx


  #max_pressure = get_max_pressure('AA', 30, 0, nodes, edges_dict, rates_dict)

  # Completely from hyper-neutrino
  b = (1 << len(nodes)) - 1
  for i in range(0, (b + 1)//2):
    max_pressure_p2 = max(max_pressure_p2, get_max_pressure('AA', 26, i, nodes, edges_dict, rates_dict) + get_max_pressure('AA', 26, b ^ i, nodes, edges_dict, rates_dict))
     
# print answer
ans1 = max_pressure
ans2 = max_pressure_p2
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
