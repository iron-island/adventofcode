import math
import re

input_file = "input5.txt"
example_file = "example5.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

seeds = []

def a2b(a_int, dict_map):
    b = None
    for i in dict_map:
        src, dsrange = i
        dest = dict_map[(src, dsrange)]
    
        if a_int in range(src, src + dsrange):
            b = dest + (a_int - src)
            break
    
    if (b == None):
        b = a_int

    return b

def process_inputs(in_file):
    output = 0

    seed2soil = {}
    soil2fert = {}
    fert2water = {}
    water2light = {}
    light2temp = {}
    temp2hum = {}
    hum2loc = {}
    mydict = {}
    with open(in_file) as file:
        line = file.readline()
   
        seeds = re.findall(r'\d+', line[7:])

        mapping = None
        while line:
            line = line.strip()

            if (line == ""):
                mapping = None
                line = file.readline()
                continue

            if (mapping == None):
                if ("seed-to-soil" in line):
                    dict_map = seed2soil
                    mapping = 1
                elif ("soil-to-fert" in line):
                    dict_map = soil2fert
                    mapping = 1
                elif ("fertilizer-to-water" in line):
                    dict_map = fert2water
                    mapping = 1
                elif ("water-to-light" in line):
                    dict_map = water2light
                    mapping = 1
                elif ("light-to-temp" in line):
                    dict_map = light2temp
                    mapping = 1
                elif ("temperature-to-humidity" in line):
                    dict_map = temp2hum
                    mapping = 1
                elif ("humidity-to-location" in line):
                    dict_map = hum2loc
                    mapping = 1
            else:
                dest, src, dsrange = re.findall(r'\d+', line)
                dict_map[(int(src), int(dsrange))] = int(dest)

            line = file.readline()

    loc_list = []
    for s in seeds:
        #seed = int(s)
        #soil = None
        #for i in seed2soil:
        #    src, dsrange = i
        #    dest = seed2soil[(src, dsrange)]
    
        #    if seed in range(src, src + dsrange):
        #        soil = dest + (seed - src)
        #        #print(soil)
        #        break

        #if (soil == None):
        #    soil = seed
        soil = a2b(int(s), seed2soil)
        fert = a2b(soil, soil2fert)
        water = a2b(fert, fert2water)
        light = a2b(water, water2light)
        temp = a2b(light, light2temp)
        hum = a2b(temp, temp2hum)
        loc = a2b(hum, hum2loc)

        loc_list.append(loc)

    output = min(loc_list)

    return output

def process_inputs2(in_file):
    output = 0

    seed2soil = {}
    soil2fert = {}
    fert2water = {}
    water2light = {}
    light2temp = {}
    temp2hum = {}
    hum2loc = {}
    mydict = {}

    seeds_list = []
    with open(in_file) as file:
        line = file.readline()
   
        seeds = re.findall(r'\d+', line[7:])

        mapping = None
        while line:
            line = line.strip()

            if (line == ""):
                mapping = None
                line = file.readline()
                continue

            if (mapping == None):
                if ("seed-to-soil" in line):
                    dict_map = seed2soil
                    mapping = 1
                elif ("soil-to-fert" in line):
                    dict_map = soil2fert
                    mapping = 1
                elif ("fertilizer-to-water" in line):
                    dict_map = fert2water
                    mapping = 1
                elif ("water-to-light" in line):
                    dict_map = water2light
                    mapping = 1
                elif ("light-to-temp" in line):
                    dict_map = light2temp
                    mapping = 1
                elif ("temperature-to-humidity" in line):
                    dict_map = temp2hum
                    mapping = 1
                elif ("humidity-to-location" in line):
                    dict_map = hum2loc
                    mapping = 1
            else:
                dest, src, dsrange = re.findall(r'\d+', line)
                dict_map[(int(src), int(dsrange))] = int(dest)

            line = file.readline()

    # Split seeds according to ranges based on seed2soil

    min_loc = 1000000000000
    min_seed = 0
    min_cnt = 0
    cnt = 0
    skip = 1
    if (skip != 1):
        for s in seeds:
            #seed = int(s)
            #soil = None
            #for i in seed2soil:
            #    src, dsrange = i
            #    dest = seed2soil[(src, dsrange)]
        
            #    if seed in range(src, src + dsrange):
            #        soil = dest + (seed - src)
            #        #print(soil)
            #        break

            #if (soil == None):
            #    soil = seed

            if (cnt % 2 == 0):
                init = int(s)
                cnt += 1
                continue
            else:
                init_range = int(s)

                for i in range(init, init + init_range - 1, 10000):
                    soil = a2b(i, seed2soil)
                    fert = a2b(soil, soil2fert)
                    water = a2b(fert, fert2water)
                    light = a2b(water, water2light)
                    temp = a2b(light, light2temp)
                    hum = a2b(temp, temp2hum)
                    loc = a2b(hum, hum2loc)

                    if (loc < min_loc):
                        min_loc = loc
                        min_seed = i
                        min_cnt = cnt
                        print(f'min_loc, min_seed, min_cnt = {min_loc}, {min_seed}, {min_cnt}')

            cnt += 1

    #lb = 124747783
    #ub = lb + 108079254 - 1
    #for i in range(lb, ub, 1000):

    #lb = 222935783 - 2000
    #ub = 222935783 + 2000
    #for i in range(lb, ub):

    #lb = 2957349913
    #ub = lb + 359478652 - 1
    #for i in range(lb, ub, 1000):
    
    lb = 3177317913 - 2000
    ub = 3177317913 + 2000
    for i in range(lb, ub):
        soil = a2b(i, seed2soil)
        fert = a2b(soil, soil2fert)
        water = a2b(fert, fert2water)
        light = a2b(water, water2light)
        temp = a2b(light, light2temp)
        hum = a2b(temp, temp2hum)
        loc = a2b(hum, hum2loc)

        if (loc < min_loc):
            min_i = i
            min_loc = loc
    print(min_i)
    output = min_loc

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
