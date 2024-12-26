import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
input_file = "../../inputs/2022/input05.txt"

stack = {}

stack["1"] = ["D", "L", "J", "R", "V", "G", "F"]
stack["2"] = ["T", "P", "M", "B", "V", "H", "J", "S"]
stack["3"] = ["V", "H", "M", "F", "D", "G", "P", "C"]
stack["4"] = ["M", "D", "P", "N", "G", "Q"]
stack["5"] = ["J", "L", "H", "N", "F"]
stack["6"] = ["N", "F", "V", "Q", "D", "G", "T", "Z"]
stack["7"] = ["F", "D", "B", "L"]
stack["8"] = ["M", "J", "B", "S", "V", "D", "N"]
stack["9"] = ["G", "L", "D"]

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  line = 1
  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    #if (line >= 1) and (line <= 9):
    if (line >= 11):
      txtfile_line = txtfile_line.split(" ")
      num_crates = int(txtfile_line[1])
      src = txtfile_line[3]
      dest = txtfile_line[5]

      #for i in range(1, num_crates+1):
      #  #idx = 0 - i
      #  #stack[dest].append(stack[src][idx])
      #  stack[src].pop(idx)
      src_stack = stack[src][0-num_crates:]
      for i in range (1, num_crates+1):
        stack[src].pop()
      for i in range(0, len(src_stack)):
        stack[dest].append(src_stack[i])
    
    # process

    # read next line
    txtfile_line = txtfile.readline() 
    line = line + 1

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
for i in range(1, 10):
  print(stack[str(i)][-1])
ans1 = 0
ans2 = 0
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
