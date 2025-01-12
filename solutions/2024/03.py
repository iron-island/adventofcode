input_file = "../../inputs/2024/input03.txt"
example_file = "example03.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def mul(x,y):
    
    return int(x)*int(y)

def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
        nextline = line

        while nextline:
            line = line.strip()
            nextline = file.readline()
            line = line + nextline

        i = 0
        while i != -1:
            i = line.find("mul(")
            if (i > 0):
                subline = line[i+1:]
                j = subline.find(")")

                if (j > 0):
                    #print(line[i:(i+j+2)])
                    try:
                        product = eval(line[i:(i+j+2)])
                        output += product
                        #print(line[i:(i+j+2)])
                    except:
                        product = 0

                    line = line[i+1:]

    return output

def process_inputs2(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
        nextline = line

        while nextline:
            line = line.strip()
            nextline = file.readline()
            line = line + nextline

        # find do() and don't()
        i = 0
        enabled_line = ""
        #while i != -1:
        #    i = line.find("don't()")
        #    j = line.find("do()")

        #    if (i > 0) and (j > 0):
        #        # dont first
        #        if (i < j):
        #            line = line[:i] + line[j+4:]
        #        # do first
        #        else:
        #            i = line.find("do()")
        #       
        #            if (i > 0):
        #                line = line[i+4:] 
        dont_split = line.split("don't()")
        enabled_line = dont_split[0]
        dont_split = dont_split[1:]
        #print(len(dont_split))
        for d in dont_split:
            if ("do()" in d):
                d_split = d.split("do()")
                enabled_strings = ''.join(d_split[1:])
                enabled_line = enabled_line + enabled_strings

        # mul()
        i = 0
        line = enabled_line
        while i != -1:
            i = line.find("mul(")
            if (i > 0):
                subline = line[i+1:]
                j = subline.find(")")

                if (j > 0):
                    #print(line[i:(i+j+2)])
                    try:
                        product = eval(line[i:(i+j+2)])
                        output += product
                        #print(line[i:(i+j+2)])
                    except:
                        product = 0

                    line = line[i+1:]

    return output

#part1_example = process_inputs(example_file)
part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print("")
print("--- Advent of Code 2024 Day 3: Mull It Over ---")
#print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
#print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
