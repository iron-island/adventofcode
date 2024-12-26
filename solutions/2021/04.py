# initialize variables

# 100 boards
total = 100
boards = [[[ 0 for col in range(5)] for row in range(5)] for b in range(total)]
marked = [[[ 0 for col in range(5)] for row in range(5)] for b in range(total)]
b = 0

# read input file
with open('../../inputs/2021/input04.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  # get inputs
  inputs = txtfile_line.split(",")
  inputs_num = [int(i) for i in inputs]

  blank = txtfile.readline()
  while txtfile_line:
    # get board
    for row in range(5):
      txtfile_line = txtfile.readline()
      num = txtfile_line.split()
      for col in range(5):
        boards[b][row][col] = int(num[col])

    b = b + 1

    # list comprehension
    # [(i-1) for i in mylist if (i == 0)]

    # process

    # read next line
    txtfile_line = txtfile.readline() 

win = total
n = 0
b = 0
num_wins = 0
won_boards = [0 for b in range(total)]
last_win = total
for num in inputs_num:
  win = total

  # copy marked
  prev_marked = list(marked)

  # mark boards
  for b in range(total):
    for row in range(5):
      for col in range(5):
        if (num == boards[b][row][col]):
          marked[b][row][col] = 1


  num_wins = 0
  for b in range(total):
    # skip if already won previously
    if (won_boards[b] == 0):
      # check row win
      for row in range(5):
        col_count = 0
        for col in range(5):
          if (marked[b][row][col]):
            col_count = col_count + 1

        if (col_count == 5):
          break

      if (col_count == 5):
        win = b
        #break
        won_boards[b] = 1

      # check row win
      for col in range(5):
        row_count = 0
        for row in range(5):
          if (marked[b][row][col]):
            row_count = row_count + 1

        if (row_count == 5):
          break

      if (row_count == 5):
        win = b
        #break
        won_boards[b] = 1

    if (won_boards[b]):
      num_wins = num_wins + 1

  # find last to win
  if (win < total):
    print("num_wins = %d" % num_wins)

    if (num_wins == total):
      last_in = num
      last_win = win
      print("total = %d" % (total))
      print("last_in = %d" % (last_in))
      print("last_win = %d" % (last_win))
      break

  # find first to win
  #if (win < total):
  #  last_in = num
  #  print("last_in = %d" % (last_in))
  #  print("win = %d" % (win))
  #  break

  n = n + 1

# calculate score
unmarked = 0
print(len(prev_marked))
print(last_win)
for row in range(5):
  for col in range(5):
    if (prev_marked[last_win][row][col] == 0):
      unmarked = unmarked + boards[last_win][row][col]
print("unmarked = %d" % unmarked)

score = unmarked*last_in
#print("First star: %d" % (score))
print("Second star: %d" % (score))
