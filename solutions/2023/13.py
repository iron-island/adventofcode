import numpy as np
import math

# a = np.flip()
# a = np.vstack((a, [...]))
# (a==b).all()

input_file = "../../inputs/2023/input13.txt"
example_file = "example13.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

smudge_dict = {'#': '.', '.': '#'}

def find_symmetry(b):
    # matching rows
    a = np.array(b)
    symmetric = 0
    total_rows = len(a)
    for r in range(1, math.ceil(total_rows/2)):
        # top rows first
        top = a[0:r]
        bottom = a[r:(r+r)]
        flipb = np.flip(bottom, axis=0)
        #print(f'Row {r}')
        #print(f'  top =\n{top}')
        #print(f'  bot =\n{bottom}')
        #print(f'flipb =\n{np.flip(bottom, axis=0)}')
        s_array = (top==np.flip(bottom, axis=0))
        symmetric = s_array.all()
    
        if (symmetric):
        #    print(f'  Row {r} is symmetric!')
            return 'h'
    
        # bottom rows next
        top = np.flip(a,axis=0)[0:r]
        bottom = np.flip(a,axis=0)[r:(r+r)]
        flipb = np.flip(bottom, axis=0)
        #print(f'Row {r}')
        #print(f'  top =\n{top}')
        #print(f'  bot =\n{bottom}')
        #print(f'flipb =\n{np.flip(bottom, axis=0)}')
        s_array = (top==np.flip(bottom, axis=0))
        symmetric = s_array.all()
    
        if (symmetric):
        #    print(f'  Row {r} is symmetric!')
            return 'h'

    # matching columns
    a = np.array(b).T
    symmetric = 0
    total_rows = len(a)
    for r in range(1, math.ceil(total_rows/2)):
        # top rows first
        top = a[0:r]
        bottom = a[r:(r+r)]
        flipb = np.flip(bottom, axis=0)
        #print(f'Row {r}')
        #print(f'  top =\n{top}')
        #print(f'  bot =\n{bottom}')
        #print(f'flipb =\n{np.flip(bottom, axis=0)}')
        s_array = (top==np.flip(bottom, axis=0))
        symmetric = s_array.all()
    
        if (symmetric):
        #    print(f'  Row {r} is symmetric!')
            return 'v'
    
        # bottom rows next
        top = np.flip(a,axis=0)[0:r]
        bottom = np.flip(a,axis=0)[r:(r+r)]
        flipb = np.flip(bottom, axis=0)
        #print(f'Row {r}')
        #print(f'  top =\n{top}')
        #print(f'  bot =\n{bottom}')
        #print(f'flipb =\n{np.flip(bottom, axis=0)}')
        s_array = (top==np.flip(bottom, axis=0))
        symmetric = s_array.all()
    
        if (symmetric):
        #    print(f'  Row {r} is symmetric!')
            return 'v'

def process_inputs(in_file):
    output = 0

    blocks_2darray = []
    with open(in_file) as file:
        line = file.readline()
    
        blocks_array = []
        while line:
            line = line.strip()

            if (line == ""):
                blocks_2darray.append(blocks_array)
                line = file.readline()
                blocks_array = []
                continue
            else:
                row = [x for x in line]
                blocks_array.append(row)

            line = file.readline()
        blocks_2darray.append(blocks_array)

    for b in blocks_2darray:

        # matching rows
        a = np.array(b)
        symmetric = 0
        total_rows = len(a)
        for r in range(1, math.ceil(total_rows/2)):
            # top rows first
            top = a[0:r]
            bottom = a[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            print(f'Row {r}')
            print(f'  top =\n{top}')
            print(f'  bot =\n{bottom}')
            print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + 100*r

            # bottom rows next
            top = np.flip(a,axis=0)[0:r]
            bottom = np.flip(a,axis=0)[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            print(f'Row {r}')
            print(f'  top =\n{top}')
            print(f'  bot =\n{bottom}')
            print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + 100*(total_rows - r)

        # matching columns
        a = np.array(b).T
        symmetric = 0
        total_rows = len(a)
        for r in range(1, math.ceil(total_rows/2)):
            # top rows first
            top = a[0:r]
            bottom = a[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            print(f'Row {r}')
            print(f'  top =\n{top}')
            print(f'  bot =\n{bottom}')
            print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + r

            # bottom rows next
            top = np.flip(a,axis=0)[0:r]
            bottom = np.flip(a,axis=0)[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            print(f'Row {r}')
            print(f'  top =\n{top}')
            print(f'  bot =\n{bottom}')
            print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + (total_rows - r)

    return output

def process_inputs2(in_file):
    output = 0

    blocks_2darray = []
    with open(in_file) as file:
        line = file.readline()
    
        blocks_array = []
        while line:
            line = line.strip()

            if (line == ""):
                blocks_2darray.append(blocks_array)
                line = file.readline()
                blocks_array = []
                continue
            else:
                row = [x for x in line]
                blocks_array.append(row)

            line = file.readline()
        blocks_2darray.append(blocks_array)

    for b in blocks_2darray:
        smudge_found = False

        # matching rows
        a = np.array(b)
        symmetric = 0
        total_rows = len(a)
        for r in range(1, math.ceil(total_rows/2)):
            # top rows first
            top = a[0:r]
            bottom = a[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            s_array = (top==np.flip(bottom, axis=0))
            symmetric = s_array.all()

            #if (symmetric):
            #    print(f'  Row {r} is symmetric!')
            #    output = output + 100*r
            _, counts = np.unique(s_array, return_counts=True)
            pos = np.where(s_array==False)
            #row = pos[0][0]
            #col = pos[1][0]
            if (counts[0] == 1):
                # No transformation needed
                smudge_found = True
                print(f'Found smudge on {pos}! r = {r}')
                output = output + 100*r
                break

            # bottom rows next
            top = np.flip(a,axis=0)[0:r]
            bottom = np.flip(a,axis=0)[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            s_array = (top==np.flip(bottom, axis=0))
            symmetric = s_array.all()

            #if (symmetric):
            #    print(f'  Row {r} is symmetric!')
            #    output = output + 100*(total_rows - r)
            _, counts = np.unique(s_array, return_counts=True)
            pos = np.where(s_array==False)
            #row = pos[0][0]
            #col = pos[1][0]
            if (counts[0] == 1):
                # Transform needed
                print(f'Found smudge on {pos}! Transform 1 needed')
                smudge_found = True
                output = output + 100*(total_rows - r)
                break

        if (smudge_found):
            continue

        # matching columns
        a = np.array(b).T
        symmetric = 0
        total_rows = len(a)
        for r in range(1, math.ceil(total_rows/2)):
            # top rows first
            top = a[0:r]
            bottom = a[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            s_array = (top==np.flip(bottom, axis=0))
            symmetric = s_array.all()

            #if (symmetric):
            #    print(f'  Row {r} is symmetric!')
            #    output = output + r
            _, counts = np.unique(s_array, return_counts=True)
            pos = np.where(s_array==False)
            if (counts[0] == 1):
                print(f'Found smudge on {pos}! Transform 2 needed')
                smudge_found = True
                output = output + r
                break

            # bottom rows next
            top = np.flip(a,axis=0)[0:r]
            bottom = np.flip(a,axis=0)[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            s_array = (top==np.flip(bottom, axis=0))
            symmetric = s_array.all()

            #if (symmetric):
            #    print(f'  Row {r} is symmetric!')
            #    output = output + (total_rows - r)
            _, counts = np.unique(s_array, return_counts=True)
            pos = np.where(s_array==False)
            if (counts[0] == 1):
                print(f'Found smudge on {pos}! Transform 3 needed')
                smudge_found = True
                output = output + (total_rows-r)
                break

    return output

    # Rerun with smudges fixed
    output = 0
    for b in blocks_2darray:

        # matching rows
        a = np.array(b)
        symmetric = 0
        total_rows = len(a)
        for r in range(1, math.ceil(total_rows/2)):
            # top rows first
            top = a[0:r]
            bottom = a[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + 100*r

            # bottom rows next
            top = np.flip(a,axis=0)[0:r]
            bottom = np.flip(a,axis=0)[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + 100*(total_rows - r)

        # matching columns
        a = np.array(b).T
        symmetric = 0
        total_rows = len(a)
        for r in range(1, math.ceil(total_rows/2)):
            # top rows first
            top = a[0:r]
            bottom = a[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + r

            # bottom rows next
            top = np.flip(a,axis=0)[0:r]
            bottom = np.flip(a,axis=0)[r:(r+r)]
            flipb = np.flip(bottom, axis=0)
            #print(f'Row {r}')
            #print(f'  top =\n{top}')
            #print(f'  bot =\n{bottom}')
            #print(f'flipb =\n{np.flip(bottom, axis=0)}')
            symmetric = (top==np.flip(bottom, axis=0)).all()

            if (symmetric):
                print(f'  Row {r} is symmetric!')
                output = output + (total_rows - r)

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
