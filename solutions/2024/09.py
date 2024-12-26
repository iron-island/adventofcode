input_file = "input9.txt"
example_file = "example9.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
def process_inputs(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            disk = line

            line = file.readline()

    # Compact
    compacted_disk = []
    id_num = 0
    blank_num = 0
    blank_string = ""
    for idx, d in enumerate(disk):
        d_int = int(d)
        if ((idx % 2) == 0): # file
            for i in range(0, d_int):
                compacted_disk.append(id_num)
            id_num += 1
        else: # blank
            for i in range(0, d_int):
                compacted_disk.append('.')
                blank_num += 1
                blank_string = blank_string + "."

    # Compact
    length = len(compacted_disk)
    compacted_string = ""
    iteration = 0
    while (True):
        if ((iteration % 1000) == 0):
            print(f'{iteration} of {blank_num}')
        iteration += 1

        compacted_string = [str(x) for x in compacted_disk]
        compacted_string = ''.join(compacted_string)
        #print(compacted_string)
        if (blank_string in compacted_string):
            break
        #if (compacted_disk[-blank_num:] == blank_string):
        #    break

        idx_from = 0
        for idx_reverse in range(1, length):
            num = compacted_disk[-idx_reverse]
            if (num != '.'):
                idx_from = idx_reverse
                break
        #print(num)

        # Move num
        for idx in range(0, length):
            blank = compacted_disk[idx]
            if (blank == '.'):
                compacted_disk[-idx_from] = blank
                compacted_disk[idx] = num
                #print(idx)
                break

    # Evaluate
    print(compacted_string)
    for idx, d in enumerate(compacted_disk):
        if (d == '.'):
            break

        output += idx*d

    return output

def process_inputs2(in_file):
    output = 0

    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            disk = line

            line = file.readline()

    # Compact
    compacted_disk = []
    id_num = 0
    blank_num = 0
    blank_string = ""
    for idx, d in enumerate(disk):
        d_int = int(d)
        if ((idx % 2) == 0): # file
            mydict = {}
            mydict[id_num] = d_int
            id_num += 1
            #for i in range(0, d_int):
            #    compacted_disk.append(id_num)
            #id_num += 1
        else: # blank
            mydict = {}
            mydict["blank"] = d_int
            #for i in range(0, d_int):
            #    compacted_disk.append('.')
            #    blank_num += 1
            #    blank_string = blank_string + "."
        compacted_disk.append(mydict)

    # Compact
    for id_num_reverse in range(id_num-1, -1, -1):
        #print(f'{id_num_reverse}: {compacted_disk}')

        # find file ID = id_num_reverse
        idx_file = -1
        num_file = -1
        for idx, mydict in enumerate(compacted_disk):
            myid = list(mydict.keys())[0]
            mynum = mydict[myid]

            if (myid == id_num_reverse):
                idx_file = idx
                num_file = mynum
                break

        # Find blank segments
        new_compacted_disk = compacted_disk
        for idx, mydict in enumerate(compacted_disk):
            myid = list(mydict.keys())[0]
            mynum = mydict[myid]

            if (myid == 'blank') and (idx < idx_file):
                # debugging
                #if (id_num_reverse == 7):
                #    print(f'blank: {mynum}')
                #    print(f'file:  {num_file}')

                if (mynum == num_file):
                    # Exchange if exact same length
                    new_compacted_disk[idx] = {id_num_reverse: num_file}
                    new_compacted_disk[idx_file] = {'blank': mynum}
                    break
                elif (mynum > num_file):
                    new_compacted_disk[idx] = {id_num_reverse: num_file}
                    new_compacted_disk[idx_file] = {'blank': num_file}
                    new_compacted_disk.insert(idx+1, {'blank': mynum-num_file})
                    break
        compacted_disk = new_compacted_disk

    # Evaluate
    actual_idx = 0
    for idx, mydict in enumerate(compacted_disk):
        myid = list(mydict.keys())[0]
        mynum = mydict[myid]

        if (myid != 'blank'):
            curr_sum = 0
            for i in range(actual_idx, actual_idx+mynum):
                partial_sum = i*myid
                curr_sum += partial_sum
                #print(partial_sum)
            output += curr_sum

        actual_idx += mynum

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
