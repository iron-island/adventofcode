import sys
import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def print_elves(elves):
  min_x = 1000000
  min_y = 1000000
  max_x = -1000000
  max_y = -1000000
  for elf in elves:
    x = elf.real
    y = elf.imag
  
    min_x = int(min(x, min_x))
    min_y = int(min(y, min_y))
  
    max_x = int(max(x, max_x))
    max_y = int(max(y, max_y))
    
  for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
      coordinates = complex(x, y)
      if coordinates in elves:
        print("#", end="")
      else:
        print(".", end="")

    print("")

# initialize variables
input_file = "../../inputs/2022/input23.txt"
#input_file = "example23.txt"

elves = set()
# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()
  
  row = 0
  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()

    for idx, t in enumerate(txtfile_line):
      coordinates = complex(idx, row)
      if (t == '#'):
        elves.add(coordinates)

    # read next line
    txtfile_line = txtfile.readline() 
    row += 1

num_rounds = 1
dir_check = [[complex(0, -1), complex(1, -1) , complex(-1, -1)],
             [complex(0, 1) , complex(1, 1)  , complex(-1, 1) ],
             [complex(-1, 0), complex(-1, -1), complex(-1, 1) ],
             [complex(1, 0) , complex(1, -1) , complex(1, 1)  ]
            ]
for r in range(0, num_rounds):
  i = 0
  still_moving = len(elves)
  #print_elves(elves)
  while True:
    #print_elves(elves)
    #print(f'Round {r}/{num_rounds}: i = {i} for {still_moving}/{len(elves)} elves still moving')
    proposed = set()
    proposed_elf_dict = {}
    duplicates = set()
    for elf in elves:
      # first half of round
      i_check1 = (i) % 4
      i_check2 = (i+1) % 4
      i_check3 = (i+2) % 4
      i_check4 = (i+3) % 4

      elf_check1_0 = elf + dir_check[i_check1][0]
      elf_check1_1 = elf + dir_check[i_check1][1]
      elf_check1_2 = elf + dir_check[i_check1][2]

      elf_check2_0 = elf + dir_check[i_check2][0]
      elf_check2_1 = elf + dir_check[i_check2][1]
      elf_check2_2 = elf + dir_check[i_check2][2]

      elf_check3_0 = elf + dir_check[i_check3][0]
      elf_check3_1 = elf + dir_check[i_check3][1]
      elf_check3_2 = elf + dir_check[i_check3][2]

      elf_check4_0 = elf + dir_check[i_check4][0]
      elf_check4_1 = elf + dir_check[i_check4][1]
      elf_check4_2 = elf + dir_check[i_check4][2]
     
      # check adjacent positions
      if (elf_check1_0 not in elves) and \
         (elf_check1_1 not in elves) and \
         (elf_check1_2 not in elves) and \
         (elf_check2_0 not in elves) and \
         (elf_check2_1 not in elves) and \
         (elf_check2_2 not in elves) and \
         (elf_check3_0 not in elves) and \
         (elf_check3_1 not in elves) and \
         (elf_check3_2 not in elves) and \
         (elf_check4_0 not in elves) and \
         (elf_check4_1 not in elves) and \
         (elf_check4_2 not in elves):
        proposed_coordinate = elf
      elif (elf_check1_0 not in elves) and \
           (elf_check1_1 not in elves) and \
           (elf_check1_2 not in elves):
        proposed_coordinate = elf + dir_check[i_check1][0]
      elif (elf_check2_0 not in elves) and \
           (elf_check2_1 not in elves) and \
           (elf_check2_2 not in elves):
        proposed_coordinate = elf + dir_check[i_check2][0]
      elif (elf_check3_0 not in elves) and \
           (elf_check3_1 not in elves) and \
           (elf_check3_2 not in elves):
        proposed_coordinate = elf + dir_check[i_check3][0]
      elif (elf_check4_0 not in elves) and \
           (elf_check4_1 not in elves) and \
           (elf_check4_2 not in elves):
        proposed_coordinate = elf + dir_check[i_check4][0]
      else:
        proposed_coordinate = elf

      if (proposed_coordinate in proposed):
        proposed.add(proposed_elf_dict[proposed_coordinate])

        #print(f'Elf in {elf} proposing to go to {proposed_coordinate}')

        # stay put
        proposed.add(elf)

        duplicates.add(proposed_coordinate)
      else:
        proposed.add(proposed_coordinate)
        proposed_elf_dict[proposed_coordinate] = elf

    # second half of round
    # remove duplicates
    for d in duplicates:
      proposed.remove(d)

    if (proposed == elves):
      # no elf moved
      num_rounds = i+1
      break
    else:
      still_moving = len(elves) - len(elves & proposed)
      elves = proposed.copy()
      i += 1

# check largest rectangle
min_x = 1000000
min_y = 1000000
max_x = -1000000
max_y = -1000000
for elf in elves:
  x = elf.real
  y = elf.imag

  min_x = min(x, min_x)
  min_y = min(y, min_y)

  max_x = max(x, max_x)
  max_y = max(y, max_y)

#print_elves(elves)

# empty ground tiles are just the area minus the no. of elves
print(min_x)
print(min_y)
print(max_x)
print(max_y)
empty_tiles = (max_x - min_x + 1)*(max_y - min_y + 1) - len(elves)

# print answer
ans1 = int(empty_tiles)
ans2 = num_rounds
print(f'First star: {ans1}')
print(f'Second star: {ans2}')
