import pprint
import math

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

#def snafu_to_dec

# initialize variables
input_file = "../../inputs/2022/input25.txt"
#input_file = "example25.txt"

decimal = []
sum_decimal = 0
DEBUG = 0
# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()

    # process
    num = 0
    for i in range(1, len(txtfile_line)+1):
      character = txtfile_line[-1*i]
      if (character == "="):
        digit = -2
      elif (character == "-"):
        digit = -1
      else:
        digit = int(character)

      num += digit*(5**(i - 1))
    DEBUG = 1
    decimal.append(num)
    sum_decimal += num

    # read next line
    txtfile_line = txtfile.readline() 

#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint()

print(decimal)
print(sum_decimal)

# find highest digit first
i = 0
min_diff = math.inf
diff = math.inf
for i in range(0, 22):
  # increment digits
  for d in range(1, 4):
    diff = abs(sum_decimal - d*(5**i))

    if (diff < min_diff):
      min_diff = diff
      best_d = d
      best_i = i

if (best_d == 3):
  best_i = best_i + 1
  best_d = 1

sum_snafu = ""
sum_snafu = sum_snafu + str(best_d)

# after finding highest digit, find remaining digits
for i in range(best_i-1, -1, -1):
  min_diff = sum_decimal - best_d*(5**(i+1))
  sum_decimal = min_diff

  min_diff = math.inf
  for d in [-2, -1, 0, 1, 2]:
    diff = abs(sum_decimal - d*(5**i))

    if (diff < min_diff):
      min_diff = diff
      best_d = d

  if (best_d == -2):
    snafu_d = "="
  elif (best_d == -1):
    snafu_d = "-"
  else:
    snafu_d = str(best_d)

  sum_snafu = sum_snafu + snafu_d

# print answer
ans1 = sum_snafu
ans2 = 0
print(f'First star: {ans1}')
print(f'Second star: {ans2}')
