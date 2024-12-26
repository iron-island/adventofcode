# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:42:40 2023

@author: AIson
"""

def process_inputs(input_file):
    card2hex = {
        '2' : '0',
        '3' : '1',
        '4' : '2',
        '5' : '3',
        '6' : '4',
        '7' : '5',
        '8' : '6',
        '9' : '7',
        'T' : '8',
        'J' : '9',
        'Q' : 'A',
        'K' : 'B',
        'A' : 'C' 
        }

    output = 0

    int2bid = {}
    int_list = []
    with open(input_file) as file:
        line = file.readline()
        
        while line:
            line = line.strip()
        
            line = line.split()
            
            hex_string = ''
            for c in line[0]:
                hex_string = hex_string + card2hex[c]
            
            len_set = len(set(hex_string))
            if (len_set == 5): # high card
                hex_string = hex_string
            elif (len_set == 4): # one pair
                hex_string = 'F' + hex_string
            elif (len_set == 3): # two pair or 3 of a kind
                twopair = False
                for h in hex_string:
                    if hex_string.count(h) == 2:
                        twopair = True
                        
                if (twopair): # two pair
                    #print(f'Two pair: {hex_string}')
                    hex_string = 'FF' + hex_string
                else: # three of a kind
                    #print(f'Three of a kind: {hex_string}')
                    hex_string = 'FFF' + hex_string
            elif (len_set == 2): # full house or 4 of a kind
                fullhouse = False
                for h in hex_string:
                    if hex_string.count(h) == 3:
                         fullhouse = True
                         
                if (fullhouse):
                    hex_string = 'FFFF' + hex_string
                else:    
                    hex_string = 'FFFFF' + hex_string
            elif (len_set == 1): # 5 of a kind
                hex_string = 'FFFFFF' + hex_string
                
            #hex_string = '0x' + hex_string
            #hex_string_list.append(hex_string)
            #hex2bid[hex_string] = line[1]
             
            int_val = int(hex_string, 16)
            int_list.append(int_val)
            if (int_val in int2bid):
                print("ERROR!")
            int2bid[int_val] = line[1]
            line = file.readline()
    
    int_list.sort()
    for idx, i in enumerate(int_list):
        #print(f'{int2bid[i]}*{idx+1}')
        output += (idx+1)*int(int2bid[i])
    
    return output

def most_common(lst):
    max_cnt = 0
    for l in lst:
        if lst.count(l) > max_cnt:
            max_cnt = lst.count(l)
            m = l
    return max_cnt, m

def process_inputs2(input_file):
    card2hex = {
        'J' : '0',
        '2' : '1',
        '3' : '2',
        '4' : '3',
        '5' : '4',
        '6' : '5',
        '7' : '6',
        '8' : '7',
        '9' : '8',
        'T' : '9',
        'Q' : 'A',
        'K' : 'B',
        'A' : 'C' 
        }

    output = 0

    int2bid = {}
    int_list = []
    with open(input_file) as file:
        line = file.readline()
        
        while line:
            line = line.strip()
        
            line = line.split()
            
            hex_string = ''
            for c in line[0]:
                hex_string = hex_string + card2hex[c]
            
            len_set = len(set(hex_string))
            max_cnt = 0
            if ('0' in hex_string):
                max_cnt, m = most_common(hex_string)
                
            if (len_set == 5): # high card
                if '0' in hex_string:
                    # upgrade to one pair
                    hex_string = 'F' + hex_string
                else:
                    hex_string = hex_string
            elif (len_set == 4): # one pair
                if hex_string.count('0') == 2:
                    # upgrade to 3 of a kind
                    hex_string = 'FFF' + hex_string
                elif hex_string.count('0') == 1:
                    # upgrade to 3 of a kind
                    hex_string = 'FFF' + hex_string
                else:
                    hex_string = 'F' + hex_string
            elif (len_set == 3): # two pair or 3 of a kind
                twopair = False
                for h in hex_string:
                    if hex_string.count(h) == 2:
                        twopair = True
                        
                if (twopair): # two pair
                    if hex_string.count('0') == 2:
                        # upgrade to four of a kind
                        hex_string = 'FFFFF' + hex_string
                    elif hex_string.count('0') == 1:
                        # upgrade to full house
                        hex_string = 'FFFF' + hex_string
                    else:
                        hex_string = 'FF' + hex_string
                else: # three of a kind
                    if hex_string.count('0') == 3:
                        # upgrade to four of a kind
                        hex_string = 'FFFFF' + hex_string
                    elif hex_string.count('0') == 1:
                        # upgrade to four of a kind
                        hex_string = 'FFFFF' + hex_string
                    else:
                        hex_string = 'FFF' + hex_string
            elif (len_set == 2): # full house or 4 of a kind
                fullhouse = False
                for h in hex_string:
                    if hex_string.count(h) == 3:
                         fullhouse = True
                         
                if (fullhouse):
                    if hex_string.count('0') == 3:
                        # upgrade to five of a kind
                        hex_string = 'FFFFFF' + hex_string
                    elif hex_string.count('0') == 2:
                        # upgrade to five of a kind
                        hex_string = 'FFFFFF' + hex_string
                    else:
                        hex_string = 'FFFF' + hex_string
                else:
                    if hex_string.count('0') == 4:
                        # upgrade to five of a kind
                        hex_string = 'FFFFFF' + hex_string
                    elif hex_string.count('0') == 1:
                        # upgrade to five of a kind
                        hex_string = 'FFFFFF' + hex_string
                    else:
                        hex_string = 'FFFFF' + hex_string
            elif (len_set == 1): # 5 of a kind
                hex_string = 'FFFFFF' + hex_string
                
            #hex_string = '0x' + hex_string
            #hex_string_list.append(hex_string)
            #hex2bid[hex_string] = line[1]
             
            int_val = int(hex_string, 16)
            int_list.append(int_val)
            if (int_val in int2bid):
                print("ERROR!")
            int2bid[int_val] = line[1]
            line = file.readline()
    
    int_list.sort()
    for idx, i in enumerate(int_list):
        output += (idx+1)*int(int2bid[i])
    
    return output

part1_example = 0
part1 = 0

part1_example = process_inputs('example7.txt')
part1 = process_inputs('input7.txt')

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')

part2_example = 0
part2 = 0

part2_example = process_inputs2('example7.txt')
part2 = process_inputs2('input7.txt')

print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
