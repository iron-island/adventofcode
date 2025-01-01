from functools import cache

input_file = "../../inputs/2021/input21.txt"
example_file = "example21.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

MAX_SCORE = 21
MAX_POS = 10

@cache
def dfs_universes(player, pos_tuple, score_tuple):
    # Base case
    score1, score2 = score_tuple
    if (score1 >= MAX_SCORE):
        return 1, 0
    elif (score2 >= MAX_SCORE):
        return 0, 1

    # Recursion
    num1 = 0
    num2 = 0
    #for roll in range(1, 4):
    #    for die in range(1, 4):
    for roll1 in range(1, 4):
        for roll2 in range(1, 4):
            for roll3 in range(1, 4):
                # Reinitialize score and position for every universe's roll
                score_list = list(score_tuple)
                pos_list = list(pos_tuple)

                if (player == 1):
                    idx = 0
                    next_player = 2
                else:
                    idx = 1
                    next_player = 1

                # Move
                die = roll1 + roll2 + roll3
                pos = pos_list[idx] + die
                if ((pos % MAX_POS) == 0):
                    pos = MAX_POS
                else:
                    pos = (pos % MAX_POS)
                pos_list[idx] = pos

                # Score
                score_list[idx] += pos

                next_pos_tuple = tuple(pos_list)
                next_score_tuple = tuple(score_list)

                deeper_num1, deeper_num2 = dfs_universes(next_player, next_pos_tuple, next_score_tuple)
                num1 += deeper_num1
                num2 += deeper_num2

    return num1, num2

def process_inputs(in_file):
    output = 0

    pos_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            pos_list.append(int(line.split(" ")[-1]))

            line = file.readline()

    score_list = [0, 0]

    rolls = 0
    die = 0
    loser_score = 0
    while True:
        for idx in range(0, 2):
            moves = 0
            for i in range(0, 3):
                rolls += 1
                die += 1
                if (die > 100):
                    die = 1

                moves += die

            # Move
            pos = pos_list[idx] + moves
            if ((pos % 10) == 0):
                pos = 10
            else:
                pos = (pos % 10)
            pos_list[idx] = pos

            # Score
            score_list[idx] += pos

            # Check
            score1, score2 = score_list

            if (score1 >= 1000):
                loser_score = score2
                break
            elif (score2 >= 1000):
                loser_score = score1
                break
        if (loser_score):
            break

    output = loser_score*rolls

    return output

def process_inputs2(in_file):
    output = 0

    pos_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            pos_list.append(int(line.split(" ")[-1]))

            line = file.readline()

    # Play
    next_player = 1
    next_pos_tuple = tuple(pos_list)
    next_score_tuple = tuple([0, 0])
    print(next_pos_tuple)
    num1, num2 = dfs_universes(next_player, next_pos_tuple, next_score_tuple)

    print(num1, num2)
    output = max(num1, num2)

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
