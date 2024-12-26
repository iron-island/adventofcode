import pprint

# initialize variables
input_file = "../../inputs/2021/input17.txt"
#input_file = "example17.txt"

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    parsed_line = txtfile_line.strip().split(", ")

    target_area = parsed_line[0]
    x_bounds = target_area.split("x=")[1]
    y_bounds = parsed_line[1][2:]

    x1, x2 = x_bounds.split("..")
    y1, y2 = y_bounds.split("..")
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    # read next line
    txtfile_line = txtfile.readline() 

# Compute max possible vx to still fall inside target area
vx = 0
test_x = 0
min_vx = 0
while (test_x <= x2):
    max_vx = vx
    vx += 1

    test_x = test_x + vx

    if (min_vx == 0) and (test_x >= x1):
        min_vx = vx

print(f'vx range is from {min_vx} to {max_vx}')

def part1():
    vy = 0
    best_vel = [0, 0]
    candidate_max_y = 0
    step = 0
    max_y = 0
    
    #for vx in range(min_vx, x2+1):
    for vx in range(min_vx, max_vx+1):
        init_vx = vx
    
        for vy in range(0, 1000):
            init_vy = vy
            curr_vx = vx
            curr_vy = vy
    
            curr_x = 0
            curr_y = 0
            while True:
                curr_x = curr_x + curr_vx
                curr_y = curr_y + curr_vy
    
                if (curr_vy == 0):
                    candidate_max_y = curr_y
    
                if (curr_vx > 0):
                    curr_vx = curr_vx - 1
                elif (curr_vx < 0):
                    curr_vx = curr_vx + 1
           
                curr_vy = curr_vy - 1
    
                step += 1
    
                if (curr_x in range(x1, x2+1)) and (curr_y in range(y1, y2+1)):
                    if (candidate_max_y > max_y):
                        max_y = candidate_max_y
                        best_vel = [init_vx, init_vy]
                elif (curr_x > x2) or (curr_y < y1):
                    break

    return max_y, best_vel

def part2():
    vy = 0
   
    probe_count = 0 
    for vx in range(min_vx, x2+1):
        init_vx = vx
    
        # 247 was the init_vy for max height in part 1
        for vy in range(y1, 247+1):
            init_vy = vy
            curr_vx = vx
            curr_vy = vy
    
            curr_x = 0
            curr_y = 0
            while True:
                curr_x = curr_x + curr_vx
                curr_y = curr_y + curr_vy
    
                if (curr_vx > 0):
                    curr_vx = curr_vx - 1
                elif (curr_vx < 0):
                    curr_vx = curr_vx + 1
           
                curr_vy = curr_vy - 1
    
                if (curr_x in range(x1, x2+1)) and (curr_y in range(y1, y2+1)):
                    probe_count += 1
                    break
                elif (curr_x > x2) or (curr_y < y1):
                    break

    return probe_count

# print answer
#max_y, best_vel = part1()
#print(f'best_vel = {best_vel}')
#print(f'First star: {max_y}')

probe_count = part2()
print(f'Second star: {probe_count}')
