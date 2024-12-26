import pprint

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(myqueue)

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def pop_dig(parsed_line, i, dig):
  for j in range(len(dig)):
    dig[j] = parsed_line[i][j]

  return dig

def ispresent(target, test):
  res = all(ele in target for ele in test)
  return res

# 1 uses 2
# 4 uses 4
# 7 uses 3
# 8 uses 7

def get_dig(digstring, seg):
  lenstring = len(digstring)
  d = [0 for i in range(7)]
  for i in range(lenstring):
    idx = seg.index(digstring[i])
    d[idx] = 1

  if (lenstring == 2):
    digit = 1
  elif (lenstring == 4):
    digit = 4
  elif (lenstring == 3):
    digit = 7
  elif (lenstring == 7):
    digit = 8
  elif (d[0] and d[1] and d[2] and not(d[3]) and d[4] and d[5] and d[6]):
    digit = 0
  elif (d[0] and not(d[1]) and d[2] and d[3] and d[4] and not(d[5]) and d[6]):
    digit = 2
  elif (d[0] and not(d[1]) and d[2] and d[3] and not(d[4]) and d[5] and d[6]):
    digit = 3
  elif (d[0] and d[1] and not(d[2]) and d[3] and not(d[4]) and d[5] and d[6]):
    digit = 5
  elif (d[0] and d[1] and not(d[2]) and d[3] and d[4] and d[5] and d[6]):
    digit = 6
  elif (d[0] and d[1] and d[2] and d[3] and not(d[4]) and d[5] and d[6]):
    digit = 9
    
  return digit

# initialize variables
num_digits = 0
alldig = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
iteration = 0
out = 0

# read input file
with open('../../inputs/2021/input08.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    seg = ['x' for i in range(7)]
    dig0 = ['x' for i in range(6)]
    dig1 = ['x' for i in range(2)]
    dig2 = ['x' for i in range(5)]
    dig3 = ['x' for i in range(5)]
    dig4 = ['x' for i in range(4)]
    dig5 = ['x' for i in range(5)]
    dig6 = ['x' for i in range(6)]
    dig7 = ['x' for i in range(3)]
    dig8 = ['x' for i in range(7)]
    dig9 = ['x' for i in range(6)]
    dig0_known = 0
    dig1_known = 0
    dig2_known = 0
    dig3_known = 0
    dig4_known = 0
    dig5_known = 0
    dig6_known = 0
    dig7_known = 0
    dig8_known = 0
    dig9_known = 0

    # parse
    parsed_line = txtfile_line.split(" | ")
    parsed_line1 = parsed_line[0].split()
    parsed_line2 = parsed_line[1].split()

    # process
    num_1 = len(parsed_line1)
    num_2 = len(parsed_line2)

    parsed_line = ['x' for i in range(num_1 + num_2)]

    for i in range(num_1):
      parsed_line[i] = parsed_line1[i]
    for i in range(num_2):
      parsed_line[i + num_1] = parsed_line2[i]

    num = len(parsed_line)

    # find dig1, dig4, dig7 first
    for i in range(num):
      cur_len = len(parsed_line[i])

      if (cur_len == 3): # digit 7
        dig7_known = 1
        for j in range(3):
          dig7[j] = parsed_line[i][j]

      if (cur_len == 2): # digit 1
        dig1_known = 1
        for j in range(2):
          dig1[j] = parsed_line[i][j]

      if (cur_len == 4): # digit 4
        dig4_known = 1
        for j in range(4):
          dig4[j] = parsed_line[i][j]

    # OPTIMIZED
    if (dig1_known and dig4_known and dig7_known):
      cur_out = 0
      for i in range(num_2):
        cur_dig = parsed_line2[i]
        cur_len = len(cur_dig)
        
        if (cur_len == 6):
          if (ispresent(cur_dig, dig1) and ispresent(cur_dig, dig7) and not(ispresent(cur_dig, dig4))):
            digit = 0
          elif (ispresent(cur_dig, dig1) and ispresent(cur_dig, dig7) and ispresent(cur_dig, dig4)):
            digit = 9
          elif not(ispresent(cur_dig, dig1)):
            digit = 6
        elif (cur_len == 5):
          if (ispresent(cur_dig, dig1) and ispresent(cur_dig, dig7) and not(ispresent(cur_dig, dig4))):
            digit = 3
          else:
            count_present = 0
            for j in range(4):
              count_present = count_present + cur_dig.count(dig4[j])
            if (count_present == 3):
              digit = 5
            else:
              digit = 2
        elif (cur_len == 2):
          digit = 1
        elif (cur_len == 4):
          digit = 4
        elif (cur_len == 3):
          digit = 7
        elif (cur_len == 7):
          digit = 8

        cur_out = cur_out + digit*(10**(3-i))

    out = out + cur_out

    # if length is 6:
    #   digit 0 if present 1,7 but not 4
    #   digit 6 if 1 not present
    #   digit 9 if 1, 7, 4 present
    # if length is 5:
    #   digit 5 if 4 is missing 1
    #   digit 2 if 4 is missing 2
    #   digit 3 if present 1, 7

    ## find unique letter between dig7 and dig1
    #for i in range(len(dig7)):
    #  if (dig1.count(dig7[i]) == 0):
    #    seg[0] = dig7[i]

    ## if 5 letters and all dig1 letters are present, it is dig3
    #for i in range(num):
    #  cur_len = len(parsed_line[i])
    #  
    #  if (cur_len == 5):
    #    if ((parsed_line[i].count(dig1[0])) and (parsed_line[i].count(dig1[1]))):
    #      dig3_known = 1
    #      dig3 = pop_dig(parsed_line, i, dig3)
    #      break

    ## if 6 letters and not all dig1 letters are present, it is dig6
    ##              and dig4 is present, it is dig9
    #for i in range(num):
    #  cur_len = len(parsed_line[i])
    #  if (cur_len == 6):
    #    if (dig1_known):
    #      count0 = parsed_line[i].count(dig1[0])
    #      count1 = parsed_line[i].count(dig1[1])
    #      num_present = count0 + count1
    #      if (num_present == 1): # find dig6
    #        dig6_known = 1
    #        dig6 = pop_dig(parsed_line, i, dig6)
    #        if (count0):
    #          seg[5] = dig1[0]
    #          seg[2] = dig1[1]
    #        elif (count1):
    #          seg[5] = dig1[1]
    #          seg[2] = dig1[0]
    #    
    #      elif (num_present == 2): # find dig0
    #        dig0_known = 1
    #        dig0 = pop_dig(parsed_line, i, dig0)
    #        temp_list = list(set(alldig) - set(dig0))
    #        seg[3] = temp_list[0]

    #    if (dig4_known):
    #      count0 = parsed_line[i].count(dig4[0])
    #      count1 = parsed_line[i].count(dig4[1])
    #      count2 = parsed_line[i].count(dig4[2])
    #      count3 = parsed_line[i].count(dig4[3])
    #      num_present = count0 + count1 + count2 + count3
    #      if(num_present == 4):
    #        dig9_known = 1
    #        dig9 = pop_dig(parsed_line, i, dig9)
    #        temp_list = list(set(alldig) - set(dig9))
    #        seg[4] = temp_list[0]

    #  # currently known seg: 0, 2, 3, 4, 5
    #  if (seg[0] != 'x') and (seg[0] != 'x') and (seg[2] != 'x') and (seg[3] != 'x') and (seg[4] != 'x') and (seg[5] != 'x') and (dig4_known == 1):
    #    temp_list = list(set(alldig) - set(dig4))
    #    seg[1] = temp_list[0]

    #curr_out = 0
    #for i in range(num_2):
    #  dig = get_dig(parsed_line2[i], seg)  
    #  curr_out = curr_out + dig*10**(3-i)
   
    #out = out + curr_out 


    # read next line
    iteration = iteration + 1
    txtfile_line = txtfile.readline() 

# print answer
ans1 = out
print("First star: %d" % (ans1))
#print("Second star: %d" % (ans2))
