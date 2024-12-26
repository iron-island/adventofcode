import functools
import itertools

input_file = "../../inputs/2023/input12.txt"
example_file = "example12.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
DEBUG = False

def valid(candidate_symbol_list, number_list):

    string_list = ''.join(candidate_symbol_list)
    symbol_list = [x for x in string_list.split('.') if (x != '')]

    #print(f'string_list = {string_list}')
    #print(f'symbol_list = {symbol_list}')
    for idx, s in enumerate(symbol_list):
        if (s.count('#') != number_list[idx]):
            return False

    return True
class unique_element:
    def __init__(self,value,occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    eset=set(elements)
    listunique = [unique_element(i,elements.count(i)) for i in eset]
    u=len(elements)
    return perm_unique_helper(listunique,[0]*u,u-1)

def perm_unique_helper(listunique,result_list,d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d]=i.value
                i.occurrences-=1
                for g in  perm_unique_helper(listunique,result_list,d-1):
                    yield g
                i.occurrences+=1

def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)

def process_inputs(in_file):
    output = 0

    symbol_array = []
    number_array = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            init_symbol_list, init_number_list = line.split(" ")

            symbol_list = [x for x in init_symbol_list]
            number_list = [int(x) for x in init_number_list.split(",")]

            symbol_array.append(symbol_list)
            number_array.append(number_list)

            line = file.readline()

    #for idx, s in enumerate(symbol_array):
    #    print(s, end="")
    #    print(number_array[idx])

    for idx, symbol_list in enumerate(symbol_array):
        number_list = number_array[idx]

        total = sum(number_list)

        knowns = symbol_list.count('#')
        unknowns = symbol_list.count('?')

        unknown_broken = total - knowns

        init_arrangement = []
        if (unknown_broken == 0):
            output = output + 1
            continue
        for i in range(0, unknown_broken):
            init_arrangement.append('#')
        for i in range(0, unknowns-unknown_broken):
            init_arrangement.append('.')

        # Generate all possible arrangements, and evaluate if valid

        print(f'Generating permutations for {len(init_arrangement)}-length arrangement with {unknown_broken} unknown broken springs...')
        #permutations = set(itertools.permutations(init_arrangement))
        #permutations = list(perm_unique(init_arrangement))
        #print(f'Evaluating {len(permutations)} permutations...')
        print(f'Evaluating permutations...')

        num_valid = 0
        #for idx_p, p in enumerate(permutations):
        idx_p = 0
        for p in perm_unique(init_arrangement):
            cnt = 0
            candidate_symbol_list = symbol_list.copy()
            for idx_s, s in enumerate(symbol_list):
                if (s == '?'):
                    candidate_symbol_list[idx_s] = p[cnt]
                    cnt += 1

            if (valid(candidate_symbol_list, number_list)):
                num_valid += 1
                if (idx == 0):
                    print(f'Candidate {idx_p}: {candidate_symbol_list} is valid')

            idx_p += 1

        print(f'Row {idx}: {num_valid} arrangements')
        if (idx == 0):
            print(permutations)
        output = output + num_valid

    return output

def process_inputs2(in_file):
    output = 0

    symbol_array = []
    number_array = []
    with open(in_file) as file:
        line = file.readline()
    
        num_groupable = 0
        less_chunks = 0
        more_chunks = 0
        max_excess_chunks = 0 
        max_lacking_chunks = 0

        has_exact_springs = 0

        idx_max_excess = 0
        idx_exact_springs = 0
        while line:
            line = line.strip()

            init_symbol_list, init_number_list = line.split(" ")

            symbol_list = [x for x in init_symbol_list]
            number_list = [int(x) for x in init_number_list.split(",")]

            # 5 folds
            #symbol_array.append(symbol_list + ['?'] + symbol_list + ['?'] + symbol_list + ['?'] + symbol_list + ['?'] + symbol_list + ['.'])
            #number_array.append(number_list + number_list + number_list + number_list + number_list)
            # 2 folds
            #symbol_array.append(symbol_list + ['#'] + symbol_list + ['.'])
            #number_array.append(number_list + number_list)
            # 5 folds method 2
            #symbol_array.append(symbol_list + ['.'] + symbol_list + ['.'] + symbol_list + ['.'] + symbol_list + ['.'] + symbol_list + ['.'])
            #number_array.append(number_list + number_list + number_list + number_list + number_list)

            # 1 fold
            symbol_array.append(symbol_list + ['.'])
            number_array.append(number_list)

            symbol_string = ''.join(symbol_array[-1])
            groups = [x for x in symbol_string.split('.') if (x != '')]

            len_groups = len(groups)
            len_last_number_list = len(number_array[-1])
            idx_array = len(number_array)-1
            if (len_groups == len_last_number_list):
                num_groupable += 1
            elif (len_groups < len_last_number_list):
                less_chunks += 1
                max_lacking_chunks = max(max_lacking_chunks, len_last_number_list - len_groups)

                largest_spring = max(number_array[-1])
                s = ''
                for i in range(0, largest_spring):
                    s = s + '#'

                if (s in groups):
                    has_exact_springs += 1
                    print(f'Row {idx_array} has exact springs')
            else:
                more_chunks += 1 # one of the chunks is just .
                if (max_excess_chunks < (len_groups-len_last_number_list)):
                    max_excess_chunks = max(max_excess_chunks, len_groups - len_last_number_list)
                    idx_max_excess = idx_array

            line = file.readline()

    print(f'num_groupable {num_groupable}')
    print(f'less_chunks {less_chunks} with max_lacking_chunks = {max_lacking_chunks} from row {idx_max_excess} and exact springs = {has_exact_springs}')
    print(f'more_chunks {more_chunks}')
    print(f'max excess_chunks {max_excess_chunks}')

    for idx, s in enumerate(symbol_array):
        print(s, end="")
        print(number_array[idx])

    for idx, symbol_list in enumerate(symbol_array):
        number_list = number_array[idx]

        symbol_length = len(symbol_list)
        total = sum(number_list)
        print(symbol_length)

        knowns = symbol_list.count('#')
        unknowns = symbol_list.count('?')

        unknown_broken = total - knowns

        if (unknown_broken == 0):
            output = output + 1
            continue

        # Generate all possible arrangements, and evaluate if valid

        init_arrangement = []
        # Method 1
        for n in number_list:
            curr_group = ''
            for i in range(0, n):
                curr_group = curr_group + '#'

            init_arrangement.append(curr_group + '.')
        for i in range(0, symbol_length - total - len(number_list)):
            init_arrangement.append('.')

        # Method 2: sliding window?
        #offset_list = []
        #for idx, n in enumerate(number_list):
        #    left_nums = number_list[0:idx].copy()
        #    right_nums = number_list[idx:]
        #    right_nums.pop(0)

        #    left_sum = sum(left_nums)
        #    right_sum = sum(right_nums)

        #    l_offset = 0
        #    r_offset = 0
        #    if (left_sum):
        #        l_offset = left_sum + (left_sum-1)

        #    if (right_sum):
        #        r_offset = right_sum + (right_sum-1)

        #    offset_list = (l_offset, r_offset)

        print(f'Generating permutations for {len(init_arrangement)}-length arrangement with {unknown_broken} unknown broken springs...')
        #print(init_arrangement)
        # Method 1
        #permutations = list(perm_unique(init_arrangement))
        #print(f'Evaluating {len(permutations)} permutations...')

        # Method 2

        print(f'Evaluating permutations...')

        num_valid = 0
        idx_p = 0
        #for idx_p, p in enumerate(permutations):
        for p in perm_unique(init_arrangement):
            cnt = 0
            ifvalid = True
            candidate_symbol_list = ''.join(p)

            #if (idx == 2):
            #    print(f'Candidate  : {candidate_symbol_list}')
            #    print(f'Symbol list: {"".join(symbol_list)}')

            if (valid(candidate_symbol_list, number_list)):
                for idx_s, s in enumerate(symbol_list):
                    if (s in ['#', '.']) and (s != candidate_symbol_list[idx_s]):
                        ifvalid = False
                        break
            else:
                ifvalid = False

            if ifvalid:
                #if (idx == 2):
                #    print("Valid!")
                num_valid += 1
        #    for idx_s, s in enumerate(symbol_list):
        #        if (s == '?'):
        #            candidate_symbol_list[idx_s] = p[cnt]
        #            cnt += 1

        #    if (valid(candidate_symbol_list, number_list)):
        #        num_valid += 1
        #        if (idx == 0):
        #            print(f'Candidate {idx_p}: {candidate_symbol_list} is valid')

        print(f'Row {idx}: {num_valid} arrangements')
        output = output + (num_valid)

    return output

#@cache()
mycache = {}
#@functools.lru_cache()
def recursive_check(chunk_list, offset_list, symbol_list, idx, prev_offset):
    cache_in = tuple((chunk_list, offset_list, symbol_list, idx, prev_offset))
    if (cache_in in mycache):
        #print(f'Already in cache!')
        return mycache[cache_in]
    l_offset, r_offset = offset_list[idx]

    cnt = 0
    num_valid = 0
    for offset in range(l_offset+prev_offset, r_offset+1):
        #symbol_chunk = ''.join(symbol_list[offset:(offset+len(chunk))])

        chunk = chunk_list[idx]
        if (offset == 0): # chunk at the start
            symbol_chunk = ''.join(symbol_list[offset:(offset+len(chunk)+1)])
            remaining_symbols = symbol_list[(offset+len(chunk)+1):]
            chunk = chunk + '.'
            str_offset = ''
        elif (offset == offset_list[-1][1]): # chunk at the end
            symbol_chunk = ''.join(symbol_list[(offset-1):(offset+len(chunk))])
            remaining_symbols = symbol_list[(offset+len(chunk)):]
            chunk = '.' + chunk
            str_offset = ' '*(offset-1)
        else:
            symbol_chunk = ''.join(symbol_list[(offset-1):(offset+len(chunk)+1)])
            remaining_symbols = symbol_list[(offset+len(chunk)+1):]
            chunk = '.' + chunk + '.'
            str_offset = ' '*(offset-1)

        if (DEBUG):
            print(f'Checking idx = {idx} out of {len(chunk_list)-1}: {chunk} vs {symbol_chunk}')
            print(f'  {str_offset + chunk}')
            print(f'  {"".join(symbol_list)}')

        valid_chunk = True
        assert(len(symbol_chunk) == len(chunk))

        # Early stoppage if at last chunk and '#' is at the beginning. If we move forward,
        #   we won't be seeing it anymore and might mistakenly evaluate future arrangements as valid
        # Debugged via Row 22
        #if (idx == (len(chunk_list)-1)) and (symbol_chunk[0] == '#'):
        if (symbol_chunk[0] == '#') and (cnt):
            if (DEBUG):
                print(f'EARLY STOPPAGE')
            mycache[cache_in] = num_valid
            return num_valid

        for idx_s, s in enumerate(symbol_chunk):
            if (s != '?') and (s != chunk[idx_s]):
                valid_chunk = False
                break

        #if (symbol_chunk.replace('?', '#') == chunk):
        if (valid_chunk):
            if (idx < (len(chunk_list)-1)):
                if (DEBUG):
                    print(f'  match! next idx = {idx+1}')
                num_valid += recursive_check(chunk_list, offset_list, symbol_list, idx+1, prev_offset+cnt)
            else:

                # Before considering, check if remaining symbols at the end do not contain '#'
                if (DEBUG):
                    print(f'  Remaining symbols: {remaining_symbols}')
                if ('#' not in remaining_symbols):
                    if (DEBUG):
                        print('   valid arrangement found!')
                    num_valid += 1
                #return num_valid+1

        cnt += 1

    mycache[cache_in] = num_valid
    return num_valid

def process_inputs3(in_file):
    output = 0

    symbol_array = []
    number_array = []
    with open(in_file) as file:
        line = file.readline()
    
        num_groupable = 0
        less_chunks = 0
        more_chunks = 0
        max_excess_chunks = 0 
        max_lacking_chunks = 0

        has_exact_springs = 0

        idx_max_excess = 0
        idx_exact_springs = 0
        while line:
            line = line.strip()

            init_symbol_list, init_number_list = line.split(" ")

            symbol_list = [x for x in init_symbol_list]
            number_list = [int(x) for x in init_number_list.split(",")]

            # 5 folds
            symbol_array.append(symbol_list + ['?'] + symbol_list + ['?'] + symbol_list + ['?'] + symbol_list + ['?'] + symbol_list)
            number_array.append(number_list + number_list + number_list + number_list + number_list)
            # 2 folds
            #symbol_array.append(symbol_list + ['#'] + symbol_list + ['.'])
            #number_array.append(number_list + number_list)
            # 5 folds method 2
            #symbol_array.append(symbol_list + ['.'] + symbol_list + ['.'] + symbol_list + ['.'] + symbol_list + ['.'] + symbol_list + ['.'])
            #number_array.append(number_list + number_list + number_list + number_list + number_list)

            # 1 fold
            #symbol_array.append(symbol_list)
            #number_array.append(number_list)

            symbol_string = ''.join(symbol_array[-1])
            groups = [x for x in symbol_string.split('.') if (x != '')]

            len_groups = len(groups)
            len_last_number_list = len(number_array[-1])
            idx_array = len(number_array)-1
            if (len_groups == len_last_number_list):
                num_groupable += 1
            elif (len_groups < len_last_number_list):
                less_chunks += 1
                max_lacking_chunks = max(max_lacking_chunks, len_last_number_list - len_groups)

                largest_spring = max(number_array[-1])
                s = ''
                for i in range(0, largest_spring):
                    s = s + '#'

                if (s in groups):
                    has_exact_springs += 1
                    print(f'Row {idx_array} has exact springs')
            else:
                more_chunks += 1 # one of the chunks is just .
                if (max_excess_chunks < (len_groups-len_last_number_list)):
                    max_excess_chunks = max(max_excess_chunks, len_groups - len_last_number_list)
                    idx_max_excess = idx_array

            line = file.readline()

    print(f'num_groupable {num_groupable}')
    print(f'less_chunks {less_chunks} with max_lacking_chunks = {max_lacking_chunks} from row {idx_max_excess} and exact springs = {has_exact_springs}')
    print(f'more_chunks {more_chunks}')
    print(f'max excess_chunks {max_excess_chunks}')

    for idx, s in enumerate(symbol_array):
        print(s, end="")
        print(number_array[idx])

    for idx, symbol_list in enumerate(symbol_array):
        number_list = number_array[idx]

        symbol_length = len(symbol_list)
        total = sum(number_list)
        print(symbol_length)

        knowns = symbol_list.count('#')
        unknowns = symbol_list.count('?')

        unknown_broken = total - knowns

        if (unknown_broken == 0):
            output = output + 1
            continue

        # Generate all possible arrangements, and evaluate if valid
        # Method 2: sliding window?
        chunk_list = []
        offset_list = []
        for idx_n, n in enumerate(number_list):
            chunk_list.append(n*'#')

            left_nums = number_list[0:idx_n].copy()
            right_nums = number_list[idx_n:]
            right_nums.pop(0)

            left_sum = sum(left_nums)
            right_sum = sum(right_nums)

            l_offset = 0
            r_offset = 0
            if (left_sum):
                l_offset = left_sum + len(left_nums)

            r_offset = len(symbol_list) - (right_sum + len(right_nums)) - n

            offset_list.append((l_offset, r_offset))

        if (DEBUG):
            print(f'symbol_list = {symbol_list}')
            print(f'number_list = {number_list}')
            print(f'offset_list = {offset_list}')

        # Method 2
        print(f'Evaluating permutations...')
        num_valid = 0
        #num_valid = recursive_check(tuple(chunk_list), tuple(offset_list), tuple(symbol_list), 0, 0, num_valid, {})
        num_valid = recursive_check(tuple(chunk_list), tuple(offset_list), tuple(symbol_list), 0, 0)

        print(f'Row {idx}: {num_valid} arrangements')
        output = output + (num_valid)

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
#part2 = process_inputs2(input_file)

part2_example = process_inputs3(example_file)
part2 = process_inputs3(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
