# initialize variables
num = 0
bit11_1 = 0
bit10_1 = 0
bit9_1 = 0
bit8_1 = 0
bit7_1 = 0
bit6_1 = 0
bit5_1 = 0
bit4_1 = 0
bit3_1 = 0
bit2_1 = 0
bit1_1 = 0
bit0_1 = 0

total_lines = 0

# read input file
with open('../../inputs/2021/input03.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    num = txtfile_line

    # process
    gamma = list("000000000000")
    epsilon = list("111111111111")
    total_lines = total_lines + 1

    if (num[0] == "1"):
      bit11_1 = bit11_1 + 1
    if (num[1] == "1"):
      bit10_1 = bit10_1 + 1
    if (num[2] == "1"):
      bit9_1 = bit9_1 + 1
    if (num[3] == "1"):
      bit8_1 = bit8_1 + 1

    if (num[4] == "1"):
      bit7_1 = bit7_1 + 1
    if (num[5] == "1"):
      bit6_1 = bit6_1 + 1
    if (num[6] == "1"):
      bit5_1 = bit5_1 + 1
    if (num[7] == "1"):
      bit4_1 = bit4_1 + 1

    if (num[8] == "1"):
      bit3_1 = bit3_1 + 1
    if (num[9] == "1"):
      bit2_1 = bit2_1 + 1
    if (num[10] == "1"):
      bit1_1 = bit1_1 + 1
    if (num[11] == "1"):
      bit0_1 = bit0_1 + 1


    # read next line
    txtfile_line = txtfile.readline() 

bit11_0 = total_lines - bit11_1
bit10_0 = total_lines - bit10_1
bit9_0 = total_lines - bit9_1
bit8_0 = total_lines - bit8_1
bit7_0 = total_lines - bit7_1
bit6_0 = total_lines - bit6_1
bit5_0 = total_lines - bit5_1
bit4_0 = total_lines - bit4_1
bit3_0 = total_lines - bit3_1
bit2_0 = total_lines - bit2_1
bit1_0 = total_lines - bit1_1
bit0_0 = total_lines - bit0_1

if (bit11_1 > bit11_0):
  gamma[0] = '1'
  epsilon[0] = "0"
if (bit10_1 > bit10_0):
  gamma[1] = '1'
  epsilon[1] = "0"
if (bit9_1 > bit9_0):
  gamma[2] = '1'
  epsilon[2] = "0"
if (bit8_1 > bit8_0):
  gamma[3] = '1'
  epsilon[3] = "0"

if (bit7_1 > bit7_0):
  gamma[4] = '1'
  epsilon[4] = "0"
if (bit6_1 > bit6_0):
  gamma[5] = '1'
  epsilon[5] = "0"
if (bit5_1 > bit5_0):
  gamma[6] = '1'
  epsilon[6] = "0"
if (bit4_1 > bit4_0):
  gamma[7] = '1'
  epsilon[7] = "0"

if (bit3_1 > bit3_0):
  gamma[8] = "1"
  epsilon[8] = "0"
if (bit2_1 > bit2_0):
  gamma[9] = "1"
  epsilon[9] = "0"
if (bit1_1 > bit1_0):
  gamma[10] = "1"
  epsilon[10] = "0"
if (bit0_1 > bit0_0):
  gamma[11] = "1"
  epsilon[11] = "0"

gamma_num = int("".join(gamma), 2)
epsilon_num = int("".join(epsilon), 2)

power = gamma_num*epsilon_num

oxygen_list = []
co2_list = []

# read input file
with open('../../inputs/2021/input03.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    num = txtfile_line

    if (num[0] == gamma[0]):
      oxygen_list.append(num[0:12])
    else:
      co2_list.append(num[0:12])

    # read next line
    txtfile_line = txtfile.readline() 

oxygen_total = len(oxygen_list)
co2_total = len(co2_list)

for i in range(1, 12):
  if (oxygen_total > 1):
    new_oxygen_list = []
    bits1 = 0
    bits0 = 0
    for j in range(oxygen_total):
      # find majority
      if (oxygen_list[j][i] == "1"):
        bits1 = bits1 + 1
      else:
        bits0 = bits0 + 1

  bit_crit = "1"
  if (bits1 < bits0):
    bit_crit = "0"

  if (oxygen_total > 1):
    for j in range(oxygen_total):
      if (oxygen_list[j][i] == bit_crit):
        new_oxygen_list.append(oxygen_list[j])

  if (co2_total > 1):
    new_co2_list = []
    bits1 = 0
    bits0 = 0
    for j in range(co2_total):
      # find majority
      if (co2_list[j][i] == "0"):
        bits0 = bits0 + 1
      else:
        bits1 = bits1 + 1

  bit_crit = "0"
  if (bits1 < bits0):
    bit_crit = "1"

  if (co2_total > 1):
    for j in range(co2_total):
      if (co2_list[j][i] == bit_crit):
        new_co2_list.append(co2_list[j])

  oxygen_list = new_oxygen_list
  co2_list = new_co2_list
  oxygen_total = len(oxygen_list)
  co2_total = len(co2_list)
  print("oxygen_total: %d" % (oxygen_total))
  print("co2_total: %d " % (co2_total))

oxygen_num = int("".join(oxygen_list[0]), 2)
co2_num = int("".join(co2_list[0]), 2)
life = oxygen_num*co2_num
print(oxygen_list)
print(co2_list)
print(oxygen_num)
print(co2_num)

# print answer
print("First star: %d" % (power))
print("Second star: %d" % (life))
