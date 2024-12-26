import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def print_mixed_nums(mixed_nums):
  for i in range(0, len(mixed_nums)):
    for m in mixed_nums:
      if (mixed_nums[m] == i):
        print(m[0], end=", ")
  print("")

# initialize variables
input_file = "../../inputs/2022/input20.txt"
#input_file = "example20.txt"

nums = {}

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  idx = 0
  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    num = int(txtfile_line)*811589153
    v = 0
    while (num, v) in nums:
      v += 1
    nums[(num, v)] = idx
    idx += 1
      
    # read next line
    txtfile_line = txtfile.readline() 

len_nums = len(nums)
mod_num = len(nums) - 1
mixed_nums = nums.copy()

# mix
for i in range(1, 11):
  print(f'Iteration {i}/10...')
  for n_tuple in nums:
    n = n_tuple[0]
    idx = mixed_nums[n_tuple]
  
    #if (n < 0):
    #  new_idx = (idx + n - 1) % mod_num
    #  if (new_idx == 0):
    #    new_idx = mod_num-1
    #else:
    #  new_idx = (idx + n)
    #  if (new_idx >= mod_num):
    #    new_idx = new_idx % mod_num + 1
    if (n > 0):
      new_idx = (idx + n) % mod_num
      if new_idx == 0:
        new_idx = mod_num
    else:
      new_idx = (idx + n) % mod_num
      if new_idx == 0:
        new_idx = mod_num

    #print(f'Moving {n} to index {new_idx}')
  
    # mix
    mixed_nums[n_tuple] = new_idx
    if (new_idx > idx):
      #if (n > 0):
      for other_tuple in mixed_nums:
        idx_o = mixed_nums[other_tuple]
        if (idx_o > idx) and (idx_o <= new_idx) and (other_tuple != n_tuple):
          mixed_nums[other_tuple] = idx_o - 1
      #else:
      #  for other_tuple in mixed_nums:
      #    idx_o = mixed_nums[other_tuple]
      #    if (idx_o > idx) and (idx_o < new_idx) and (other_tuple != n_tuple):
      #      mixed_nums[other_tuple] = idx_o - 1
    elif (new_idx < idx):
      for other_tuple in mixed_nums:
        idx_o = mixed_nums[other_tuple]
        if (idx_o < idx) and (idx_o >= new_idx) and (other_tuple != n_tuple):
          mixed_nums[other_tuple] = idx_o + 1

  #print_mixed_nums(mixed_nums)

print_mixed_nums(mixed_nums)
# find 0
mixed_indices = {}
for m in mixed_nums:
  idx = mixed_nums[m]
  mixed_indices[idx] = m

idx_0 = mixed_nums[(0, 0)]
m1 = (idx_0 + 1000) % len_nums
m2 = (idx_0 + 2000) % len_nums
m3 = (idx_0 + 3000) % len_nums

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
num_m1 = mixed_indices[m1][0]
num_m2 = mixed_indices[m2][0]
num_m3 = mixed_indices[m3][0]

print(num_m1)
print(num_m2)
print(num_m3)
ans1 = num_m1 + num_m2 + num_m3
ans2 = 0
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
