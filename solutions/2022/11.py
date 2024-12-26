# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 13:52:43 2022

@author: AIson
"""

input_file = "../../inputs/2022/input11.txt"
#input_file = "example11.txt"

last_m = 0
items = []
operation = []
operand = []
div_by = []
true_result = []
false_result = []
inspected = []
with open(input_file) as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(" ")
    
    if ("Monkey" in txtfile_line):
      inspected.append(0)
    elif ("Starting" in txtfile_line):
      item_list = []
      for p in parsed_line[2:]:
        item = int(p.split(",")[0])
        item_list.append(item)
      items.append(item_list.copy())
    elif ("Operation" in txtfile_line):
      operation.append(parsed_line[4])
      
      if (parsed_line[5] == "old"):
        operand.append(parsed_line[5])
      else:
        operand.append(int(parsed_line[5]))
    elif ("Test" in txtfile_line):
      div_by.append(int(parsed_line[3]))
    elif ("If true" in txtfile_line):
      true_result.append(int(parsed_line[5]))
    elif ("If false" in txtfile_line):
      false_result.append(int(parsed_line[5]))
        
    # read next line
    txtfile_line = txtfile.readline()
    
num_rounds = 10000
pattern = []
pattern.append([6, 0, 6, 0, 16, 14, 16, 6])
pattern.append([14, 0, 14, 0, 6, 16, 6, 14])
pattern.append([16, 0, 16, 0, 14, 6, 14, 16])

for r in range(1, num_rounds+1):
  if (r < num_rounds*2):
    prev_inspected = inspected.copy()
    diff_inspected = inspected.copy()
    for idx_m, m in enumerate(items):
      #m_copy = m.copy()
      for idx_i, i in enumerate(m):
        #'''
        # inspect
        if operand[idx_m] == "old":
          op = i
        else:
          op = operand[idx_m]
            
        if operation[idx_m] == '+':
          m[idx_i] = i + op
        else:
          #if (operand[idx_m] == "old"):
          #  m[idx_i] = i
          #else:
          #  m[idx_i] = i * op
          m[idx_i] = i * op
        inspected[idx_m] += 1
        
        # decrease worry
        #m[idx_i] = m[idx_i]//3
        #m[idx_i] = m[idx_i] % (23*19*13*17)
        m[idx_i] = m[idx_i] % (3*13*19*17*5*7*11*2)
        
        # throw
        if (m[idx_i] % div_by[idx_m]) == 0:
          receive = true_result[idx_m]
        else:
          receive = false_result[idx_m]
            
        items[receive].append(m[idx_i])
        #'''
        
        #m_copy.pop(0)
      #items[idx_m] = m_copy.copy()
      items[idx_m] = []    
    
    #print(r)
    for idx, i in enumerate(inspected):
      diff_inspected[idx] = i - prev_inspected[idx]
    print(diff_inspected)
  else:
    # enforce pattern:
    if (input_file == "dec11_test.txt"):
      p = (r - 8) % 3
      for idx, i in enumerate(inspected):
        inspected[idx] = i + pattern[p][idx]
    else:
      pattern = [5, 5, 0, 5]
      for idx, i in enumerate(inspected):
        inspected[idx] = i + pattern[idx]

print(inspected)
