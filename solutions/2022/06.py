import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
input_file = "../../inputs/2022/input06.txt"

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  character = 0
  message = 0
  while txtfile_line:
    # parse
    txtfile_line.strip()
    #parsed_line = txtfile_line.split(" ")
    for i in range(4, len(txtfile_line)):
      marker = txtfile_line[(i-4):i]
      marker_set = set(txtfile_line[(i-4):i])
      if len(marker_set) == len(marker):
        character = i
        break

    # process
    for i in range(14, len(txtfile_line)):
      marker = txtfile_line[(i-14):i]
      marker_set = set(txtfile_line[(i-14):i])
      if len(marker_set) == len(marker):
        message = i
        break

    # read next line
    txtfile_line = txtfile.readline() 

# queue
#myqueue = []
#myqueue.append('a')
#myqueue.append('b')
#myqueue.append('c')
#myqueue # ['a', 'b', 'c']
#myqueue.pop(0) # ['b', 'c']
#myqueue.index('c') # 1
#myqueue.pop(1) # ['b']

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint()

# print answer
ans1 = character
ans2 = message
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
