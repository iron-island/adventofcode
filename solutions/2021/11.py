import pprint

# initialize variables
input_file = '../../inputs/2021/input11.txt'
num_x = 10
num_y = 10
max_steps = 100
energy = [[0 for i in range(num_x)] for j in range(num_y)]

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def update_energy(energy, flash, add_queue, i, j, num_flashes):
  cur_energy = energy[j][i]

  if (cur_energy == 9):
    # flash
    energy[j][i] = 0
    flash[j][i] = 1
    num_flashes = num_flashes + 1

    # add adjacent squares to queue
    up_present = j > 0
    down_present = (j < (num_y-1))
    left_present = (i > 0)
    right_present = (i < (num_x-1))

    if up_present:
      add_queue.append([j-1, i])

      if left_present:
        add_queue.append([j-1, i-1])
      if right_present:
        add_queue.append([j-1, i+1])
    if down_present:
      add_queue.append([j+1, i])

      if left_present:
        add_queue.append([j+1, i-1])
      if right_present:
        add_queue.append([j+1, i+1])
    if left_present:
      add_queue.append([j, i-1])
    if right_present:
      add_queue.append([j, i+1])
  else:
    energy[j][i] = cur_energy + 1

  return energy, flash, add_queue, num_flashes


# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  j = 0
  while txtfile_line:
    # parse
    for i in range(num_x):
      num = txtfile_line[i]
      energy[j][i] = int(num)

    # process
    j = j + 1

    # read next line
    txtfile_line = txtfile.readline() 

num_flashes = 0
sync_step = 0
n = 1
while(1):
  flash = [[0 for i in range(num_x)] for j in range (num_y)]
  add_queue = []

  for i in range(num_x):
    for j in range(num_y):
      already_flashed = flash[j][i]

      if not(already_flashed):
        energy, flash, add_queue, num_flashes = update_energy(energy, flash, add_queue, i, j, num_flashes)

  # add energy to adjecent squares
  queue_length = len(add_queue)
  while (queue_length):
    q = 0
    j = add_queue[q][0]
    i = add_queue[q][1]

    already_flashed = flash[j][i]
    if already_flashed:
      add_queue.pop(q)
    else:
      energy, flash, add_queue, num_flashes = update_energy(energy, flash, add_queue, i, j, num_flashes)
      add_queue.pop(q)

    # update queue length
    queue_length = len(add_queue)

  # check if synchronized
  flash_row = [0 for i in range(num_x)]
  if (energy.count(flash_row) == num_y):
    sync_step = n
    print(n)
    break
  n = n + 1
  print(n)

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(energy)

# print answer
print("First star: %d" % (num_flashes))
print("First star: %d" % (sync_step))
