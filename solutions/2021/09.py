import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
input_file = '../../inputs/2021/input09.txt'
iterations = 5
num_y = 0
num_x = 0

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    #parsed_line = txtfile_line.split()
    num_x = len(txtfile_line) - 1 # remove \n
    
    # process
    num_y = num_y + 1
    # read next line
    txtfile_line = txtfile.readline() 

heightmap = [[0 for i in range(num_x)] for i in range(num_y)]

# read input file
j = 0
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    for i in range(num_x):
      num = txtfile_line[i]
      heightmap[j][i] = int(num) + 1 # incorporate the risk level
    
    # process
    j = j + 1
    # read next line
    txtfile_line = txtfile.readline() 

risk = 0
lowpoints = 0
for j in range(num_y):
  for i in range(num_x):
    if (j > 0):
      up = heightmap[j-1][i]
    else:
      up = 100

    if (j < (num_y-1)):
      down = heightmap[j+1][i]
    else:
      down = 100

    if (i > 0):
      before = heightmap[j][i-1]
    else:
      before = 100

    if (i < (num_x-1)):
      after = heightmap[j][i+1]
    else:
      after = 100

    cur = heightmap[j][i]
    if (cur < before) and (cur < after) and (cur < up) and (cur < down):
      lowpoints = lowpoints + 1
      risk = risk + cur

basin1 = 0
basin2 = 0
basin3 = 0

# find regions bounded by 9
bound = 1000
basinmap = [[bound for i in range(num_x)] for j in range(num_y)]
# print answer

cur_basin = 0
for j in range(num_y):
  for i in range(num_x):
    cur = heightmap[j][i]
    b = basinmap[j][i]

    up_present = j > 0
    down_present = (j < (num_y-1))
    left_present = (i > 0)
    right_present = (i < (num_x-1))

    if (cur < 10):
      # inherit if not yet inherited
      if (b == bound):
        if up_present:
          up_b = basinmap[j-1][i]
        else:
          up_b = bound
          up = 10

        if down_present:
          down_b = basinmap[j+1][i]
          down = heightmap[j+1][i]
        else:
          down_b = bound
          down = 10

        if left_present:
          left_b = basinmap[j][i-1]
        else:
          left_b = bound
          left = 10

        if right_present:
          right_b = basinmap[j][i+1]
          right = heightmap[j][i+1]
        else:
          right_b = bound
          right = 10

        # diagonals
        if up_present and left_present:
          up_left_b = basinmap[j-1][i-1]
        else:
          up_left_b = bound

        if up_present and right_present:
          up_right_b = basinmap[j-1][i+1]
        else:
          up_right_b = bound

        if down_present and left_present:
          down_left_b = basinmap[j+1][i-1]
        else:
          down_left_b = bound

        if down_present and right_present:
          down_right_b = basinmap[j+1][i+1]
        else:
          down_right_b = bound
      
        if (up_b < bound) or (left_b < bound) or (right_b < bound) or (down_b < bound):
          # inherit  
          b = min(up_b, left_b, right_b, down_b)

          # some basins might be the same
          if (up_b < bound) and (up_b != b):
            print("ERROR!")
          if (down_b < bound) and (down_b != b):
            print("ERROR!")
          if (left_b < bound) and (left_b != b):
            print("ERROR!")
          if (right_b < bound) and (right_b != b):
            print("ERROR!")

          basinmap[j][i] = b
        else:
          # or assign new basin
          b = cur_basin
          basinmap[j][i] = b
          cur_basin = cur_basin + 1

      # end if (b == bound)

      b = basinmap[j][i]
      if down_present:
        down_b = basinmap[j+1][i]
        down = heightmap[j+1][i]
      else:
        down_b = bound
        down = 10

      if right_present:
        right_b = basinmap[j][i+1]
        right = heightmap[j][i+1]
      else:
        right_b = bound
        right = 10

      if down_present and left_present:
        down_left_b = basinmap[j+1][i-1]
        down_left = heightmap[j+1][i-1]
      else:
        down_left_b = bound
        down_left = 10

      if down_present and right_present:
        down_right_b = basinmap[j+1][i+1]
        down_right = heightmap[j+1][i+1]
      else:
        down_right_b = bound
        down_right = 10

      # spread
      if (b < bound):
        if right_present and (right_b == bound) and (right < 10):
          basinmap[j][i+1] = b
          right_b = b

        if down_present and (down_b == bound) and (down < 10):
          basinmap[j+1][i] = b
          down_b = b

        # spread to diagonals
        if ((down_b == b) or (right_b == b)) and (down_right < 10):
          basinmap[j+1][i+1] = b

        if ((down_b == b) or (left_b == b)) and (down_left < 10):
          basinmap[j+1][i-1] = b

    # end if of if (c < 10)

# repopulate basin
for x in range(iterations):
  # bin the basin
  basin_bins = [0 for i in range(cur_basin)]
  num_bounds = 0
  for j in range(num_y):
    for i in range(num_x):
      cur = heightmap[j][i]
      b = basinmap[j][i]
  
      if (b < bound):
        basin_bins[b] = basin_bins[b] + 1
      else:
        num_bounds = num_bounds + 1
  
  for i in range(num_x):
    for j in range(num_y):
      cur = heightmap[j][i]
      b = basinmap[j][i]
  
      up_present = j > 0
      down_present = (j < (num_y-1))
      left_present = (i > 0)
      right_present = (i < (num_x-1))
  
      if (b < bound):
        if up_present:
          up_b = basinmap[j-1][i]
        else:
          up_b = bound
          up = 10
  
        if down_present:
          down_b = basinmap[j+1][i]
          down = heightmap[j+1][i]
        else:
          down_b = bound
          down = 10
  
        if left_present:
          left_b = basinmap[j][i-1]
        else:
          left_b = bound
          left = 10
  
        if right_present:
          right_b = basinmap[j][i+1]
          right = heightmap[j][i+1]
        else:
          right_b = bound
          right = 10
  
        # respread
        count = basin_bins[b]
        up_count = 0
        if (up_b < bound) and (up_b != b):
          up_count = basin_bins[up_b]
  
        down_count = 0
        if (down_b < bound) and (down_b != b):
          down_count = basin_bins[down_b]
  
        left_count = 0
        if (left_b < bound) and (left_b != b):
          left_count = basin_bins[left_b]
  
        right_count = 0
        if (right_b < bound) and (right_b != b): 
          right_count = basin_bins[right_b]
  
        max_count = max(up_count, down_count, left_count, right_count, count)

        if (max_count == up_count):
          b = up_b
        elif (max_count == down_count):
          b = down_b
        elif (max_count == left_count):
          b = left_b
        elif (max_count == right_count):
          b = right_b
  
        basinmap[j][i] = b
        if (up_b < bound) and (up_b != b):
          basinmap[j-1][i] = b
  
        if (down_b < bound) and (down_b != b):
          basinmap[j+1][i] = b
  
        if (left_b < bound) and (left_b != b):
          basinmap[j][i-1] = b
  
        if (right_b < bound) and (right_b != b): 
          basinmap[j][i+1] = b

# bin the basin one last time
basin_bins = [0 for i in range(cur_basin)]
num_bounds = 0
for j in range(num_y):
  for i in range(num_x):
    cur = heightmap[j][i]
    b = basinmap[j][i]

    if (b < bound):
      basin_bins[b] = basin_bins[b] + 1
    else:
      num_bounds = num_bounds + 1

nonempty_bins = [x for x in basin_bins if (x > 0)]
cur_basin = len(nonempty_bins)

basin_bins = nonempty_bins
print(num_x)
print(num_y)
print(lowpoints)
print(cur_basin)
print(num_bounds)
print(basin_bins)
basin1 = max(basin_bins)
print(basin1)
basin_bins.remove(basin1)
basin2 = max(basin_bins)
print(basin2)
basin_bins.remove(basin2)
basin3 = max(basin_bins)
print(basin3)

# print answer
#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(basinmap)

print("First star: %d" % (risk))
print("Second star: %d" % (basin1*basin2*basin3))
