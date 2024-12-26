import pprint

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(myqueue)

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
rules = []
ins = []
steps = 40

# read input file
with open('../../inputs/2021/input14.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  polymer = list(txtfile_line[0:-1])
  txtfile.readline() # blank
  txtfile_line = txtfile.readline()
  while txtfile_line:
    # parse
    parsed_line = txtfile_line.split(" -> ")
    rules.append(parsed_line[0])
    ins.append(parsed_line[1][0])

    # read next line
    txtfile_line = txtfile.readline() 


new_polymer = [x for x in polymer]
#for n in range(steps):
#  len_polymer = len(polymer)
#  insert_queue = []
#  idx_queue = []
#
#  for i in range(len_polymer-1):
#    a = polymer[i]
#    b = polymer[i+1]
#
#    for r in range(len(rules)):
#      a_rule = rules[r][0]
#      b_rule = rules[r][1]
#
#      if (a == a_rule) and (b == b_rule):
#        insert_queue.append(ins[r])
#        idx_queue.append(i+1)
#
#  offset = 0
#  insert_queue = [x for _, x in sorted(zip(idx_queue, insert_queue))]
#  idx_queue.sort()
#  for n in range(len(insert_queue)):
#    idx = idx_queue[n] + offset
#    polymer.insert(idx, insert_queue[n])
#    offset = offset + 1

# populate initial possible pairs
pairs = {}
pairs_count = []
letters = []
letters_count = []
for i in range(len(polymer)-1):
  a = polymer[i]
  b = polymer[i+1]

  pair = (a + b)
  if not(pair in pairs.keys()): #if (pairs.count(pair) == 0):
    #pairs.append(pair)
    #pairs_count.append(1)
    pairs[pair] = 1
  else:
    #idx = pairs.index(pair)
    #pairs_count[idx] = pairs_count[idx] + 1
    pairs[pair] = pairs[pair] + 1

  # update letters
  if (letters.count(a) == 0):
    letters.append(a)
    letters_count.append(1)
  elif (i == 0):
    idx = letters.index(a)
    letters_count[idx] = letters_count[idx] + 1

  if (letters.count(b) == 0):
    letters.append(b)
    letters_count.append(1)
  else:
    idx = letters.index(b)
    letters_count[idx] = letters_count[idx] + 1

print(rules)
print(ins)
# add to pairs
for n in range(steps):

  print("Step %d:" % (n+1))
  update_pairs = []
  update_pairs_count = [] # to be added
  remove_queue = []     # to be set to 0 first
  for r in range(len(rules)):
    a_rule = rules[r][0]
    b_rule = rules[r][1]
    ins_rule = ins[r]

    pair = (a_rule + b_rule)
    new_pair1 = (a_rule + ins_rule)
    new_pair2 = (ins_rule + b_rule)

    if (pair in pairs.keys()): #if (pairs.count(pair)):
      #idx_pair = pairs.index(pair)
      #count = pairs_count[idx_pair]
      count = pairs[pair]

      if (count): # insert
        if not((pair == new_pair1) and (pair == new_pair2)):
          remove_queue.append(pair)

        if (update_pairs.count(new_pair1)):
          idx_update_pairs = update_pairs.index(new_pair1)
          update_pairs_count[idx_update_pairs] = update_pairs_count[idx_update_pairs] + count
        else:
          update_pairs.append(new_pair1)
          update_pairs_count.append(count)

        if (update_pairs.count(new_pair2)):
          idx_update_pairs = update_pairs.index(new_pair2)
          update_pairs_count[idx_update_pairs] = update_pairs_count[idx_update_pairs] + count
        else:
          update_pairs.append(new_pair2)
          update_pairs_count.append(count)
        #if (new_pair1 in pairs.keys()):
        #  new_pair1_count = pairs[new_pair1]
        #else:
        #  new_pair1_count = 0
        #if (new_pair2 in pairs.keys()):
        #  new_pair2_count = pairs[new_pair2]
        #else:
        #  new_pair2_count = 0

        # if rule and insert is just 1 letter
        if (pair == new_pair1) and (pair == new_pair2):
          update_pairs_count[-1] = 1

        # update letter count
        new_letter_count = count
        #print(new_letter_count)
        if (letters.count(ins_rule) == 0):
          letters.append(ins_rule)
          letters_count.append(new_letter_count)
        else:
          idx = letters.index(ins_rule)
          letters_count[idx] = letters_count[idx] + new_letter_count

        if (ins_rule == "C"):
          print("%d C is inserted through rule %s" % (new_letter_count, pair))
        elif (ins_rule == "B"):
          print("%d B is inserted through rule %s" % (new_letter_count, pair))

    if (pair == "HC") or (pair == ("BC")):
      print(new_pair1)
      print(new_pair2)
      print(update_pairs)
      print(update_pairs_count)


  # update pairs
  for q in remove_queue:
    #idx = pairs.index(q)
    #pairs.pop(idx)
    #pairs_count.pop(idx)
    pairs[q] = 0

  for p in update_pairs:
    idx_update_pairs = update_pairs.index(p)
    new_pairs_count = update_pairs_count[idx_update_pairs]
    
    if (p in pairs.keys()): #if (pairs.count(p)):
      #idx = pairs.index(p)
      #pairs_count[idx] = pairs_count[idx] + new_pairs_count
      pairs[p] = pairs[p] + new_pairs_count
    else:
      #pairs.append(p)
      #pairs_count.append(new_pairs_count)
      pairs[p] = new_pairs_count

    if (p == "BC"):
      print("Added %d new BC" % (new_pairs_count))

  print(pairs)
  print(pairs_count)
  print(letters)
  print(letters_count)
        
# bin letetrs
#for x in pairs:
#  a = x[0]
#  b = x[1]
#  if (letters.count(a) == 0):
#    letters.append(a)
#    letters_count.append(1)
#  else:
#    idx = letters.index(a)
#    letters_count[idx] = letters_count[idx] + 1
#
#  if (letters.count(b) == 0):
#    letters.append(b)
#    letters_count.append(1)
#  else:
#    idx = letters.index(b)
#    letters_count[idx] = letters_count[idx] + 1
#for x in polymer:
#  if (letters.count(x) == 0):
#    letters.append(x)
#    letters_count.append(1)
#  else:
#    idx = letters.index(x)
#    letters_count[idx] = letters_count[idx] + 1

print(letters)
print(letters_count)
max_l = max(letters_count)
min_l = min(letters_count)
# queue
#print(pairs)
#print(pairs_count)
print(max_l)
print(min_l)

# print answer
print("First star: %d" % (max_l - min_l))
