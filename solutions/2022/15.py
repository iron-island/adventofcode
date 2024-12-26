#import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def get_line(bound1, bound2):
  x1 = bound1[0]
  y1 = bound1[1]

  x2 = bound2[0]
  y2 = bound2[1]

  points = []

  min_x = min(x1, x2)
  min_y = min(y1, y2)

  # x2-x1 and y2-y1 will always be equal, so just autoincrement y
  y = min_y + 1
  for x in range(min_x, min_y+1):
    points.append([x, y])
    y += 1

  return points

# Ref: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       #raise Exception('lines do not intersect')
      return -1, -1

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def get_intersections(line1, line2, other_line1, other_line2):
  candidates = []
  intersection_x, intersection_y = line_intersection(line1, other_line1)
  if (intersection_x != -1) and (intersection_x == int(intersection_x)):
    candidates.append([int(intersection_x-1), int(intersection_y-1)])
    candidates.append([int(intersection_x-1), int(intersection_y+1)])
    candidates.append([int(intersection_x+1), int(intersection_y-1)])
    candidates.append([int(intersection_x+1), int(intersection_y+1)])
  intersection_x, intersection_y = line_intersection(line2, other_line1)
  if (intersection_x != -1) and (intersection_x == int(intersection_x)):
    candidates.append([int(intersection_x-1), int(intersection_y-1)])
    candidates.append([int(intersection_x-1), int(intersection_y+1)])
    candidates.append([int(intersection_x+1), int(intersection_y-1)])
    candidates.append([int(intersection_x+1), int(intersection_y+1)])
  intersection_x, intersection_y = line_intersection(line1, other_line2)
  if (intersection_x != -1) and (intersection_x == int(intersection_x)):
    candidates.append([int(intersection_x-1), int(intersection_y-1)])
    candidates.append([int(intersection_x-1), int(intersection_y+1)])
    candidates.append([int(intersection_x+1), int(intersection_y-1)])
    candidates.append([int(intersection_x+1), int(intersection_y+1)])
  intersection_x, intersection_y = line_intersection(line2, other_line2)
  if (intersection_x != -1) and (intersection_x == int(intersection_x)):
    candidates.append([int(intersection_x-1), int(intersection_y-1)])
    candidates.append([int(intersection_x-1), int(intersection_y+1)])
    candidates.append([int(intersection_x+1), int(intersection_y-1)])
    candidates.append([int(intersection_x+1), int(intersection_y+1)])

  return candidates

def get_bounds(s, d):
  x = s[0]
  y = s[1]

  # add corners first
  bounds = []
  bounds.append([x - d, y    ])
  bounds.append([x    , y - d])
  bounds.append([x + d, y    ])
  bounds.append([x    , y + d])

  return bounds

# initialize variables
input_file = "../../inputs/2022/input15.txt"
#input_file = "example15.txt"

# read input file
sensors = []
beacons = []
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(" ")
   
    parse_sensor_x = int(parsed_line[2][:-1].split("x=")[1])
    parse_sensor_y = int(parsed_line[3][:-1].split("y=")[1])
    parse_beacon_x = int(parsed_line[8][:-1].split("x=")[1])
    parse_beacon_y = int(parsed_line[9].split("y=")[1])

    sensors.append([parse_sensor_x, parse_sensor_y])
    beacons.append([parse_beacon_x, parse_beacon_y])

    # read next line
    txtfile_line = txtfile.readline() 

print(sensors)
print(beacons)

if (input_file == "dec15_sample.txt"):
  ROW_Y = 10
else:
  ROW_Y = 2000000

# precompute manhattan distances
dist = []
max_x_ROW_Y = 0
for idx, s in enumerate(sensors):
  x = s[0]
  y = s[1]
  b_x = beacons[idx][0]
  b_y = beacons[idx][1]

  dist.append(abs(x - b_x) + abs(y - b_y)) 

  # find max x in ROW_Y that has a beacon?
  if (b_y == ROW_Y):
    max_x_ROW_Y = max(b_x, max_x_ROW_Y)

print(f'{len(dist)} Distances: {dist}')

curr_x = -5000000 # assumption
max_x  = 5000000 # assumption
curr_x = 0
num_empty = 0
grid_row = ""
early_exit = 0
curr_dist = []
prev_curr_dist = []
part2 = 1
while not part2:
  # stop if rightmost beacon is hit?
  #if (curr_x == max_x):
  if early_exit:
    break

  #extend_grid = "."
  if ([curr_x, ROW_Y] not in beacons):
    if (len(curr_dist)):
      prev_curr_dist = curr_dist.copy()
    curr_dist = []

    for idx, s in enumerate(sensors):
      x = s[0]
      y = s[1]

      curr_d = abs(x - curr_x) + abs(y - ROW_Y)
      curr_dist.append(curr_d)

    for idx, d in enumerate(dist):
      if (curr_dist[idx] <= d):
        num_empty += 1
        #extend_grid = "#"
        break

    # if all distances monotonically increased, stop
    if (len(prev_curr_dist)):
      for idx, curr_d in enumerate(curr_dist):
        if (prev_curr_dist[idx] < curr_d) and (prev_curr_dist[idx] > dist[idx]):
          early_exit = 1
        else:
          early_exit = 0
          break
    
    # DEBUG
    #if (curr_x == -2) or (curr_x == 14):
    #  print(f'DEBUG: curr_dist = {curr_dist}')
    #  print(f'DEBUG: dist = {dist}')

  #if (curr_x >= -2) and (curr_x <= max_x):
  #  print(extend_grid, end="")

  curr_x += 1
  print(f'{num_empty}, curr_x = {curr_x}')

# part 2
all_bounds = []
for idx, s, in enumerate(sensors):
  bounds = get_bounds(s, dist[idx])
  all_bounds.append(bounds)

min_distress_x = 0
min_distress_y = 0
if input_file == 'dec15_sample.txt':
  max_distress_x = 20
  max_distress_y = 20
else:  
  print("real input")
  max_distress_x = 4000000
  max_distress_y = 4000000
# find coordinates that differ by only 2, inside them lies the beacon
candidate_x_set = set() 
candidate_y_set = set() 
candidate_set = set()
for idx, bounds in enumerate(all_bounds):
  #print(f'all_bounds: {idx+1}/{len(all_bounds)}')

  for idx_curr_b, curr_b in enumerate(bounds):
    #print(f'  bounds: {idx_curr_b+1}/{len(bounds)}')

    x = curr_b[0]
    y = curr_b[1]

    if (idx_curr_b == 0):
      line1_idx = 3
    else:
      line1_idx = idx_curr_b - 1

    if (idx_curr_b == 3):
      line2_idx = 0
    else:
      line2_idx = idx_curr_b - 1

    # check what direction is the current bound
    left  = 0
    up    = 0
    right = 0
    down  = 0
    if (idx_curr_b == 0):   # left
      left = 1
    elif (idx_curr_b == 1): # up
      up = 1
    elif (idx_curr_b == 2): # right
      right = 1
    elif (idx_curr_b == 3): # down
      down = 1
    line1 = ((x, y), (bounds[line1_idx][0], bounds[line1_idx][1]))
    line2 = ((x, y), (bounds[line2_idx][0], bounds[line2_idx][1]))

    for idx_other_bounds, other_bounds in enumerate(all_bounds):
      if (idx_other_bounds == idx):
        continue
      else:
        for idx_other_b, other_b in enumerate(other_bounds):
          other_x = other_b[0]
          other_y = other_b[1]

          diff_x = abs(x - other_x)
          diff_y = abs(y - other_y)

          if (idx_other_b == 0):
            other_line1_idx = 3
          else:
            other_line1_idx = idx_other_b - 1

          if (idx_other_b == 3):
            other_line2_idx = 0
          else:
            other_line2_idx = idx_other_b - 1

          other_line1 = ((other_x, other_y), (other_bounds[other_line1_idx][0], other_bounds[other_line1_idx][1]))
          other_line2 = ((other_x, other_y), (other_bounds[other_line2_idx][0], other_bounds[other_line2_idx][1]))

          if (left):
            if (idx_other_b == 0):   # left
              # check intersections
              candidates = get_intersections(line1, line2, other_line1, other_line2)
            elif (idx_other_b == 1): # up
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
            elif (idx_other_b == 2): # right
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)
            elif (idx_other_b == 3): # down
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
          elif (up):
            if (idx_other_b == 0):   # left
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
            elif (idx_other_b == 1): # up
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)
            elif (idx_other_b == 2): # right
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
            elif (idx_other_b == 3): # down
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)
          elif (right):
            if (idx_other_b == 0):   # left
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)
            elif (idx_other_b == 1): # up
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
            elif (idx_other_b == 2): # right
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)
            elif (idx_other_b == 3): # down
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
          elif (down):
            if (idx_other_b == 0):   # left
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
            elif (idx_other_b == 1): # up
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)
            elif (idx_other_b == 2): # right
              if (diff_x == 1) and (diff_y == 1):
                print("CONSIDER!")
            elif (idx_other_b == 3): # down
              # check intersections 
              candidates = get_intersections(line1, line2, other_line1, other_line2)

          for c in candidates:
            c_x = c[0]
            c_y = c[1]
            if (c_x >= min_distress_x) and (c_x <= max_distress_x):
              candidate_x_set.add(c[0])
            if (c_y >= min_distress_y) and (c_y <= max_distress_y):
              candidate_y_set.add(c[1])
            #if (c_x >= min_distress_x) and (c_x <= max_distress_x) and (c_y >= min_distress_y) and (c_y <= max_distress_y):
            #  candidate_set.add((c_x, c_y))

    # FIRST ATTEMPT, ASSUMED THAT BOUNDED REGION IS A CROSS
    '''
    #if (x >= min_distress_x) and (x <= max_distress_x) and (y >= min_distress_y) and (y <= max_distress_y):
    for idx_other_bounds, other_bounds in enumerate(all_bounds):
      if (idx == idx_other_bounds):
        continue
      else:
        for idx_other_b, other_b in enumerate(other_bounds):
          other_x = other_b[0]
          other_y = other_b[1]

          diff_x = abs(x - other_x)  
          diff_y = abs(y - other_y)
        
          if (diff_x <= 20):
            #c_x = min(x, other_x) + 1
            #if (c_x >= min_distress_x) and (c_x <= max_distress_x):
            #  candidate_x_set.add(c_x)
            for c_x in range(min(x, other_x)+1, max(x, other_x)+2):
              if (c_x >= min_distress_x) and (c_x <= max_distress_x):
                candidate_x_set.add(c_x)
          if (diff_y <= 20):
            #c_y = min(y, other_y) + 1
            #if (c_y >= min_distress_y) and (c_y <= max_distress_y):
            #  candidate_y_set.add(c_y)
            for c_y in range(min(y, other_y)+1, max(y, other_y)+1):
              if (c_y >= min_distress_y) and (c_y <= max_distress_y):
                candidate_y_set.add(c_y)
    '''

'''
# trial optimized version
for c in candidate_set:
  c_x = c[0]
  c_y = c[1]
  for idx, s in enumerate(sensors):
    x = s[0]
    y = s[1]

    c_d = abs(x - c_x) + abs(y - c_y)

    if (c_d <= dist[idx]):
      not_candidate = 1
      break

  if not (not_candidate):
    distress_x = c_x
    distress_y = c_y
    print(f'Found from candidate_set: {c_x}, {c_y}')
'''

# test all candidate combinations if they can have a beacon
for c_x in candidate_x_set:
  early_exit = 0
  for c_y in candidate_y_set:
    not_candidate = 0
    for idx, s in enumerate(sensors):
      x = s[0]
      y = s[1]
  
      c_d = abs(x - c_x) + abs(y - c_y)
  
      if (c_d <= dist[idx]):
        not_candidate = 1
        break
  
    if not (not_candidate):
      distress_x = c_x
      distress_y = c_y
      print(f'Found: {c_x}, {c_y}')
      early_exit = 1

  if early_exit:
    break

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint()

# print answer
ans1 = num_empty
ans2 = distress_x*4000000 + distress_y
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
