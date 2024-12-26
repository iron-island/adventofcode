import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
input_file = "../../inputs/2022/input13_modified.txt"
#input_file = "example13.txt"

inputs = []

def check_order_v2(l, r, not_order=None, debug=""):
  if (not_order == 1):
    return 1
  elif (not_order == 0):
    return 0

  print(f'{debug}Compare {l} vs {r}')

  if (type(l) is int) and (type(r) is int):
    # if they are equal, not_order will still be None
    if (l < r):
      return 0
    elif (l > r):
      return 1
  elif (type(l) is list) and (type(r) is list):
    if (len(r) < len(l)):
      #l_ints = 0
      #r_ints = 0
      #for i in l:
      #  if (type(i) is int):
      #    l_ints += 1
      #for i in r:
      #  if (type(i) is int):
      #    r_ints += 1

      #if (l_ints == len(l)) and (r_ints == len(r)):
      #  print(f'{debug}List comparison path taken!')
      #  return (not (l < r))
      #else:

      for idx_r_item, r_item in enumerate(r):
        not_order = check_order_v2(l[idx_r_item], r_item, not_order, debug + "  ")

        if (not_order):
          return 1
      
      # if right ran out of items while no decision was made, 
      #   considered as not ordered
      if (not_order == None):
        return 1
      else:
        return not_order
    else:
      for idx_l_item, l_item in enumerate(l):
        not_order = check_order_v2(l_item, r[idx_l_item], not_order, debug + "  ") 
      
        if (not_order):
          return 1

      # if left ran out of items while no decision was made,
      #   considered as ordered
      if (len(l) < len(r)):
        print(f'{debug}Left ran out! Pair is ordered')
        return 0
  elif (type(l) is int) and (type(r) is list):
    return check_order_v2([l], r, not_order, debug + "  ")
  elif (type(l) is list) and (type(r) is int):
    return check_order_v2(l, [r], not_order, debug + "  ")

  return not_order

def check_order(l, r, debug=0, continue_check=1):
  not_order = 0

  if (type(l) is int) and (type(r) is int):
    if (debug):
      print(f'Int compare {l} vs {r}')

    if (l < r):
      return 0, 0
    elif (l == r):
      return 0, 1
    else:
      return 1, 0
  elif (type(l) is list) and (type(r) is list):
    if (debug):
      print(f'Compare {l} vs {r}')

    l_items_int = 1
    r_items_int = 1
    for items in l:
      if not (type(items) is int):
        l_items_int = 0
    for items in r:
      if not (type(items) is int):
        r_items_int = 0

    if (len(l) > 0) and (len(r) > 0) and l_items_int and r_items_int:
      if (l < r):
        return 0, 0
      elif (l == r):
        return 0, 1
      else:
        return 1, 0
    else: # brute force
      if (len(r) == 0):
        return 1, 0
      elif (len(l) == 0):
        return 0, 0

    # recursion
    for idx_l_item, l_item in enumerate(l):
      if (debug):
        print(f'Trying compare {l_item} vs {r} index {idx_l_item} with not_order = {not_order}')
      try:
        not_order, continue_check = check_order(l_item, r[idx_l_item],debug)
        
        if not_order:
          if (debug):
            print(f'Compare {l[idx_l_item]} vs {r[idx_l_item]}: not in order')
          return 1, 0
      except IndexError as e:
        if (debug):
          print(f'Exception {e} occurred, trying index {idx_l_item} on {r}, returning 1')
        #return 1, 0

        if (continue_check):
          return 0, 1
        else:
          return 1, 0
  elif (type(l) is int) and (type(r) is list):
    not_order, continue_check = check_order([l], r)
  elif (type(l) is list) and (type(r) is int):
    if (debug):
      print(f'Compare {l} vs {[r]} (made right a list)')

    not_order, continue_check = check_order(l, [r], debug)

  return not_order, continue_check

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    #parsed_line = txtfile_line.split(" ")

    # process
    if (txtfile_line == ""):
      inputs.append({})
    else:
      if (inputs[-1].get("left") == None):
        inputs[-1]["left"] = eval(txtfile_line)
      else:
        inputs[-1]["right"] = eval(txtfile_line)

    # read next line
    txtfile_line = txtfile.readline() 

divider = []
divider.append([[2]])
divider.append([[6]])

sum_idx = 0
not_order = 0
continue_check = 1
idx_list = []
sum_divider_0 = 0
sum_divider_1 = 0
for idx, i in enumerate(inputs):
  left = i["left"]
  right = i["right"]

  if (idx == 1):
    debug = 1
  else:
    debug = 0

  print(f'======= Pair {idx+1} ======= ')

  # part 1
  #not_order = check_order_v2(left, right, None)

  #if (not_order == 0):
  #  print(idx+1)
  #  idx_list.append(idx+1)
  #  sum_idx = sum_idx + idx + 1

  # part 2
  divider_bigger = 0
  divider_bigger = check_order_v2(divider[0], left, None)
  if (divider_bigger):
    sum_divider_0 += 1
  divider_bigger = check_order_v2(divider[0], right, None)
  if (divider_bigger):
    sum_divider_0 += 1

  divider_bigger = check_order_v2(divider[1], left, None)
  if (divider_bigger):
    sum_divider_1 += 1
  divider_bigger = check_order_v2(divider[1], right, None)
  if (divider_bigger):
    sum_divider_1 += 1
 
# queue
#myqueue = []
#myqueue.append('a')
#myqueue.append('b')
#myqueue.append('c')
#myqueue # ['a', 'b', 'c']
#myqueue.pop(0) # ['b', 'c']
#myqueue.index('c') # 1
#myqueue.pop(1) # ['b']

pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint()

# print answer
ans1 = sum_idx
ans2 = (sum_divider_0 + 1)*(sum_divider_1 + 2)
print(sum_divider_0)
print(sum_divider_1)
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
