horizontal = 0
depth = 0
aim = 0

with open('../../inputs/2021/input02.txt', 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    parsed_line = txtfile_line.split(" ")
    direction = parsed_line[0]
    num = int(parsed_line[1])
    print(direction)
    print(num)

    # update position
    if (direction == "forward"):
      horizontal = horizontal + num
      depth = depth + aim*num
    elif (direction == "up"):
      #depth = depth - num
      aim = aim - num
      if (depth < 0):
        depth = 0
      if (aim < 0):
        aim = 0
    elif (direction == "down"):
      #depth = depth + num
      aim = aim + num

    # read next line
    txtfile_line = txtfile.readline() 

print("First star: %d" % (horizontal * depth))
print("Second star: %d" % (horizontal * depth))
