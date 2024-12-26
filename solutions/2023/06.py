import re
input_file = "../../inputs/2023/input06.txt"
example_file = "example06.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 1

    ways_list = []
    with open(in_file) as file:
        line = file.readline()
        line = line.strip()
        time = re.findall(r'\d+', line)

        line = file.readline()
        line = line.strip()
        distance = re.findall(r'\d+', line)

    for idx, t in enumerate(time):
        t_int = int(t)
        d_int = int(distance[idx])

        ways = 0
        for speed in range(0, t_int):
            time_left = (t_int - speed)
            possible_distance = speed*time_left

            if (possible_distance > d_int):
                ways += 1

        output = output*ways

    return output

def process_inputs2(in_file):
    output = 1

    with open(in_file) as file:
        line = file.readline()
        line = line.strip()
        time = ''.join(re.findall(r'\d+', line))

        line = file.readline()
        line = line.strip()
        distance = ''.join(re.findall(r'\d+', line))

    t_int = int(time)
    d_int = int(distance)

    ways = 0
    for speed in range(0, t_int):
        time_left = (t_int - speed)
        possible_distance = speed*time_left

        if (possible_distance > d_int):
            ways += 1

    output = output*ways

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
