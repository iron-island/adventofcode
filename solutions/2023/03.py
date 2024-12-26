input_file = "input3.txt"
example_file = "example03.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
symbol_list = []
engine_array = []
include_list = []
def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            line = line.strip()

            #engine_array.append(line)

            #numbers_list = re.findall(r'\d+', line)
            #numbers_array.append(numbers_list)
 
            col = 0 
            for idx, c in enumerate(line):
                if (c.isdigit() == False) and (c != '.'):
                    #symbol_list.append((row, col))

                    # left
                    include_list.append((idx-1, row-1))
                    include_list.append((idx-1, row))
                    include_list.append((idx-1, row+1))

                    # top, bottom
                    include_list.append((idx, row-1))
                    include_list.append((idx, row+1))

                    # right
                    include_list.append((idx+1, row-1))
                    include_list.append((idx+1, row))
                    include_list.append((idx+1, row+1))
        
                col += 1
            #
            row += 1
            line = file.readline()

    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            line = line.strip()

            #print(include_list)
            isvalid = False
            part_string = ""
            line = line + "."
            for idx, c in enumerate(line):
                if (c.isdigit()):
                    part_string = part_string + c

                    if ((idx, row) in include_list):
                        isvalid = True

                else:
                    if (part_string != "") and isvalid:
                        #if (row == 19):
                        #    print(part_string)
                        output = output + int(part_string)
                        isvalid = False
                        part_string = ""

                    part_string = ""

            #
            row += 1
            line = file.readline()

    return output

def process_inputs2(in_file):
    gear_array = []
    valid_array = []
    output = 0

    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            line = line.strip()

            #engine_array.append(line)

            #numbers_list = re.findall(r'\d+', line)
            #numbers_array.append(numbers_list)
 
            col = 0 
            for idx, c in enumerate(line):
                gear = []
                if (c == "*"):
                    # left
                    gear.append((idx-1, row-1))
                    gear.append((idx-1, row))
                    gear.append((idx-1, row+1))

                    # top, bottom
                    gear.append((idx, row-1))
                    gear.append((idx, row+1))

                    # right
                    gear.append((idx+1, row-1))
                    gear.append((idx+1, row))
                    gear.append((idx+1, row+1))

                    gear_array.append(gear)
                    valid_array.append([])
        
                col += 1
            #
            row += 1
            line = file.readline()

    with open(in_file) as file:
        line = file.readline()
   
        row = 0 
        while line:
            line = line.strip()

            #print(include_list)
            isvalid = -1
            part_string = ""
            line = line + "."
            for idx, c in enumerate(line):
                if (c.isdigit()):
                    part_string = part_string + c

                    for g_idx, gear in enumerate(gear_array):
                        if ((idx, row) in gear):
                            isvalid = g_idx
                            print(f'{part_string}, {isvalid}')

                else:
                    if (part_string != "") and (isvalid > -1):
                        valid_array[isvalid].append(int(part_string))
                        isvalid = -1
                        part_string = ""

                    part_string = ""

            #
            row += 1
            line = file.readline()

    for v in valid_array:
        if (len(v) == 2):
            print(f'{v[0]} * {v[1]}')
            output = output + v[0]*v[1]

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
