f = open("../../inputs/2021/input01.txt", "r")

incr = -1
num = 0

window_num0 = -1
window_num1 = -1
window_num2 = -1

prev_window_sum = 0
window_sum = 0

window_incr = -1

with open('../../inputs/2021/input01.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # update current and previous number
    prev_num = num
    num = int(txtfile_line)

    # compare current number with previous number
    if (num > prev_num):
      incr = incr + 1

    # read next line
    txtfile_line = txtfile.readline() 

num = 0

with open('../../inputs/2021/input01.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # update numbers in the window
    num = int(txtfile_line)
    window_num0 = window_num1
    window_num1 = window_num2
    window_num2 = num

    prev_window_sum = window_sum
    window_sum = window_num0 + window_num1 + window_num2

    if (window_sum > prev_window_sum) and (window_num0 != -1):
      window_incr = window_incr + 1

    # read next line
    txtfile_line = txtfile.readline() 

print("First star: %d" % (incr))
print("Second star: %d" % (window_incr))
