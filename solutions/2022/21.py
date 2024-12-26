import pprint
import sys

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def get_root(monkeys, humn):
  monkeys["humn"] = str(humn)

  root_available = 0
  while root_available == 0:
    #print(num)
    num = 0
    for m in monkeys:
      try:
        val = eval(monkeys[m])
        monkeys[m] = str(val)
        exec(m + " = " + str(val))
        if m == 'root':
          root_available = 1
          break
        num += 1
      except:
        continue

  return float(monkeys["root"])

# initialize variables
input_file = "../../inputs/2022/input21.txt"
#input_file = "example21.txt"

monkeys = {}
# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(": ")

    # process
    monkeys[parsed_line[0]] = parsed_line[1]
    exec(parsed_line[0] + " = None")

    # read next line
    txtfile_line = txtfile.readline() 

#print(monkeys)
PART1 = 0
if (PART1):
  root_available = 0
  while root_available == 0:
    #print(num)
    num = 0
    for m in monkeys:
      try:
        val = eval(monkeys[m])
        monkeys[m] = str(val)
        exec(m + " = " + str(val))
        if m == 'root':
          root_available = 1
        num += 1
      except:
        continue
else:
  # make root operation difference
  root_operations = monkeys["root"].split(" ")
  monkeys["root"] = f'{root_operations[0]} - {root_operations[2]}'

  # trial and error initial values
  max_humn = 10000000000000
  min_humn = 1000000000000
  max_root = int(get_root(monkeys.copy(), min_humn)) # should be positive
  min_root = int(get_root(monkeys.copy(), max_humn)) # should be negative

  # binary search
  mid_root = max_root
  while mid_root != 0:
    mid_humn = (max_humn + min_humn)//2
    mid_root = int(get_root(monkeys.copy(), mid_humn))
    print(f'Using humn = {mid_humn}, root = {mid_root}')

    if mid_root > 0 and mid_root < max_root:
      max_root = mid_root
      min_humn = mid_humn
    elif mid_root < 0 and mid_root > min_root:
      min_root = mid_root
      max_humn = mid_humn

# print answer
ans1 = root
ans2 = mid_humn
print(f'First star: {ans1}')
print(f'Second star: {ans2}')
