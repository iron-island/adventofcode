import pprint
import math
import sys

width = 0
height = 0

def print_valley(empty_tiles_t, blizzards):
  right_blizzard = blizzards[0]
  left_blizzard = blizzards[1]
  up_blizzard = blizzards[2]
  down_blizzard = blizzards[3]

  for y in range(1, height+1):
    for x in range(1, width+1):  
      coord = complex(x, y)

      if coord in empty_tiles_t:
        print(".", end="")
      elif coord in right_blizzard:
        print(">", end="")
      elif coord in left_blizzard:
        print("<", end="")
      elif coord in up_blizzard:
        print("^", end="")
      elif coord in down_blizzard:
        print("v", end="")

    print("")

#print(sys.setrecursionlimit(1500))

cache = {}
def dfs(t, empty_tiles, visited, curr, wait_t):

  if (curr == complex(width, height+1)):
    print(f'Reached goal in {t} minutes!')

    cache[(t, curr, wait_t)] = t
    return t

  if (t, curr, wait_t) in cache:
    return cache[(t, curr, wait_t)]

  if (wait_t >= 10):
    # if waited too long, stop exploring deeper states
    cache[(t, curr, wait_t)] = math.inf
    return math.inf
  else:
    #visited.add(curr)

    # construct neighbors based on empty tiles on the next time,
    next_empty_tiles = empty_tiles[(t+1) % len(empty_tiles)]
    neighbors = set()
    if (curr+1) in next_empty_tiles: # and (curr+1) not in visited:
      neighbors.add(curr+1)

    if (curr+1j) in next_empty_tiles: # and (curr+1j) not in visited:
      neighbors.add(curr+1j)

    if (curr) in next_empty_tiles:
      neighbors.add(curr)

    if (curr-1) in next_empty_tiles: # and (curr-1) not in visited:
      neighbors.add(curr-1)

    if (curr-1j) in next_empty_tiles and ((curr-1j) != complex(1, 0)): # and (curr+1j) not in visited:
      neighbors.add(curr-1j)

    if len(neighbors):
      min_t = math.inf
      print(neighbors)
      print(wait_t)
      for n in neighbors:
        if (n == curr):
          min_t = min(min_t, dfs(t+1, empty_tiles, visited, n, wait_t+1))
        else:
          min_t = min(min_t, dfs(t+1, empty_tiles, visited, n, 0))

      cache[(t, curr, wait_t)] = min_t
      return min_t
    else:
      # dead end, stop exploring deeper states
      cache[(t, curr, wait_t)] = math.inf
      return math.inf

# initialize variables
input_file = "../../inputs/2022/input24.txt"
#input_file = "example24.txt"

left_blizzard = set()
right_blizzard = set()
up_blizzard = set()
down_blizzard = set()
# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  row = 0
  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    
    for idx, t in enumerate(txtfile_line):
      coordinate = complex(idx, row)
      if (t == ">"):
        right_blizzard.add(coordinate)
      elif (t == "<"):
        left_blizzard.add(coordinate)
      elif (t == "^"):
        up_blizzard.add(coordinate)
      elif (t == "v"):
        down_blizzard.add(coordinate)

    width = len(txtfile_line) - 2

    # read next line
    txtfile_line = txtfile.readline() 
    row += 1

height = row - 2

all_tiles = set()
for y in range(1, height+1):
  for x in range(1, width+1):
    all_tiles.add(complex(x, y))
# add start and ending positions to all_tiles
all_tiles.add(complex(1, 0))
all_tiles.add(complex(width, height+1))

# precompute simulation, since it would repeat every num_row*num_col
empty_tiles = []
empty_tiles.append(all_tiles - (right_blizzard | left_blizzard | up_blizzard | down_blizzard))
for t in range(1, int(width*height)):
  next_right_blizzard = set()
  unit_move = complex(1, 0)
  for r in right_blizzard:
    if (r.real < width):
      next_right_blizzard.add(r + unit_move)
    else:
      next_right_blizzard.add(complex(1, r.imag))
  right_blizzard = next_right_blizzard.copy()

  next_left_blizzard = set()
  unit_move = complex(-1, 0)
  for l in left_blizzard:
    if (l.real > 1):
      next_left_blizzard.add(l + unit_move)
    else:
      next_left_blizzard.add(complex(width, l.imag))
  left_blizzard = next_left_blizzard.copy()

  next_up_blizzard = set()
  unit_move = complex(0, -1)
  for u in up_blizzard:
    if (u.imag > 1):
      next_up_blizzard.add(u + unit_move)
    else:
      next_up_blizzard.add(complex(u.real, height))
  up_blizzard = next_up_blizzard.copy()

  next_down_blizzard = set()
  unit_move = complex(0, 1)
  for d in down_blizzard:
    if (d.imag < height):
      next_down_blizzard.add(d + unit_move)
    else:
      next_down_blizzard.add(complex(d.real, 1))
  down_blizzard = next_down_blizzard.copy()

  # after precomputing, store only the empty tiles
  empty_tiles.append(all_tiles - (right_blizzard | left_blizzard | up_blizzard | down_blizzard))

blizzards = [right_blizzard, left_blizzard, up_blizzard, down_blizzard]
for t in range(0, 3):
  print(f'============== Minute {t}===============')
  #print_valley(empty_tiles[t], blizzards)

print("Starting BFS...")
queue = []
#queue.append((complex(1, 0), 0))
#queue.append((complex(width, height+1), 332)) 
queue.append((complex(1, 0), 630))
visited = set()
min_t = math.inf
while len(queue):
  if (queue[0] in visited):
    queue.pop(0)
    continue
  else:
    curr, t = queue[0]
    visited.add(queue[0])

    if (curr == complex(width, height+1)):
    #if (curr == complex(1, 0)):
      min_t = t
      break

  next_empty_tiles = empty_tiles[(t+1) % len(empty_tiles)]

  if (curr+1) in next_empty_tiles and ((curr+1, t+1) not in visited):
    queue.append((curr+1, t+1))

  if (curr+1j) in next_empty_tiles and ((curr+1j, t+1) not in visited):
    queue.append((curr+1j, t+1))

  if (curr) in next_empty_tiles and ((curr, t+1) not in visited):
    queue.append((curr, t+1))

  if (curr-1) in next_empty_tiles and ((curr-1, t+1) not in visited):
    queue.append((curr-1, t+1))

  if (curr-1j) in next_empty_tiles and ((curr-1j) != complex(1, 0)) and ((curr-1j, t+1) not in visited):
  #if (curr-1j) in next_empty_tiles and ((curr-1j, t+1) not in visited):
    queue.append((curr-1j, t+1))
  
  queue.pop(0)

print("Starting DFS...")
visited = set()
#min_t = math.inf
#min_t = dfs(0, empty_tiles, visited, complex(1, 0), 0)

# print answer
ans1 = 0
ans2 = min_t
print(f'First star: {ans1}')
print(f'Second star: {ans2}')
