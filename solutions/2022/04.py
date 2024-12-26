import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def gen_list(sections):
  parsed_sections = sections.split("-")
  start_sec = int(parsed_sections[0])
  end_sec = int(parsed_sections[1])

  section_list = []
  for i in range(start_sec, end_sec + 1):
    section_list.append(i)

  return section_list

# initialize variables
input_file = "../../inputs/2022/input04.txt"

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  redundant = 0
  while txtfile_line:
    # parse
    #parsed_line = txtfile_line.split(" ")
    # remove new line at the end
    txtfile_line = txtfile_line[:-1]
    parsed_line = txtfile_line.split(",")

    first_section_list = gen_list(parsed_line[0])
    second_section_list = gen_list(parsed_line[1])

    # process
    common = list(set(first_section_list) & set(second_section_list))

    #if (len(common) == len(first_section_list)) or (len(common) == len(second_section_list)):
    #  redundant = redundant + 1
    if (len(common)):
      redundant = redundant + 1

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
ans1 = redundant
ans2 = 0
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
