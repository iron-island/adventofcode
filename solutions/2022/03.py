import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def get_priority(mychar):
  a_num = ord('a')
  A_num = ord('A')

  priority = 0
  if (ord(mychar) >= a_num):
    priority = ord(mychar) - a_num + 1
  elif (ord(mychar) >= A_num):
    priority = ord(mychar) - A_num + 27

  return priority

# initialize variables
input_file = "../../inputs/2022/input03.txt"


# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  total_priority = 0
  while txtfile_line:
    # parse
    #parsed_line = txtfile_line.split(" ")

    # process
    # 1st star
    #rucksack = txtfile_line[0:-1]
    #num_items = len(rucksack)

    #first = rucksack[0:num_items/2]
    #second = rucksack[num_items/2:]
    #common = list(set(first) & set(second))
    #priority = get_priority(common[0])

    # 2nd star
    first = txtfile_line[0:-1]
    txtfile_line = txtfile.readline()
    second = txtfile_line[0:-1]
    txtfile_line = txtfile.readline()
    third = txtfile_line[0:-1]
    badge = list(set(first) & set(second) & set(third))
    priority = get_priority(badge[0])
  
    total_priority = total_priority + priority

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
ans1 = total_priority
ans2 = total_priority
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
