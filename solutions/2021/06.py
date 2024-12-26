import pprint

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(myqueue)

#def remove_all(mylist, val):
#  return [x for x in mylist if x != val]

# queue
#myqueue = []
#myqueue.append('a')
#myqueue.append('b')
#myqueue.append('c')
#myqueue # ['a', 'b', 'c']
#myqueue.pop(0) # ['b', 'c']
#myqueue.index('c') # 1
#myqueue.pop(1) # ['b']

# initialize variables
total_days = 256

# read input file
with open('../../inputs/2021/input06.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    parsed_line = txtfile_line.split(",")
    fish = [int(i) for i in parsed_line]

    # read next line
    txtfile_line = txtfile.readline() 

# process
num_fish = len(fish)
fish_bins = [0 for i in range(9)]
init_fish = [6 for i in fish]

# bin the fish
for i in range(num_fish):
  time = fish[i]
  fish_bins[time] = fish_bins[time] + 1

#print(fish_bins)

for d in range(1, total_days+1):
  num_fish = len(fish)

  for c in range(9):
      if (c == 0):
        reset_fish = fish_bins[0]
        fish_bins[0] = fish_bins[1]
      elif (c == 6):
        fish_bins[6] = fish_bins[7] + reset_fish
      elif (c == 8):
        fish_bins[8] = reset_fish
      else:
        fish_bins[c] = fish_bins[c+1]

      #if (fish[i] == 0):
      #  fish[i] = 6
      #  new_init_fish = 8
      #  fish.append(new_init_fish)
      #  init_fish.append(new_init_fish)
      #else:
      #  fish[i] = fish[i] - 1

  print("After %d days:" % d)
  print(fish_bins)
  #print(fish)

# print answer
num_fish = 0
for i in range(len(fish_bins)):
  num_fish = num_fish + fish_bins[i]
ans1 = num_fish
ans2 = 1
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
