# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

with open("../../inputs/2022/input02.txt") as txtfile:
    txtfile_line = txtfile.readline()
    
    score = 0
    round_score = 0
    opp = 0
    mine = 0
    while txtfile_line:
        # parse
        print(txtfile_line)
        opp = txtfile_line[0]
        mine = txtfile_line[2]
        
        #print(opp)
        #print(mine)
        # process
        if (mine == 'X'): # lose
            round_score = 0
            if (opp == 'A'): # rock -> scissors
                round_score = round_score + 3
            elif (opp == 'B'): # paper -> rock
                round_score = round_score + 1
            elif (opp == 'C'): # scissors -> paper
                round_score = round_score + 2
        elif (mine == 'Y'):
            round_score = 3
            if (opp == 'A'): # rock
                round_score = round_score + 1
            elif (opp == 'B'): # paper
                round_score = round_score + 2
            elif (opp == 'C'): # scissors
                round_score = round_score + 3
        elif (mine == 'Z'):
            round_score = 6
            if (opp == 'A'): # paper
                round_score = round_score + 2
            elif (opp == 'B'): # scissors
                round_score = round_score + 3
            elif (opp == 'C'): # rock
                round_score = round_score + 1
            
        score = score + round_score
        # read next line
        txtfile_line = txtfile.readline()
        
print(score)
