import random
import math

from sympy import solve
from sympy.abc import x, y, z, u, v, w, a, b, c

input_file = "../../inputs/2023/input24.txt"
example_file = "example24.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def compute_pos(t, pos_tuple, vel_tuple):
    x, y, z = pos_tuple
    vx, vy, vz = vel_tuple

    new_x = x + vx*t
    new_y = y + vy*t
    new_z = z + vz*t

    return (new_x, new_y, new_z)

def process_inputs(in_file, MIN_POS=200000000000000, MAX_POS=400000000000000):
    output = 0

    hail_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            pos, vel = line.split(" @ ")
            pos_float = [float(p) for p in pos.split(", ")]
            vel_float = [float(v) for v in vel.split(", ")]
            hail_list.append(pos_float + vel_float)

            line = file.readline()

    len_hail_list = len(hail_list)
    for idx_h1, h1 in enumerate(hail_list):
        x1, y1, z1, vx1, vy1, vz1 = h1

        m1 = vy1/vx1

        for idx_h2 in range(idx_h1+1, len_hail_list):
            h2 = hail_list[idx_h2]

            x2, y2, z2, vx2, vy2, vz2 = h2
            m2 = vy2/vx2

            # Eq 1: y = (vy1/vx1)*(x - x1) + y1
            # Eq 2: y = (vy2/vx2)*(x - x2) + y2
            #m1*x - m1*x1 + y1 = m2*x - m2*x2 + y2
            #(m1-m2)*x = m1*x1 - m2*x2 + y2 - y1
            m_diff = m1-m2
            if (m_diff == 0):
                # in case they are parallel, and already intersect
                if (x1 == x2) and (y1 == y2) and (x1 >= MIN_POS) and (x1 <= MAX_POS) and (y1 >= MIN_POS) and (y1 <= MAX_POS):
                    output += 1
                continue

            x = (m1*x1 - m2*x2 + y2 - y1)/m_diff
            y = m1*(x-x1) + y1

            #print(f'Hailstone A: {h1}')
            #print(f'Hailstone B: {h2}')
            #print(f'Intersection (x, y): {x}, {y}')
            IN_TEST_AREA = (x >= MIN_POS) and (x <= MAX_POS) and (y >= MIN_POS) and (y <= MAX_POS)
            IN_H1_FUTURE = (not ((x >= x1) and (vx1 < 0))) and (not ((x <= x1) and (vx1 > 0))) and (not ((y >= y1) and (vy1 < 0))) and (not ((y <= y1) and (vy1 > 0)))
            IN_H2_FUTURE = (not ((x >= x2) and (vx2 < 0))) and (not ((x <= x2) and (vx2 > 0))) and (not ((y >= y2) and (vy2 < 0))) and (not ((y <= y2) and (vy2 > 0)))
            if IN_TEST_AREA and IN_H1_FUTURE and IN_H2_FUTURE:
                #print("INSIDE")
                output += 1

    return output

def process_inputs2(in_file, RAND_TIMES=[]):
    output = 0

    hail_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            pos, vel = line.split(" @ ")
            pos_float = [float(p) for p in pos.split(", ")]
            vel_float = [float(v) for v in vel.split(", ")]
            hail_list.append(pos_float + vel_float)

            line = file.readline()

    len_hail_list = len(hail_list)

    # Solve via sympy
    # Using 3 hailstones to have 9 equations with 9 unknowns:
    # x, y, z = rock position
    # u, v, w = rock velocities
    # a, b, c = time when it collides with 3 hailstones
    x1, y1, z1, vx1, vy1, vz1 = hail_list[0]
    x2, y2, z2, vx2, vy2, vz2 = hail_list[1]
    x3, y3, z3, vx3, vy3, vz3 = hail_list[2]
    equations = [x1 + a*vx1 - x - a*u, \
                 x2 + b*vx2 - x - b*u, \
                 x3 + c*vx3 - x - c*u, \
                 y1 + a*vy1 - y - a*v, \
                 y2 + b*vy2 - y - b*v, \
                 y3 + c*vy3 - y - c*v, \
                 z1 + a*vz1 - z - a*w, \
                 z2 + b*vz2 - z - b*w, \
                 z3 + c*vz3 - z - c*w, \
                ]
    solutions = solve(equations, [x, y, z, u, v, w, a, b, c], dict=True)
    output = int(solutions[0][x] + solutions[0][y] + solutions[0][z])

    '''
    while True:
        t1_pos_list = []
        t2_pos_list = []
        t3_pos_list = []

        randtimes = []
        for i in range(0, 3):
            while True:
                #randtime = random.randint(1, len_hail_list) # arbitrary, not necessarily enough
                randtime = random.randint(1, 1e6) # arbitrary, not necessarily enough
                if randtime not in randtimes:
                    randtimes.append(randtime)
                    break

        randtimes = sorted(randtimes)
        print(f'Trying {randtimes}...')

        #for idx, t in enumerate([1, math.ceil(len_hail_list/2), len_hail_list]):
        for idx, t in enumerate(randtimes):
            for h in hail_list:
                x, y, z, vx, vy, vz = h

                new_pos = compute_pos(t, (x, y, z), (vx, vy, vz))

                if (idx == 0):
                    t1_pos_list.append(new_pos)
                elif (idx == 1):
                    t2_pos_list.append(new_pos)
                elif (idx == 2):
                    t3_pos_list.append(new_pos)

        for idx1, p1 in enumerate(t1_pos_list):
            x1, y1, z1 = p1

            for idx2, p2 in enumerate(t2_pos_list):
                x2, y2, z2 = p2

                if (idx2 == idx1) or (x2 == x1):
                    continue

                m_y_21 = (y2 - y1)/(x2 - x1)
                m_z_21 = (z2 - z1)/(x2 - x1)

                for idx3, p3 in enumerate(t3_pos_list):
                    x3, y3, z3 = p3

                    if (idx3 == idx2) or (idx3 == idx1) or (x3 == x1):
                        continue

                    m_y_31 = (y3 - y1)/(x3-x1)
                    m_z_31 = (z3 - z1)/(x3-x1)

                    if (m_y_31 == m_y_21) and (m_z_31 == m_z_21):
                        print(f'Found line! Times are {randtimes}')
                        return
    '''

    return output

#part1_example = process_inputs(example_file, 7, 27)
#part1 = process_inputs(input_file)

part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file, [9, 86, 223])

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
