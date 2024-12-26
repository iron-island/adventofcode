import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def print_rocks(rocks_set, shape_coordinates=[]):
  if (len(shape_coordinates)):
    height = max(max(rocks_set)[0], max(shape_coordinates)[0])
  else:
    height = max(rocks_set)[0]

  while height >= 0:
    for i in range(0, 7):
      if ((height, i) in rocks_set):
        print("#", end="")
      elif ((height, i) in shape_coordinates):
        print("@", end="")
      else:
        print(".", end="")
    print("")
    height = height - 1
  print("xxxxxxx")
  print("")

def height_from_pattern(num_rocks, pattern_init, pattern_mod, pattern_height):
  periods = (num_rocks - pattern_init)//pattern_mod
  idx_pattern_height = (num_rocks - pattern_init) % pattern_mod

  return pattern_init_height + pattern_add*periods + pattern_height[idx_pattern_height]

# initialize variables
input_file = "../../inputs/2022/input17.txt"
#input_file = "example17.txt"

pattern = []

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()

    # process
    for t in txtfile_line:
      if (t == '>'):
        pattern.append(1)
      else:
        pattern.append(-1)

    # read next line
    txtfile_line = txtfile.readline() 

idx_p = 0
idx_s = -1
height = 0
shape = [[(0, 0), (0, 1), (0, 2), (0, 3)],
         [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
         [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
         [(0, 0), (1, 0), (2, 0), (3, 0)],
         [(0, 0), (0, 1), (1, 0), (1, 1)]
        ]
right_edge_shape = [3, 2, 2, 0, 1]
new_shape = 1
left_edge = 2
right_edge = None
rocks_set = set()
rest = 0
# fill in the floor
for c in range(0, 7):
  rocks_set.add((-1, c))

# tetris
num_rested = 0
DEBUG = 0
rocks_height_set = set()
idx_set = set()
offset = -1
print(f'length of jet pattern: {len(pattern)}')
next_pattern = 0
while (num_rested < 100000):

  idx_jet = idx_p % len(pattern)
  jet = pattern[idx_jet]

  # initialize shape
  if (new_shape):
    idx_s = (idx_s + 1) % 5

    if (next_pattern == 0) and (idx_jet, idx_s, offset) in idx_set:
      print(f'A PATTERN EMERGED AFTER {num_rested} ROCKS, HEIGHT {height}: IDX_JET {idx_jet}, IDX_S {idx_s}, OFFSET {offset}')
      next_pattern = 1
      curr_pattern = (idx_jet, idx_s, offset)

      pattern_init = num_rested
      pattern_init_height = height
    elif (next_pattern == 1) and ((idx_jet, idx_s, offset) == curr_pattern):
      print(f'A PATTERN EMERGED AFTER {num_rested} ROCKS, HEIGHT {height}: IDX_JET {idx_jet}, IDX_S {idx_s}, OFFSET {offset}')
      next_pattern = 2
      curr_pattern = (idx_jet, idx_s, offset)
      prev_num_rested = num_rested
      prev_height = height
      pattern_height = []
      pattern_height.append(0)
    elif (next_pattern == 2):
      if ((idx_jet, idx_s, offset) == curr_pattern):
        print(f'A PATTERN EMERGED AFTER {num_rested} ROCKS, HEIGHT {height}: IDX_JET {idx_jet}, IDX_S {idx_s}, OFFSET {offset}')
        pattern_mod = num_rested - prev_num_rested
        pattern_add = height - prev_height
        break
      else:
        # record heights
        pattern_height.append(height - prev_height) 
    else:
      idx_set.add((idx_jet, idx_s, offset))

    left_edge = 2
    right_edge = left_edge + right_edge_shape[idx_s]
    bottom_edge = height + 3

    shape_coordinates = shape[idx_s].copy()

    for idx_sc, sc in enumerate(shape_coordinates):
      shape_coordinates[idx_sc] = (sc[0] + bottom_edge, sc[1] + left_edge)

    if DEBUG:
      print("new rock:")  
      print_rocks(rocks_set, shape_coordinates)

  # simulate jets
  if ((jet == -1) and (left_edge > 0)) or \
     ((jet ==  1) and (right_edge < 6)):

    prev_shape_coordinates = shape_coordinates.copy()

    left_edge = 100
    right_edge = -100
    for idx_sc, sc in enumerate(shape_coordinates):
      left_edge = min(left_edge, sc[1] + jet)
      right_edge = max(right_edge, sc[1] + jet)
      shape_coordinates[idx_sc] = (sc[0], sc[1] + jet)

    # check collision
    if (len(set(shape_coordinates) & rocks_set)):
      shape_coordinates = prev_shape_coordinates.copy()

      # recompute edges
      left_edge = 100
      right_edge = -100
      for sc in shape_coordinates:
        left_edge = min(left_edge, sc[1])
        right_edge = max(right_edge, sc[1])
  else:
    prev_shape_coordinates = shape_coordinates.copy()

  if DEBUG:
    if (jet == -1):
      print(f'simulate left jet: {left_edge}, {right_edge}')
    else:
      print(f'simulate right jet: {left_edge}, {right_edge}')
    print_rocks(rocks_set, shape_coordinates)

  # simulate falling
  prev_shape_coordinates = shape_coordinates.copy()
  for idx_sc, sc in enumerate(shape_coordinates):
    shape_coordinates[idx_sc] = (sc[0] - 1, sc[1])

  if (len(set(shape_coordinates) & rocks_set)):
    rocks_set = rocks_set.union(set(prev_shape_coordinates))
    height = max(rocks_set)[0]+1
    offset = max(rocks_set)[1]
    new_shape = 1
    num_rested = num_rested + 1
    #print(num_rested)
    print(f'{num_rested} rocks: height = {height}')

    #if ((num_rested/2, height/2) in rocks_height_set) and (num_rested > 38):
    #  print(f'A PATTERN EMERGED IN {num_rested} ROCKS: HEIGHT {height}')
    #  break
    #else:
    #  rocks_height_set.add((num_rested, height))
  else:
    new_shape = 0

  if DEBUG:
    print("simulate fall:")
    print_rocks(rocks_set, shape_coordinates)

  # update
  idx_p = idx_p + 1

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint()
#print_rocks(rocks_set, shape_coordinates)

# extrapolate height based on pattern
print(f'Pattern: after {pattern_init} rocks, height will increase by {pattern_add} every {pattern_mod} rocks')
#periods = (1000000000000 - pattern_init)//pattern_mod
#idx_pattern_height = (1000000000000 - pattern_init) % pattern_mod

# print answer
ans1 = height_from_pattern(2022, pattern_init, pattern_mod, pattern_height)
ans2 = height_from_pattern(1000000000000, pattern_init, pattern_mod, pattern_height)
print(f'First star:  {ans1}')
print(f'Second star: {ans2}')
