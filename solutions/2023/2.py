input_file = "input2.txt"
example_file = "example2.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
RED = 12
GREEN = 13
BLUE = 14
game_id_list = []
def process_inputs(in_file):
    output = 0

    game_id = 1
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            split_line = line.split(":")
            #game_id = int(split_line[0].split())

            #game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            sets = split_line[1].split("; ")
            possible = True
            for idx, s in enumerate(sets):
                colors = s.split(", ")
                for c in colors:
                    if ("red" in c):
                        red_num = int(c[:-4])
                        #game[idx][0] = red_num
                        if (red_num > RED):
                            possible = False
                    elif ("green" in c):
                        green_num = int(c[:-6])
                        #game[idx][1] = green_num
                        if (green_num > GREEN):
                            possible = False
                    elif ("blue" in c):
                        blue_num = int(c[:-5])
                        #game[idx][2] = blue_num
                        if (blue_num > BLUE):
                            possible = False
            
            if (possible):
                output = output + game_id

            game_id += 1
            line = file.readline()

    return output

def process_inputs2(in_file):
    output = 0

    game_id = 1
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            split_line = line.split(":")
            #game_id = int(split_line[0].split())

            #game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            sets = split_line[1].split("; ")
            possible = True
            power = 0
            INIT_MAX = 0
            max_r = INIT_MAX 
            max_g = INIT_MAX 
            max_b = INIT_MAX 
            for idx, s in enumerate(sets):
                colors = s.split(", ")
                for c in colors:
                    if ("red" in c):
                        red_num = int(c[:-4])
                        #game[idx][0] = red_num
                        if (red_num > RED):
                            possible = False

                        if (red_num > max_r):   
                            max_r = red_num
                    elif ("green" in c):
                        green_num = int(c[:-6])
                        #game[idx][1] = green_num
                        if (green_num > GREEN):
                            possible = False
                        if (green_num > max_g):
                            max_g = green_num
                    elif ("blue" in c):
                        blue_num = int(c[:-5])
                        #game[idx][2] = blue_num
                        if (blue_num > BLUE):
                            possible = False
                        if (blue_num > max_b):
                            max_b = blue_num

            power = max_r*max_g*max_b
            #print(f'{max_r}, {max_g}, {max_b}')
            output = output + power
 
            game_id += 1
            line = file.readline()

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
