import pprint

FINAL_Y = 0
FINAL_X  = 0

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
input_file = "../../inputs/2022/input12.txt"
#input_file = "example12.txt"

def next_candidate(grid, visited, queue, curr_y, curr_x, cand_y, cand_x):
  if ([cand_y, cand_x] not in queue) and ([cand_y, cand_x] not in visited) and ((grid[cand_y][cand_x] - grid[curr_y][curr_x]) <= 1):
    return True
  else:
    return False

grid = []

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()

    # process
    grid.append(txtfile_line)

    # read next line
    txtfile_line = txtfile.readline() 

starting_list = []

for idx_row, row in enumerate(grid):
  new_row = []
  for idx_x, x in enumerate(row):
    curr_y = idx_row
    curr_x = idx_x

    if (x == 'S'):
      new_row.append(ord('a'))
      starting_list.append([curr_y, curr_x])
    elif (x == 'E'):
      FINAL_Y = idx_row
      FINAL_X = idx_x
      new_row.append(ord('z'))
    else:
      new_row.append(ord(x))

      if (x == 'a'):
        starting_list.append([curr_y, curr_x])

  grid[idx_row] = new_row

# BFS
depth_list = []

print(starting_list)

for idx_s, s in enumerate(starting_list):
  curr_y, curr_x = s  
  visited = []
  depth = 0
  print(f'START {idx_s}/{len(starting_list)}: ({curr_y}, {curr_x})')
  queue = []
  depth_queue = []
  queue.append([curr_y, curr_x])
  depth_queue.append(0)
  
  ans1 = 0
  iterations = 0
  while len(queue):
    y, x = queue[0]
    depth = depth_queue[0]
    visited.append([y, x])
  
    if (y == FINAL_Y) and (x == FINAL_X):
      ans1 = depth
      queue = []
      depth_queue = []
      depth_list.append(depth)
      print(f'depth = {depth}')
      break
  
    right_y = y
    right_x = x + 1
    up_y = y - 1
    up_x = x
    left_y = y
    left_x = x - 1
    down_y = y + 1
    down_x = x
  
    if (right_x < len(grid[0])) and (next_candidate(grid, visited, queue, y, x, right_y, right_x)):
      queue.append([right_y, right_x])
      depth_queue.append(depth+1)
    
    if (up_y >= 0) and (next_candidate(grid, visited, queue, y, x, up_y, up_x)):
      queue.append([up_y, up_x])
      depth_queue.append(depth+1)
  
    if (left_x >= 0) and (next_candidate(grid, visited, queue, y, x, left_y, left_x)):
      queue.append([left_y, left_x])
      depth_queue.append(depth+1)
  
    if (down_y < len(grid)) and (next_candidate(grid, visited, queue, y, x, down_y, down_x)):
      queue.append([down_y, down_x])
      depth_queue.append(depth+1)
  
    queue.pop(0)
    depth_queue.pop(0)
    iterations += 1

# queue
#myqueue = []
#myqueue.append('a')
#myqueue.append('b')
#myqueue.append('c')
#myqueue # ['a', 'b', 'c']
#myqueue.pop(0) # ['b', 'c']
#myqueue.index('c') # 1
#myqueue.pop(1) # ['b']

pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(grid)

# print answer
print(f'FINAL: ({FINAL_Y}, {FINAL_X})')
print(depth_list)
min_depth = min(depth_list)
ans1 = depth
ans2 = min_depth
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
