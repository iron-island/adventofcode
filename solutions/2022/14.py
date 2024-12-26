import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def filled(x, y, grid, stack, filled_list):
  if (grid[y][x] != '.'):
    if [x, y] not in filled_list:
      filled_list.append([x, y])

    return True
  else:
    # add to stack if not yet filled in
    stack.append([x, y])    

    return False

def print_grid(grid):
  for row in grid:
    for g in row:
      print(g, end="")
    print("")

# initialize variables
input_file = "../../inputs/2022/input14.txt"
#input_file = "example14.txt"

parsed_line_list = []
# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(" -> ")
    parsed_line_list.append(parsed_line)

    # process

    # read next line
    txtfile_line = txtfile.readline() 

# lay rocks
min_x = 1000000
max_x = 0
max_y = 0
for parsed_line in parsed_line_list:
  for p in parsed_line:
    corners = p.split(",")
    corners[0] = int(corners[0])
    corners[1] = int(corners[1])

    max_x = max(max_x, corners[0])
    max_y = max(max_y, corners[1])
    min_x = min(min_x, corners[0])

part2 = 1
if (part2):
  min_x = min_x//2
  max_x = max_x + 200

print(min_x)
print(max_x)
print(max_y)

# construct grid
grid = []
grid_row = []
grid_floor = []
for r in range(0, max_x - min_x + 1):
  grid_row.append(".")
  grid_floor.append("W")
grid_row.append("W") # creates right wall
grid_floor.append("W") # creates floor

for i in range(0, max_y+1):
  grid.append(grid_row.copy())

part2 = 1
if part2:
  grid.append(grid_row.copy())
  grid.append(grid_floor.copy())
else:
  grid.append(grid_floor.copy())

# fill with rocks
for parsed_line in parsed_line_list:
  for i in range(1, len(parsed_line)):
    corner2 = parsed_line[i].split(",")
    corner2_x = int(corner2[0]) - min_x
    corner2_y = int(corner2[1])

    corner1 = parsed_line[i-1].split(",")
    corner1_x = int(corner1[0]) - min_x
    corner1_y = int(corner1[1])

    if (corner1_x == corner2_x):
      end_y = max(corner1_y, corner2_y)
      start_y = min(corner1_y, corner2_y)

      for y in range(start_y, end_y + 1):
        grid[y][corner1_x] = '#'

    elif (corner1_y == corner2_y):    
      end_x = max(corner1_x, corner2_x)
      start_x = min(corner1_x, corner2_x)

      for x in range(start_x, end_x + 1):
        grid[corner1_y][x] = '#'
    else:
      print("ERROR")
      print(f'[{corner1_x},{corner1_y}] -> [{corner2_x},{corner2_y}]')

#print_grid(grid)
FLOOR_Y = len(grid) - 1

# DFS
HOLE_X = 500 - min_x
HOLE_Y = 0
stack = []
stack.append([HOLE_X, HOLE_Y])
filled_list = []
filled_list.append([HOLE_X, HOLE_Y])

units = 0
iteration = 0
while len(stack):
  x = stack[-1][0]
  y = stack[-1][1]

  # check if grid was too small
  if (x == 0) or (x == len(grid[0]) + 1):
    print("ERROR, grid too small!")
    break

  # check sand overflow
  if not part2:
    if (y == len(grid) - 2):
      break

  if not filled(x, y, grid, stack, filled_list):
    # check down right, then check down left, then check down
    dr = filled(x+1, y+1, grid, stack, filled_list)
    dl = filled(x-1, y+1, grid, stack, filled_list)
    d  = filled(x, y+1, grid, stack, filled_list)

    if dr and dl and d:
      grid[y][x] = 'o'
      units = units + 1

      # check if full
      if part2:
        print(units)
        if (x == HOLE_X) and (y == HOLE_Y):
          break
  else:
    stack.pop()

  iteration = iteration + 1

#print_grid(grid)

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
#pretty_print.pprint()

# print answer
ans1 = units
ans2 = units
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
