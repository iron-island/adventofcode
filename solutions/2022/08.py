# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 18:36:24 2022

@author: AIson
"""

def get_score(views, tree):
    
    score = 0
    for i in views:
        if (tree > i):
            score = score + 1
        else:
            score = score + 1
            break
        
    return score

input_file = "../../inputs/2022/input08.txt"
#input_file = "example08.txt"

grid = []

with open(input_file) as txtfile:
    txtfile_line = txtfile.readline()
    
    while txtfile_line:
        # parse
        txtfile_line = txtfile_line.strip()
        int_line = [int(x) for x in txtfile_line]
        grid.append(int_line)
        
        # read next line
        txtfile_line = txtfile.readline()

# process
visible_trees = 2*len(grid) + 2*(len(grid[0]) - 2)
max_scenic_score = 0
max_left = 10
max_right = 10
max_up = 10
max_down = 10
print(grid)
for idxr, row in enumerate(grid):
    for idxc, y in enumerate(row):
        col = []
        for line in grid:
            col.append(line[idxc])

        up = col[0:idxr]
        down = col[(idxr+1):]        
        if (idxr > 0) and (idxr < len(row)-1):
            max_up = max(up)
            max_down = max(down)
        left = row[0:idxc]
        right = row[(idxc+1):]
        if (idxc > 0) and (idxc < len(col)-1):
            max_left = max(left)
            max_right = max(right)

        if (idxr > 0) and (idxr < (len(grid) - 1)) \
            and (idxc > 0) and (idxc < (len(col) - 1)):
                 if (y > max_up) or (y > max_down) or \
                     (y > max_left) or (y > max_right):
                        visible_trees = visible_trees + 1
                        #print(f'(x,y): {idxr},{idxc}')
                        #print(f'{y}')
                        #print(f'max_up = {max_up} from {up}')
                        #print(f'max_down = {max_down} from {down}')
                        #print(f'max_left = {max_left} from {left}')
                        #print(f'max_right = {max_right} from {right}')
                        
        # compute score
        up_score = 0
        down_score = 0
        left_score = 0
        right_score = 0
        up_score = get_score(reversed(up), y)
        down_score = get_score(down, y)
        left_score = get_score(reversed(left), y)
        right_score = get_score(right, y)
        
        scenic_score = up_score * down_score * left_score * right_score
        
            
        if (scenic_score > max_scenic_score):
            max_scenic_score = scenic_score
            
        # DEBUG
        if (scenic_score == 12):
            print(f'y = {y} from ({idxr}, {idxc})')
            print(f'up_score = {up_score}')
            print(f'down_score = {down_score}')
            print(f'left_score = {left_score}')
            print(f'right_score = {right_score}')
                        
print(f'p1: {visible_trees}')
print(f'p2: {max_scenic_score}')
