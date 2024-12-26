import pprint

# initialize variables
init_x = []
init_y = []
end_x = []
end_y = []

minx = 10000
maxx = 0
miny = 10000
maxy = 0

# read input file
with open('../../inputs/2021/input05.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    parsed_line = txtfile_line.split(" ")
    x1y1 = parsed_line[0]
    x2y2 = parsed_line[2]
    x1y1_split = x1y1.split(",")
    x2y2_split = x2y2.split(",")
    init_x.append(int(x1y1_split[0]))
    init_y.append(int(x1y1_split[1]))
    end_x.append(int(x2y2_split[0]))
    end_y.append(int(x2y2_split[1]))
    
    # read next line
    txtfile_line = txtfile.readline() 

# find bounds
for i in init_x:
  if (i > maxx):
    maxx = i

  if (i < minx):
    minx = i

for i in end_x:
  if (i > maxx):
    maxx = i

  if (i < minx):
    minx = i

for j in init_y:
  if (j > maxy):
    maxy = j

  if (j < miny):
    miny = j

for j in end_y:
  if (j > maxy):
    maxy = j

  if (j < miny):
    miny = j

# construct grid
grid = [[0 for i in range(maxx+1)] for j in range(maxy+1)]

print(maxx)
print(maxy)

num_inputs = len(init_x)

# populate grid
for n in range(num_inputs):

  x1 = init_x[n]
  y1 = init_y[n]
  x2 = end_x[n]
  y2 = end_y[n]
  
  diagonal = 0
  if ((abs(x2 - x1)) and (abs(y2-y1))):
    diff = abs(x2 - x1)
    diagonal = 1
    zipx = []
    zipy = []

    if (x2 >= x1):
      for i in range(x1, x2+1):
        zipx.append(i)
    else:
      for i in range(x1, x2-1, -1):
        zipx.append(i)

    if (y2 >= y1):
      for j in range(y1, y2+1):
        zipy.append(j)
    else:
      for j in range(y1, y2-1, -1):
        zipy.append(j)

  # only vertical and horizontal lines
  if (x1 == x2):
    if (y2 >= y1):
      for j in range(y1, y2+1):
        grid[j][x1] = grid[j][x1] + 1
    else:
      for j in range(y1, y2-1, -1):
        grid[j][x1] = grid[j][x1] + 1
  elif (y1 == y2):
    if (x2 >= x1):
      for i in range(x1, x2 + 1):
        grid[y1][i]  = grid[y1][i] + 1
    else:    
      for i in range(x1, x2 - 1, -1):
        grid[y1][i]  = grid[y1][i] + 1
  elif (diagonal):
    for i,j in zip(zipx, zipy):
      grid[j][i] = grid[j][i] + 1

# compute
num_intersections = 0
for i in range(maxx+1):
  for j in range(maxy+1):
    if (grid[j][i] > 1):
      num_intersections = num_intersections + 1

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(grid)

# print answer
print("First star: %d" % (num_intersections))
