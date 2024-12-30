import numpy as np
import math
from functools import cache
from collections import defaultdict

input_file = "../../inputs/2021/input19.txt"
example_file = "example19.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

test1 = [
(-618,-824,-621),
(-537,-823,-458),
(-447,-329,318),
(404,-588,-901),
(544,-627,-890),
(528,-643,409),
(-661,-816,-575),
(390,-675,-793),
(423,-701,434),
(-345,-311,381),
(459,-707,401),
(-485,-357,347)
]

test2 = [
(686,422,578),
(605,423,415),
(515,917,-361),
(-336,658,858),
(-476,619,847),
(-460,603,-452),
(729,430,532),
(-322,571,750),
(-355,545,-477),
(413,935,-424),
(-391,539,-444),
(553,889,-390)
]

test_set = set([
(-892,524,684),
(-876,649,763),
(-838,591,734),
(-789,900,-551),
(-739,-1745,668),
(-706,-3180,-659),
(-697,-3072,-689),
(-689,845,-530),
(-687,-1600,576),
(-661,-816,-575),
(-654,-3158,-753),
(-635,-1737,486),
(-631,-672,1502),
(-624,-1620,1868),
(-620,-3212,371),
(-618,-824,-621),
(-612,-1695,1788),
(-601,-1648,-643),
(-584,868,-557),
(-537,-823,-458),
(-532,-1715,1894),
(-518,-1681,-600),
(-499,-1607,-770),
(-485,-357,347),
(-470,-3283,303),
(-456,-621,1527),
(-447,-329,318),
(-430,-3130,366),
(-413,-627,1469),
(-345,-311,381),
(-36,-1284,1171),
(-27,-1108,-65),
(7,-33,-71),
(12,-2351,-103),
(26,-1119,1091),
(346,-2985,342),
(366,-3059,397),
(377,-2827,367),
(390,-675,-793),
(396,-1931,-563),
(404,-588,-901),
(408,-1815,803),
(423,-701,434),
(432,-2009,850),
(443,580,662),
(455,729,728),
(456,-540,1869),
(459,-707,401),
(465,-695,1988),
(474,580,667),
(496,-1584,1900),
(497,-1838,-617),
(527,-524,1933),
(528,-643,409),
(534,-1912,768),
(544,-627,-890),
(553,345,-567),
(564,392,-477),
(568,-2007,-577),
(605,-1665,1952),
(612,-1593,1893),
(630,319,-379),
(686,-3108,-505),
(776,-3184,-501),
(846,-3110,-434),
(1135,-1161,1235),
(1243,-1093,1063),
(1660,-552,429),
(1693,-557,386),
(1735,-437,1738),
(1749,-1800,1813),
(1772,-405,1572),
(1776,-675,371),
(1779,-442,1789),
(1780,-1548,337),
(1786,-1538,337),
(1847,-1591,415),
(1889,-1729,1762),
(1994,-1805,1792)
])

SIGNS_LIST = [1, -1]

@cache
def get_rot_mat(degree_tuple):
    dx, dy, dz = degree_tuple 

    tx = dx*(np.pi)/180
    ty = dy*(np.pi)/180
    tz = dz*(np.pi)/180

    cos_tx = int(math.cos(tx))
    sin_tx = int(math.sin(tx))
    cos_ty = int(math.cos(ty))
    sin_ty = int(math.sin(ty))
    cos_tz = int(math.cos(tz))
    sin_tz = int(math.sin(tz))

    rot_x = np.array([[1, 0, 0],
                      [0, cos_tx, -sin_tx],
                      [0, sin_tx, cos_tx]])
    rot_y = np.array([[cos_ty, 0, sin_ty],
                      [0, 1, 0],
                      [-sin_ty, 0, cos_ty]])
    rot_z = np.array([[cos_tz, -sin_tz, 0],
                      [sin_tz, cos_tz, 0],
                      [0, 0, 1]])

    rot_mat = np.matmul(rot_y, rot_x)
    rot_mat = np.matmul(rot_z, rot_mat)

    inv_rot_mat = np.linalg.inv(rot_mat)

    return rot_mat, inv_rot_mat

def rotate(rot_mat, vec_tuple):
    in_vec = np.array([[vec_tuple[0]],
                       [vec_tuple[1]],
                       [vec_tuple[2]]])

    out_vec = np.matmul(rot_mat, in_vec)
    out_vec.shape = (3,)
    out_vec = tuple(np.round(out_vec).astype(int).tolist())

    return out_vec

def get_dist(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2

    diff_x = (x1 - x2)
    diff_y = (y1 - y2)
    diff_z = (z1 - z2)
    #diff_x = (x2 - x1)
    #diff_y = (y2 - y1)
    #diff_z = (z2 - z1)

    return diff_x, diff_y, diff_z

def get_abs_dist(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2

    diff_x = abs(x1 - x2)
    diff_y = abs(y1 - y2)
    diff_z = abs(z1 - z2)

    return diff_x + diff_y + diff_z

def process_inputs(in_file, part2=False):
    output = 0

    scanner_dict = defaultdict(list)
    num_beacons = 0
    unique_beacons_dict = defaultdict(list)
    with open(in_file) as file:
        line = file.readline()
    
        beacon_list = []
        scanner = ""
        while line:
            line = line.strip()

            if ("scanner" in line):
                beacon_list = []
                scanner = line.split(" ")[2]
            elif (line != ""):
                b_tuple = tuple([int(x) for x in line.split(",")])
                beacon_list.append(b_tuple)
                num_beacons += 1

                unique_beacons_dict[b_tuple] = []
            else:
                scanner_dict[scanner] = beacon_list

            line = file.readline()
        scanner_dict[scanner] = beacon_list

    #scan_oct_dict = defaultdict(dict)
    #for scanner in scanner_dict:
    #    flat_list = scanner_dict[scanner]
    #    oct_dict = defaultdict(list)

    #    # Arrange by octants
    #    for coords in flat_list:
    #        for x_min in SIGNS_LIST:
    #            for y_min in SIGNS_LIST:
    #                for z_min in SIGNS_LIST:
    #                    x, y, z = coords

    #                    if (x*x_min > 0) and (y*y_min >= 0) and (z*z_min >= 0):
    #                        oct_dict[(x_min, y_min, z_min)].append(coords)

    #    # Record
    #    scan_oct_dict[scanner] = oct_dict

    # Check scanners and beacons
    #init_beacons = num_beacons
    #print(f'Initial number of beacons: {init_beacons}')
    #scanners_list = list(scanner_dict.keys())
    #offset_dict = defaultdict(list)
    #for idx1, scanner1 in enumerate(scanners_list[:-1]):
    #    beacon1_list = scanner_dict[scanner1]
    #    for scanner2 in scanners_list[idx1+1:]:

    #        beacon2_list = scanner_dict[scanner2]

    #        # x
    #        for idx_x in [0, 1, 2]:
    #            for sx in SIGNS_LIST:

    #                # y
    #                for idx_y in [0, 1, 2]:
    #                    if (idx_x == idx_y):
    #                        continue
    #                    for sy in SIGNS_LIST:

    #                        # z
    #                        for idx_z in [0, 1, 2]:
    #                            if (idx_z == idx_y) or (idx_z == idx_x):
    #                                continue

    #                            for sz in SIGNS_LIST:

    #                                temp_list = []
    #                                for beacon in beacon2_list:
    #                                    x, y, z = beacon
    #                                    temp = [0, 0, 0]

    #                                    temp[idx_x] = x*sx
    #                                    temp[idx_y] = y*sy
    #                                    temp[idx_z] = z*sz

    #                                    temp_list.append(temp)

    #                                # Check distances
    #                                dist_list = []
    #                                temp_dict = defaultdict(list)
    #                                for beacon1 in beacon1_list:
    #                                    for beacon2 in temp_list:
    #                                        dist = get_dist(beacon1, beacon2)
    #                                        dist_list.append(dist)
    #                                        temp_dict[dist].append((beacon1, beacon2))

    #                                dist_set = set(dist_list)
    #                                if (len(dist_set)+11 <= len(dist_list)):
    #                                    final_dist_list = []
    #                                    for dist in temp_dict:
    #                                        dist_count = len(temp_dict[dist])
    #                                        if (dist_count >= 12):
    #                                            #num_beacons += dist_count
    #                                            num_beacons -= dist_count
    #                                            print(dist_count)
    #                                            final_dist_list.append(dist)

    #                                    assert(len(final_dist_list) <= 1)
    #                                    if (len(final_dist_list)):
    #                                        x, y, z = final_dist_list[0]
    #                                        #offset_dict[scanner1].append((scanner2, x, y, z, idx_x, idx_y, idx_z, sx, sy, sz))
    #                                        rel_offset = [0, 0, 0]
    #                                        rel_offset[idx_x] = x
    #                                        rel_offset[idx_y] = y
    #                                        rel_offset[idx_z] = z

    #                                        rel_sign = [0, 0, 0]
    #                                        rel_sign[idx_x] = sx
    #                                        rel_sign[idx_y] = sy
    #                                        rel_sign[idx_z] = sz

    #                                        offset_dict[scanner1].append((scanner2, rel_offset, rel_sign))
    #                                        print((x, y, z), (idx_x, idx_y, idx_z), (sx, sy, sz))
    #                                        print(scanner1, scanner2, rel_offset, rel_sign)

    ## Recompute offsets wrt scanner 0
    #print(offset_dict)
    #final_offset_dict = defaultdict(tuple)
    #final_offset_dict["0"] = ((0, 0, 0), (1, 1, 1))
    #for scanner1 in offset_dict:
    #    for offset in offset_dict[scanner1]:
    #        #scanner2, x2, y2, z2, sx2, sy2, sz2 = offset
    #        scanner2, rel_offset2, rel_sign2 = offset
    #        x2, y2, z2 = rel_offset2
    #        sx2, sy2, sz2 = rel_sign2

    #        if (scanner1 in final_offset_dict) and (scanner2 not in final_offset_dict):
    #            rel_offset1, rel_sign1 = final_offset_dict[scanner1]
    #            x1, y1, z1 = rel_offset1
    #            sx1, sy1, sz1 = rel_sign1
    #            final_offset_dict[scanner2] = ((x1+sx1*x2, y1+sy1*y2, z1+sz1*z2), (sx2, sy2, sz2))

    #print(final_offset_dict)

    # DEBUG
    #for sx in SIGNS_LIST:
    #    for sy in SIGNS_LIST:
    #        for sz in SIGNS_LIST:
    #            temp_list = []
    #            for t2 in test2:
    #                x, y, z = t2
    #                temp_list.append((x*sx, y*sy, z*sz))

    #            test1.sort()
    #            temp_list.sort()
    #            dist_list = list(map(get_dist, test1, temp_list))
    #            dist_set = set(dist_list)
    #            if ((len(dist_set)+11) <= len(dist_list)):
    #                print(sx, sy, sz)
    #                print(dist_set)

    # Precompute rotation matrices
    degree_list = [0, 90, 180, 270]
    out_set = set()
    degree_tuple_list = []
    for dx in degree_list:
        for dy in degree_list:
            for dz in degree_list:
                # Compute rotation
                rot_mat, inv_rot_mat = get_rot_mat((dx, dy, dz))
                out_vec = rotate(rot_mat, (1, 2, 3))
    
                if (out_vec not in out_set):
                    out_set.add(out_vec)
                    degree_tuple_list.append((dx, dy, dz))

    # Check scanners and beacons
    init_beacons = num_beacons
    print(f'Initial number of beacons: {init_beacons}')
    scanners_list = list(scanner_dict.keys())
    offset_dict = defaultdict(list)
    #for idx1, scanner1 in enumerate(scanners_list[:-1]):
    for idx1, scanner1 in enumerate(scanners_list):
        beacon1_list = scanner_dict[scanner1]
        #for scanner2 in scanners_list[idx1+1:]:
        for idx2, scanner2 in enumerate(scanners_list):
            if (idx1 == idx2):
                continue

            beacon2_list = scanner_dict[scanner2]

            for degree_tuple in degree_tuple_list:
                rot_mat, inv_rot_mat = get_rot_mat(degree_tuple)

                temp_list = []
                for beacon in beacon2_list:
                    temp = rotate(rot_mat, beacon)

                    temp_list.append(temp)

                # Check distances
                dist_list = []
                temp_dict = defaultdict(list)
                for beacon1 in beacon1_list:
                    for beacon2 in temp_list:
                        dist = get_dist(beacon1, beacon2)
                        dist_list.append(dist)
                        temp_dict[dist].append((beacon1, beacon2))

                dist_set = set(dist_list)
                if (len(dist_set)+11 <= len(dist_list)):
                    final_dist_list = []
                    for dist in temp_dict:
                        dist_count = len(temp_dict[dist])
                        if (dist_count >= 12):
                            num_beacons -= dist_count
                            #print(f'dist_count = {dist_count}')
                            final_dist_list.append(dist)

                    assert(len(final_dist_list) <= 1)
                    if (len(final_dist_list)):
                        dist = final_dist_list[0]
                        inv_dist = rotate(inv_rot_mat, dist)
                        #print(f'degrees: {degree_tuple}')
                        #print(f'dist     = {dist}')
                        #print(f'inv_dist = {inv_dist}')

                        # Record
                        offset_dict[scanner1].append((scanner2, dist, rot_mat))

    # Recompute offsets wrt scanner 0
    output = num_beacons
    abs_offset_dict = defaultdict(tuple)
    abs_offset_dict["0"] = ((0, 0, 0), ())
    print(offset_dict)
    while True:
        changed = False
        for scanner1 in offset_dict:
            for offset in offset_dict[scanner1]:
                scanner2, dist, rot_mat = offset

                if (scanner1 in abs_offset_dict) and (scanner2 not in abs_offset_dict):
                    prev_dist, prev_rot_mat = abs_offset_dict[scanner1]
                    x1, y1, z1 = prev_dist
                    x2, y2, z2 = dist

                    if (scanner1 != "0"):
                        # Apply rotation on the relative offset
                        x2, y2, z2 = rotate(prev_rot_mat, dist)
                        vec_tuple = (x1+x2, y1+y2, z1+z2)

                        # TEST
                        tot_rot_mat = np.matmul(rot_mat, prev_rot_mat)
                        tot_rot_mat = np.matmul(prev_rot_mat, rot_mat) # WORKS1
                        #tot_rot_mat = prev_rot_mat
                        #tot_rot_mat = rot_mat

                        abs_offset_dict[scanner2] = (vec_tuple, tot_rot_mat)
                    else:
                        vec_tuple = (x1+x2, y1+y2, z1+z2)
                        abs_offset_dict[scanner2] = (vec_tuple, rot_mat)

                    changed = True
                #elif (scanner2 in abs_offset_dict) and (scanner1 not in abs_offset_dict):
                #    prev_dist, prev_rot_mat = abs_offset_dict[scanner2]
                #    x1, y1, z1 = prev_dist
                #    x2, y2, z2 = dist

                #    # TEST
                #    inv_rot_mat = np.linalg.inv(rot_mat)
                #    inv_prev_rot_mat = np.linalg.inv(prev_rot_mat)
                #    tot_rot_mat = np.matmul(rot_mat, prev_rot_mat)
                #    tot_rot_mat = np.matmul(prev_rot_mat, rot_mat) # WORKS1
                #    #tot_rot_mat = prev_rot_mat
                #    #tot_rot_mat = rot_mat
                #    #tot_rot_mat = inv_prev_rot_mat
                #    #tot_rot_mat = inv_rot_mat
                #    #tot_rot_mat = np.matmul(inv_rot_mat, prev_rot_mat)
                #    #tot_rot_mat = np.matmul(prev_rot_mat, inv_rot_mat)
                #    #tot_rot_mat = np.matmul(inv_prev_rot_mat, inv_rot_mat)
                #    #tot_rot_mat = np.matmul(inv_rot_mat, inv_prev_rot_mat)
                #    #tot_rot_mat = np.matmul(inv_prev_rot_mat, rot_mat)
                #    #tot_rot_mat = np.matmul(rot_mat, inv_prev_rot_mat)

                #    #x2, y2, z2 = rotate(tot_rot_mat, dist)
                #    #vec_tuple = (x1-x2, y1-y2, z1-z2)

                #    x2, y2, z2 = rotate(tot_rot_mat, dist)
                #    vec_tuple = (x1-x2, y1-y2, z1-z2)
                #    #vec_tuple = (x1+x2, y1+y2, z1+z2)
                #    #vec_tuple = (x2-x1, y2-y1, z2-z1)
                #    #x1, y1, z1 = rotate(tot_rot_mat, prev_dist)
                #    #vec_tuple = (x1-x2, y1-y2, z1-z2)
                #    #vec_tuple = (x1+x2, y1+y2, z1+z2)
                #    #vec_tuple = (x2-x1, y2-y1, z2-z1)

                #    abs_offset_dict[scanner1] = (vec_tuple, tot_rot_mat)

                #    changed = True
        if not (changed):
            break

    # DEBUGGING
    #for degree_tuple in degree_tuple_list:
    #    rot_mat, _ = get_rot_mat(degree_tuple)

    #    out_vec = rotate(rot_mat, (1125, -168, 72))
    #    if (out_vec == (-1125, 72, -168)):
    #        print("found!")

    print(abs_offset_dict)
    scanner_list1 = list(scanner_dict.keys())
    scanner_list2 = list(abs_offset_dict.keys())
    assert(set(scanner_list1) == set(scanner_list2))

    MAX_DIST = 0
    if (part2):
        for idx1, scanner1 in enumerate(scanners_list):
            for idx2, scanner2 in enumerate(scanners_list):
                coords1, _ = abs_offset_dict[scanner1]
                coords2, _ = abs_offset_dict[scanner2]

                MAX_DIST = max(MAX_DIST, get_abs_dist(coords1, coords2))

        output = MAX_DIST

        return output

    # Check all beacons wrt scanner 0
    beacon_set = set()
    for scanner in abs_offset_dict:
        if (scanner == "0"):
            for beacon in scanner_dict[scanner]:
                beacon_set.add(beacon)
            continue

        offset, rot_mat = abs_offset_dict[scanner]
        x, y, z = offset
        inv_rot_mat = np.linalg.inv(rot_mat)
        for beacon in scanner_dict[scanner]:
            x_r, y_r, z_r = rotate(rot_mat, beacon)

            new_beacon = (x+x_r, y+y_r, z+z_r)
            beacon_set.add(new_beacon)

    # DEBUG
    if (beacon_set == test_set):
        print(f'Passes example!')

    output = len(beacon_set)

    return output

part1_example = process_inputs(example_file)
part1 = process_inputs(input_file) # 442 correct answer
# 565 too high
# 564 incorrect
# 412 too low

part2_example = process_inputs(example_file, True)
part2 = process_inputs(input_file, True)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
