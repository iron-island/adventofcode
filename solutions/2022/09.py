# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 17:45:49 2022

@author: AIson
"""

input_file = "../../inputs/2022/input09.txt"
#input_file = "example09.txt"

visited_list = []

rope_size = 10
init = 0

rope = []
for i in range(1, rope_size+1):
    rope.append([init, init])
visited_list.append([init, init])

def move_rope(rope, direction, head, tail):
    h = rope[head].copy()
    t = rope[tail].copy()
    
    if t[0] not in range(h[0]-1, h[0]+2) or \
       t[1] not in range(h[1]-1, h[1]+2):
        
        if (h[0] > t[0]):
            rope[tail][0] = t[0] + 1
        elif(h[0] < t[0]):
            rope[tail][0] = t[0] - 1            
            
        if (h[1] > t[1]):
            rope[tail][1] = t[1] + 1
        elif (h[1] < t[1]):
            rope[tail][1] = t[1] - 1
            
with open(input_file) as txtfile:
    txtfile_line = txtfile.readline()
    
    while txtfile_line:
        txtfile_line = txtfile_line.strip()
        parsed_line = txtfile_line.split(" ")
        
        # process
        direction = parsed_line[0]
        steps = int(parsed_line[1])
        for i in range(1, steps+1):
            # always move the head
            if (direction == 'U'):
                rope[0][0] = rope[0][0] + 1
            elif (direction == 'D'):
                rope[0][0] = rope[0][0] - 1
            elif (direction == 'L'):
                rope[0][1] = rope[0][1] - 1
            elif (direction == 'R'):
                rope[0][1] = rope[0][1] + 1
                
            for idx_rope in range(1, len(rope)):
                move_rope(rope, direction, idx_rope-1, idx_rope)
                
            tail = rope[-1].copy()
            if (tail not in visited_list):
                visited_list.append(tail)
                
        # read next line
        txtfile_line = txtfile.readline()

print(visited_list)        
print(f'visited = {len(visited_list)}')
