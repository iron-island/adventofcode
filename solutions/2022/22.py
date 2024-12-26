
def print_board(board, visited, max_x, max_y):
  for y in range(1, max_y+1):
    for x in range(1, max_x+1):
      coordinates = complex(x, y)

      if coordinates in board:
        if (coordinates in visited) and (board[coordinates] == '.'):
          print(visited[coordinates], end="")
        else:
          print(board[coordinates], end="")
      else:
        print(" ", end="")

    print("")

def get_unit_move(curr_dir):
  # determine direction to move
  if (curr_dir == 0): # right
    unit_move = complex(1, 0)
  elif (curr_dir == 1): # down
    unit_move = complex(0, 1)
  elif (curr_dir == 2): # left
    unit_move = complex(-1, 0)
  elif (curr_dir == 3): # up
    unit_move = complex(0, -1)

  return unit_move
  
# initialize variables
input_file = "../../inputs/2022/input22.txt"
#input_file = "example22.txt"

DEBUG = 0
TEST  = 0
PART1 = 0

get_moves = 0
get_curr = 1
moves = []
board = {}
row_wrap = {}
col_wrap = {}
min_x = None
max_x = 0
min_y = None
max_y = 0
directions = [0, 1, 2, 3] # right, down, left, up
directions_print = ['>', 'v', '<', '^']
rowdir_wrap = {}

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  row = 1
  while txtfile_line:
    # parse
    # don't strip() since this will remove the leading whitespaces
    txtfile_line = txtfile_line[:-1]

    if (get_moves):
      get_moves = 0
      # convert moves to integers and directions
      buf = ''
      for t in txtfile_line:
        if (t == 'R') or (t == 'L'):
          moves.append(int(buf))
          moves.append(t)
          buf = ''
        else:
          buf = buf + t
    elif (txtfile_line == ""):
      get_moves = 1
      max_y = row-1
    else:
      for idx, t in enumerate(txtfile_line):
        if t != " ":
          # coordinates as complex numbers, x is real part, y is imaginary part
          coordinates = complex(idx+1, row)
          board[coordinates] = t
          if (get_curr):
            curr = coordinates
            get_curr = 0
          # get minimum x coordinates to be used for precomputing row wraparounds for PART1
          if (min_x == None):
            min_x = idx+1

      if PART1:
        # precompute row wraparounds, assumption is the board is continuous along each row and column
        row_wrap[complex(min_x-1, row)] = complex(len(txtfile_line), row)
        row_wrap[complex(len(txtfile_line)+1, row)] = complex(min_x, row)
      else:
        # hardcoded cube wraparounds specific to my input, will not work with sample
        if (row in range(1, 51)):
          # face 1 left edge wraps around to face 4 left edge, upside down
          row_wrap[complex(50, row)] = complex(1, 151-row)
          rowdir_wrap[complex(50, row)] = 0 # facing right

          # face 2 right edge wraps around to face 5 right edge, upside down
          row_wrap[complex(151, row)] = complex(100, 151-row)
          rowdir_wrap[complex(151, row)] = 2 # facing left
        elif (row in range(51, 101)):
          # face 3 left edge wraps around to face 4 top edge
          row_wrap[complex(50, row)] = complex(row-50, 101)
          rowdir_wrap[complex(50, row)] = 1 # facing down

          # face 3 right edge wraps around to face 2 bottom edge
          row_wrap[complex(101, row)] = complex(row+50, 50)
          rowdir_wrap[complex(101, row)] = 3 # facing up
        elif (row in range(101, 151)):
          # face 4 left edge wraps around to face 1 left edge, upside down
          row_wrap[complex(0, row)] = complex(51, 151-row)
          rowdir_wrap[complex(0, row)] = 0 # facing right

          # face 5 right edge wraps around to face 2 right edge, upside down
          row_wrap[complex(101, row)] = complex(150, 151-row)
          rowdir_wrap[complex(101, row)] = 2 # facing left
        elif (row in range(151, 201)):
          # face 6 left edge wraps around to face 1 top edge
          row_wrap[complex(0, row)] = complex(row-100, 1)
          rowdir_wrap[complex(0, row)] = 1 # facing down

          # face 6 right edge wraps around to face 5 bottom edge
          row_wrap[complex(51, row)] = complex(row-100, 150)
          rowdir_wrap[complex(51, row)] = 3 # facing up

      max_x = max(max_x, len(txtfile_line))
          
      row += 1
      min_x = None

    # read next line
    txtfile_line = txtfile.readline() 

# precompute column wraparounds
coldir_wrap = {}
if PART1:
  for x in range(1, max_x+1):
    min_y = None
    # loop up to max_y+1 to allow column wraparound
    for y in range(1, max_y+2):
      coordinates = complex(x, y)
      if (coordinates in board) and (min_y == None):
        min_y = y
      elif (coordinates not in board) and (type(min_y) is int):
        col_wrap[complex(x, min_y-1)] = complex(x, y-1)
        col_wrap[coordinates] = complex(x, min_y)
        break
else:
  # hardcoded column wraparounds specific to my input, will not work with sample
  for x in range(1, 151):
    if (x in range(1, 51)):
      # face 4 top edge wraps around to face 3 left edge
      col_wrap[complex(x, 100)] = complex(51, x+50)
      coldir_wrap[complex(x, 100)] = 0 # facing right

      # face 6 bottom edge wraps around to face 2 top edge
      col_wrap[complex(x, 201)] = complex(x+100, 1)
      coldir_wrap[complex(x, 201)] = 1 # facing down
    elif (x in range(51, 101)):
      # face 1 top edge wraps around to face 6 left edge
      col_wrap[complex(x, 0)] = complex(1, x+100)
      coldir_wrap[complex(x, 0)] = 0 # facing right

      # face 5 bottom edge wraps around to face 6 right edge 
      col_wrap[complex(x, 151)] = complex(50, x+100)
      coldir_wrap[complex(x, 151)] = 2 # facing left
    elif (x in range(101, 151)):
      # face 2 top edge wraps around to face 6 bottom edge
      col_wrap[complex(x, 0)] = complex(x-100, 200)
      coldir_wrap[complex(x, 0)] = 3 # facing up

      # face 2 bottom edge wraps around to face 3 right edge
      col_wrap[complex(x, 51)] = complex(100, x-50)
      coldir_wrap[complex(x, 51)] = 2 # facing left

# traverse board
curr_dir = 0 # right
if DEBUG and TEST:
  # debugs face 1 top edge wraparound
  curr = complex(52, 1)
  curr_dir = 3
  # debugs face 1 left edge wraparound
  curr = complex(51, 2)
  curr_dir = 2
  # debugs face 2 top edge wraparound
  curr = complex(105, 1)
  curr_dir = 3
  # debugs face 2 right edge wraparound
  curr = complex(150, 2)
  curr_dir = 0
  # debugs face 2 bottom edge wraparound
  curr = complex(105, 50)
  curr_dir = 1
  # debugs face 3 left edge wraparound
  curr = complex(51, 52)
  curr_dir = 2
  # debugs face 3 right edge wraparound
  curr = complex(100, 52)
  curr_dir = 0
  # debugs face 4 top edge wraparound
  curr = complex(2, 101)
  curr_dir = 3
  # debugs face 4 left edge wraparound
  curr = complex(1, 102)
  curr_dir = 2
  # debugs face 5 right edge wraparound
  curr = complex(100, 102)
  curr_dir = 0
  # debugs face 5 bottom edge wraparound
  curr = complex(52, 150)
  curr_dir = 1
  # debugs face 6 left edge wraparound
  curr = complex(1, 152)
  curr_dir = 2
  # debugs face 6 right edge wraparound
  curr = complex(50, 152)
  curr_dir = 0
  # debugs face 6 bottom edge wraparound
  curr = complex(5, 200)
  curr_dir = 1

  moves = [5]
visited = {}
visited[curr] = directions_print[curr_dir]

if DEBUG and TEST:
  print(moves)
  print(visited)

for m in moves:
  if (type(m) is int):
    # determine direction to move
    unit_move = get_unit_move(curr_dir)

    # attempt to move 1 unit at a time
    for u in range(1, m+1):
      next_dir = curr_dir
      next_coord = curr + unit_move

      # check for wrap around first
      if ((curr_dir == 0) or (curr_dir == 2)) and (next_coord in row_wrap):
        # update next direction first before updating next coordinate
        if (next_coord in rowdir_wrap): # applicable only to PART2
          next_dir = rowdir_wrap[next_coord]

        next_coord = row_wrap[next_coord]
      elif (next_coord in col_wrap):
        # update next direction first before updating next coordinate
        if (next_coord in coldir_wrap): # applicable only to PART2
          next_dir = coldir_wrap[next_coord]

        next_coord = col_wrap[next_coord]
      if (next_coord in board):
        if (board[next_coord] == '.'):
          curr = next_coord
          curr_dir = next_dir
          unit_move = get_unit_move(curr_dir)

          # for debugging
          if DEBUG:
            visited[curr] = directions_print[curr_dir]
        else:
          # stopped by wall
          break
  else:
    # rotate
    if (m == 'R'): # clockwise
      curr_dir = directions[(curr_dir + 1) % 4]
    elif (m == 'L'): # counter-clockwise
      curr_dir = directions[(curr_dir - 1) % 4]

    # for debugging
    if DEBUG:
      visited[curr] = directions_print[curr_dir]

print_board(board, visited, max_x, max_y)

# print answer
password = int(1000*curr.imag + 4*curr.real + curr_dir)
ans1 = password
ans2 = password
print(f'First star: {ans1}')
print(f'Second star: {ans2}')
