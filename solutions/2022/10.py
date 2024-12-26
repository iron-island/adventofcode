import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def check_strength(cycle, x, total_strength):
  if (((cycle - 19) % 40) == 0):
    strength = x*(cycle+1)
    total_strength = total_strength + strength
    #print(f'during cycle {cycle+1}: {strength}')

  return total_strength

def render(cycle, x, crt):
  pixel = cycle % 40
  if (pixel in range(x-1, x+2)):
    y = cycle//40
    crt[y][pixel] = '#'

# initialize variables
input_file = "../../inputs/2022/input10.txt"
#input_file = "example10.txt"
#input_file = "example10_2.txt"

crt_row = []
for i in range(1, 41):
  crt_row.append('.')

crt = []
for i in range(1, 7):
  crt.append(crt_row.copy())

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  cycle = 0
  x = 1
  total_strength = 0
  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(" ")

    # process

    inst = parsed_line[0]
    if not (inst == "noop"):
      V = int(parsed_line[1])
    
      for c in range(1, 3):
        total_strength = check_strength(cycle, x, total_strength)
        render(cycle, x, crt)

        cycle = cycle + 1

        if (c == 2):
          x = x + V

        #print(f'cycle {cycle}, x = {x}')
    else:
      render(cycle, x, crt)
      total_strength = check_strength(cycle, x, total_strength)

      cycle = cycle + 1
      #print(f'cycle {cycle}, x = {x}')

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
print(f'x = {x} after {cycle} cycles')
ans1 = total_strength
ans2 = 0
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))

for r in crt:
  for p in r:
    print(p, end="")

  print("")
