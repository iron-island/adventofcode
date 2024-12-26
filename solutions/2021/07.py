import pprint

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(myqueue)

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables

# read input file
with open('../../inputs/2021/input07.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  # parse
  parsed_line = txtfile_line.split(",")
  x_list = [int(x) for x in parsed_line] 

num_x = len(x_list)

# find min and max
max_x = 0
min_x = 10000
for i in range(num_x):
  if (x_list[i] > max_x):
    max_x = x_list[i] 

  if (x_list[i] < min_x):
    min_x = x_list[i]

# bin x
num_bins = max_x - min_x + 1
bin_x = [0 for b in range(num_bins)]
for i in range(num_x):
  #offset
  b = x_list[i] - min_x
  bin_x[b] = bin_x[b] + 1

min_d = 100000000
# find shortest distance
for b in range(num_bins):
  d = 0
  for c in range(num_bins):
    sum_arithmetic = (c - b)*(abs(c - b) + 1)/2
    d = d + abs(bin_x[c]*sum_arithmetic)

  if (d < min_d):
    min_d = d

# print answer
print("First star: %d" % (min_d))
