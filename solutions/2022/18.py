import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def get_surface_area(cubes):
  # compute projections from different views
  flat_x = set()
  flat_y = set()
  flat_z = set()
  
  cube_flat_x = set()
  cube_flat_y = set()
  cube_flat_z = set()

  surface_area = 0
  
  for c in cubes:
    x = c[0]
    y = c[1]
    z = c[2]
  
    if ((x, y) not in flat_z):
      surface_area += 2
      flat_z.add((x, y))
    elif (((x, y, z+1) in cube_flat_z) and ((x, y, z-1) not in cube_flat_z)) or \
         (((x, y, z-1) in cube_flat_z) and ((x, y, z+1) not in cube_flat_z)):
      surface_area += 0
    elif (((x, y, z+1) in cube_flat_z) and ((x, y, z-1) in cube_flat_z)):
      surface_area -= 2
    else:
      surface_area += 2
    cube_flat_z.add(c)
  
    if ((y, z) not in flat_x):
      surface_area += 2
      flat_x.add((y, z))
    elif (((x+1, y, z) in cube_flat_x) and ((x-1, y, z) not in cube_flat_x)) or \
         (((x-1, y, z) in cube_flat_x) and ((x+1, y, z) not in cube_flat_x)):
      surface_area += 0
    elif (((x+1, y, z) in cube_flat_x) and ((x-1, y, z) in cube_flat_x)):
      surface_area -= 2
    else:
      surface_area += 2
    cube_flat_x.add(c)
  
    if ((x, z) not in flat_y):
      surface_area += 2
      flat_y.add((x, z))
    elif (((x, y+1, z) in cube_flat_y) and ((x, y-1, z) not in cube_flat_y)) or \
         (((x, y-1, z) in cube_flat_y) and ((x, y+1, z) not in cube_flat_y)):
      surface_area += 0
    elif (((x, y+1, z) in cube_flat_y) and ((x, y-1, z) in cube_flat_y)):
      surface_area -= 2
    else:
      surface_area += 2
    cube_flat_y.add(c)

  return surface_area

# initialize variables
input_file = "../../inputs/2022/input18.txt"
#input_file = "example18.txt"

cubes = set()

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(",")
    cube_tuple = (int(parsed_line[0]),
                  int(parsed_line[1]),
                  int(parsed_line[2]))
    cubes.add(cube_tuple)

    # read next line
    txtfile_line = txtfile.readline() 

interior_area = 0
min_x = 100000
min_y = 100000
min_z = 100000
max_x = -100000
max_y = -100000
max_z = -100000

# get boundaries of the cubes
for c in cubes:
  x = c[0]
  y = c[1]
  z = c[2]

  min_x = min(x, min_x)
  min_y = min(y, min_y)
  min_z = min(z, min_z)

  max_x = max(x, max_x)
  max_y = max(y, max_y)
  max_z = max(z, max_z)

print(f'x: {min_x} - {max_x}')
print(f'y: {min_y} - {max_y}')
print(f'z: {min_z} - {max_z}')

# INCORRECT SOLUTIONS, DOES NOT TAKE INTO ACCOUNT INDIVIDUAL BLOBS
# check surface cubes brute force #########################################################
OLD_SOLUTIONS = 0
if (OLD_SOLUTIONS):
  
  min_flat_x = set()
  min_flat_y = set()
  min_flat_z = set()
  
  min_cube_flat_x = {} 
  min_cube_flat_y = {} 
  min_cube_flat_z = {} 
  
  # positive z view
  for z in range(min_z, max_z+1):
    for y in range(min_y, max_y+1):
      for x in range(min_x, max_x+1):
        c = (x, y, z)
  
        if c in cubes:
          if (x, y) not in min_flat_z:
            min_flat_z.add((x, y))
            min_cube_flat_z[(x, y)] = z
  
          if (x, z) not in min_flat_y:
            min_flat_y.add((x, z))
            min_cube_flat_y[(x, z)] = y
  
          if (y, z) not in min_flat_x:
            min_flat_x.add((y, z))
            min_cube_flat_x[(y, z)] = x
  
  max_flat_x = set()
  max_flat_y = set()
  max_flat_z = set()
  
  max_cube_flat_x = {}
  max_cube_flat_y = {} 
  max_cube_flat_z = {} 
  
  # negative z view
  for z in range(max_z, min_z-1, -1):
    for y in range(max_y, min_y-1, -1):
      for x in range(max_x, min_x-1, -1):
        c = (x, y, z)
  
        if c in cubes:
          if (x, y) not in max_flat_z:
            max_flat_z.add((x, y))
            max_cube_flat_z[(x, y)] = z
  
          if (x, z) not in max_flat_y:
            max_flat_y.add((x, z))
            max_cube_flat_y[(x, z)] = y
  
          if (y, z) not in max_flat_x:
            max_flat_x.add((y, z))
            max_cube_flat_x[(y, z)] = x
  
  # check empty, interior cubes ##############################################################
  
  outside_cubes = set()
  empty_cubes = set()
  
  for z in range(min_z, max_z+1):
    for y in range(min_y, max_y+1):
      for x in range(min_x, max_x+1):
        c = (x, y, z)
        if (c in cubes):
          continue
  
        # empty but might still be exterior so check if really interior
        if ((x, y) not in min_cube_flat_z) or ((x, y) not in max_cube_flat_z) or (z <= min_cube_flat_z[(x, y)]) or (z >= max_cube_flat_z[(x, y)]) or \
           ((x, z) not in min_cube_flat_y) or ((x, z) not in max_cube_flat_y) or (y <= min_cube_flat_y[(x, z)]) or (y >= max_cube_flat_y[(x, z)]) or \
           ((y, z) not in min_cube_flat_x) or ((y, z) not in max_cube_flat_x) or (x <= min_cube_flat_x[(y, z)]) or (x >= max_cube_flat_x[(y, z)]):
          outside_cubes.add(c)
          continue
        else:
          empty_cubes.add(c)
  
        if ((x-1, y, z) in cubes):
          interior_area += 1
        if ((x+1, y, z) in cubes):
          interior_area += 1
        if ((x, y-1, z) in cubes):
          interior_area += 1
        if ((x, y+1, z) in cubes):
          interior_area += 1
        if ((x, y, z-1) in cubes):
          interior_area += 1
        if ((x, y, z+1) in cubes):
          interior_area += 1
  
  # compute exterior area based on surface cubes
  surface_cubes = set()
  
  for c_key in min_cube_flat_z:
    surface_cubes.add((c_key[0], c_key[1], min_cube_flat_z[c_key]))
  for c_key in max_cube_flat_z:
    surface_cubes.add((c_key[0], c_key[1], max_cube_flat_z[c_key]))
  
  for c_key in min_cube_flat_y:
    surface_cubes.add((c_key[0], min_cube_flat_y[c_key], c_key[1]))
  for c_key in max_cube_flat_y:
    surface_cubes.add((c_key[0], max_cube_flat_y[c_key], c_key[1]))
  
  for c_key in min_cube_flat_x:
    surface_cubes.add((min_cube_flat_x[c_key], c_key[0], c_key[1]))
  for c_key in max_cube_flat_x:
    surface_cubes.add((max_cube_flat_x[c_key], c_key[0], c_key[1]))
  
  exterior_surface_area = 0
  outside_cubes_internal_area = 0
  filled_cubes = cubes | empty_cubes
  for c in surface_cubes:
    x, y, z = c
  
    if ((x-1, y, z) not in filled_cubes):
      exterior_surface_area += 1
    if ((x+1, y, z) not in filled_cubes):
      exterior_surface_area += 1
    if ((x, y-1, z) not in filled_cubes):
      exterior_surface_area += 1
    if ((x, y+1, z) not in filled_cubes):
      exterior_surface_area += 1
    if ((x, y, z-1) not in filled_cubes):
      exterior_surface_area += 1
    if ((x, y, z+1) not in filled_cubes):
      exterior_surface_area += 1
  
    if ((x-1, y, z) in outside_cubes):
      outside_cubes_internal_area += 1
    if ((x+1, y, z) in outside_cubes):
      outside_cubes_internal_area += 1
    if ((x, y-1, z) in outside_cubes):
      outside_cubes_internal_area += 1
    if ((x, y+1, z) in outside_cubes):
      outside_cubes_internal_area += 1
    if ((x, y, z-1) in outside_cubes):
      outside_cubes_internal_area += 1
    if ((x, y, z+1) in outside_cubes):
      outside_cubes_internal_area += 1
  
  print(f'INCORRECT SOLUTIONS: DID NOT TAKE INTO ACCOUNT INDIVIDUAL BLOBS')
  print(f'Total cubes: {len(cubes)}')
  print(f'Empty cubes: {len(empty_cubes)}')
  print(f'Outside cubes: {len(outside_cubes)}')
  print(f'Intersection of cubes and empty cubes: {len(cubes & empty_cubes)}')
  print(f'Union of cubes and empty cubes: {len(cubes | empty_cubes)}')
  print(f'Union of all sets: {len(cubes | empty_cubes | outside_cubes)}')
  
  #pretty_print = pprint.PrettyPrinter()
  #pretty_print.pprint()
  
  # print answer
  surface_area = get_surface_area(cubes)
  exterior_area = get_surface_area(cubes | empty_cubes)
  surface_area_empty_cubes = get_surface_area(empty_cubes)
  projection_area = len(min_flat_x) + len(min_flat_y) + len(min_flat_z) + len(max_flat_x) + len(max_flat_y) + len(max_flat_z)
  
  outside_cubes_area = get_surface_area(outside_cubes)
  width = max_x - min_x + 1
  length = max_y - min_y + 1
  height = max_z - min_z + 1
  faces_area = 2*(width*length + width*height + length*height)
  print(f'{faces_area}')
  print("")
  print("INTERIOR AREA COMPUTATIONS:")
  print(f'Interior area: {interior_area}')
  print(f'get_surface_area(empty_cubes): {get_surface_area(empty_cubes)}')
  print(f'surface_area - get_surface_area(cubes | empty_cubes): {surface_area - exterior_area}')
  print("")
  print("EXTERIOR AREA COMPUTATIONS:")
  print(f'get_surface_area(cubes | empty_cubes): {exterior_area}')
  print(f'surface_area - interior area: {surface_area - interior_area}')
  print(f'surface_area - get_surface_area(empty_cubes: {surface_area - surface_area_empty_cubes})')
  print(f'exterior_surface_area: {exterior_surface_area}')
  print(f'projection area: {projection_area}')
  print(f'outside_cubes_area - face area: {outside_cubes_area - faces_area}')
  print(f'outside_cubes_internal_area: {outside_cubes_internal_area}')

# WHAT IF THERE ARE BLOBS

# BFS to fill in outside area with cubes, then compute the surface area based on the filling cubes
filler_cubes = set()
queue = []
queue.append((min_x-1, min_y-1, min_z-1))
visited = set()
while len(queue):
  x, y, z = queue[0]

  if ((x, y, z) not in cubes) and ((x, y, z) not in visited):
    filler_cubes.add((x, y, z))

    if (x > min_x-1) and (x-1, y, z) not in cubes:
      queue.append((x-1, y, z))
    if (x < max_x+1) and (x+1, y, z) not in cubes:
      queue.append((x+1, y, z))

    if (y > min_y-1) and (x, y-1, z) not in cubes:
      queue.append((x, y-1, z))
    if (y < max_y+1) and (x, y+1, z) not in cubes:
      queue.append((x, y+1, z))

    if (z > min_z-1) and (x, y, z-1) not in cubes:
      queue.append((x, y, z-1))
    if (z < max_z+1) and (x, y, z+1) not in cubes:
      queue.append((x, y, z+1))

  visited.add((x, y, z))
  queue.pop(0)

filled_width = (max_x+1) - (min_x-1) + 1
filled_length = (max_y+1) - (min_y-1) + 1
filled_height = (max_z+1) - (min_z-1) + 1
ans2 = get_surface_area(filler_cubes) - 2*(filled_width*filled_length + filled_width*filled_height + filled_length*filled_height)

print("CORRECT ANSWERS (TAKES INTO ACCOUNT INDIVIDUAL BLOBS)")
ans1 = get_surface_area(cubes)
print(f'First star: {ans1}')
print(f'Second star: {ans2}')
