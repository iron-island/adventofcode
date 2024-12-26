import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

# initialize variables
myqueue = []
score = 0
score_list = []

# read input file
with open('../../inputs/2021/input10.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    length = len(txtfile_line) - 1

    # process
    myqueue = []
    for i in range(length):
      c = txtfile_line[i]
      o_par = '('
      o_brack = '['
      o_brace = '{'
      o_tag = '<'
      c_par = ')'
      c_brack = ']'
      c_brace = '}'
      c_tag = '>'
      opening = (c == '(') or (c == '[') or (c == '{') or (c == '<')

      if opening:
        myqueue.append(c)
        #print("push!")
      else:
        last_elem = myqueue[-1]
        if (c == c_par) and (last_elem == o_par):
          print("pop!")
          myqueue.pop()
        elif (c == c_brack) and (last_elem == o_brack):
          myqueue.pop()
          print("pop!")
        elif (c == c_brace) and (last_elem == o_brace):
          myqueue.pop()
          print("pop!")
        elif (c == c_tag) and (last_elem == o_tag):
          myqueue.pop()
          print("pop!")
        else:   # corrupted line
          print("corrupted!")
          #cur_score = 0
          #if (c == c_par):
          #  cur_score = 3
          #elif (c == c_brack):
          #  cur_score = 57
          #elif (c == c_brace):
          #  cur_score = 1197
          #elif (c == c_tag):
          #  cur_score = 25137
          #score = score + cur_score
          break

      if (i == (length-1)) and (len(myqueue) > 0):
        myqueue_len = len(myqueue)
        print(myqueue)
        # incomplete
        print("incomplete")
        score = 0
        for q in range(myqueue_len-1, -1, -1):
          elem = myqueue[q]
          cur_score = 0
          if (elem == o_par):
            cur_score = 1
          elif (elem == o_brack):
            cur_score = 2
          elif (elem == o_brace):
            cur_score = 3
          elif (elem == o_tag):
            cur_score = 4

          score = score*5 + cur_score 

        score_list.append(score)
        score = 0
        myqueue = []
          
    # read next line
    txtfile_line = txtfile.readline() 

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(myqueue)

score_list.sort()
length = len(score_list)
print(length)
print(score_list)
middle_score = score_list[int((length-1)/2)]

# print answer
print("First star: %d" % (score))
print("Second star: %d" % (middle_score))
