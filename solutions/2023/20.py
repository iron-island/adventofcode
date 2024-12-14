import math

input_file = "input20.txt"
example_file = "example20.txt"
#example_file = "example20_2.txt" # answer: 32000000

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0
L = 0
H = 1
# Hardcoded for input, Part 2
RELEVANT_FF0 = ['fh', 'vl', 'tx', 'zh', 'mx', 'qd', 'mr', 'pd', 'sq']
RELEVANT_FF1 = ['vj', 'fl', 'dd', 'cg', 'fb', 'nf', 'ld', 'nz', 'dh']
RELEVANT_FF2 = ['gz', 'mz', 'ps', 'lq', 'qh', 'vk', 'gk', 'lb', 'gx']
RELEVANT_FF3 = ['jt', 'xr', 'mg', 'rd', 'cl', 'tc', 'ts', 'sg']

RELEVANT_FF0 = ['fh', 'vl', 'tx', 'zh', 'mx', 'qd', 'mr', 'pd']
RELEVANT_FF1 = ['vj', 'fl', 'dd', 'cg', 'fb', 'nf', 'ld', 'nz']
RELEVANT_FF2 = ['gz', 'mz', 'ps', 'lq', 'qh', 'vk', 'gk', 'lb']
RELEVANT_FF3 = ['jt', 'xr', 'mg', 'rd', 'cl', 'tc', 'ts']
HIGH_PERIOD = ['sq', 'dh', 'gx', 'sg']
ALL_RELEVANT_FF = RELEVANT_FF0 + RELEVANT_FF1 + RELEVANT_FF2 + RELEVANT_FF3
FF_LIST_DICT = {'sq': RELEVANT_FF0, 'dh': RELEVANT_FF1, 'gx': RELEVANT_FF2, 'sg': RELEVANT_FF3}
MIN_CYCLES = 3

ALL_RELEVANT_CONJ = ['ll', 'rc', 'gv', 'qf']

def check_state(ff_list, ff_dict):
    state = ''
    for ff in ff_list:
        state = state + str(ff_dict[ff]['state'])

    return state

def update_conj(conj_dict, mod, pulse, src):
    conj_dict[mod]["inputs"][src] = pulse

    states = set()
    for s in conj_dict[mod]["inputs"]:
        states.add(conj_dict[mod]["inputs"][s])

    if (len(states) == 1) and (1 in states):
        outpulse = 0
    else:
        outpulse = 1
            
    return conj_dict[mod]["dest"], outpulse

def process_inputs(in_file):
    output = 0

    modules_list = []
    bc_list = []
    bc = "broadcaster -> "
    ff_dict = {}
    conj_dict = {}
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            modules_list.append(line)

            if (bc in line):
                bc_list = line[len(bc):].split(", ")
            elif ("%" in line):
                ff, dest = line[1:].split(" -> ")
                ff_dict[ff] = {}
                ff_dict[ff]["state"] = 0
                ff_dict[ff]["dest"] = dest.split(", ")
            elif ("&" in line):
                conj, dest = line[1:].split(" -> ")
                conj_dict[conj] = {}
                conj_dict[conj]["inputs"] = {} # input memories will be populated later
                conj_dict[conj]["dest"] = dest.split(", ")

            line = file.readline()

    print(modules_list)
    
    # Initialize states of conj inputs
    for ff in ff_dict:
        for d in ff_dict[ff]["dest"]:
            if (d in conj_dict):
                conj_dict[d]["inputs"][ff] = 0
    
    # Debugging
    print(f'broadcaster: {bc_list}')
    print(f'flip-flops: {ff_dict}')
    print(f'conjunction: {conj_dict}')

    # Simulate
    queue = []
    low_pulses = 0
    high_pulses = 0
    PUSHES = 1000
    for p in range(1, PUSHES+1):
        print(f'Push #{p}')
        low_pulses += 1 # pushing broadcaster counts
        for idx, b in enumerate(bc_list):
            queue.append((b, L, ""))

        while len(queue):
            q = queue.pop(0)
            mod, pulse, src = q
            print(q)

            if (pulse == L):
                low_pulses += 1
            elif (pulse == H):
                high_pulses += 1

            if (mod in ff_dict) and (pulse == L):
                state = ff_dict[mod]["state"]
                if (state == 0):
                    ff_dict[mod]["state"] = 1
                    for d in ff_dict[mod]["dest"]:
                        queue.append((d, H, mod))
                elif (state == 1):
                    ff_dict[mod]["state"] = 0
                    for d in ff_dict[mod]["dest"]:
                        queue.append((d, L, mod))
            elif (mod in conj_dict):
                dest_list, outpulse = update_conj(conj_dict, mod, pulse, src)
                for dest in dest_list:
                    queue.append((dest, outpulse, mod))

    print(f'Low pulses: {low_pulses}')
    print(f'High pulses: {high_pulses}')
    output = low_pulses*high_pulses

    return output

def process_inputs2(in_file):
    output = 0

    modules_list = []
    bc_list = []
    bc = "broadcaster -> "
    ff_dict = {}
    conj_dict = {}
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            modules_list.append(line)

            if (bc in line):
                bc_list = line[len(bc):].split(", ")
            elif ("%" in line):
                ff, dest = line[1:].split(" -> ")
                ff_dict[ff] = {}
                ff_dict[ff]["state"] = 0
                ff_dict[ff]["dest"] = dest.split(", ")
            elif ("&" in line):
                conj, dest = line[1:].split(" -> ")
                conj_dict[conj] = {}
                conj_dict[conj]["inputs"] = {} # input memories will be populated later
                conj_dict[conj]["dest"] = dest.split(", ")

            line = file.readline()

    # Initialize states of conj inputs
    for ff in ff_dict:
        for d in ff_dict[ff]["dest"]:
            if (d in conj_dict):
                conj_dict[d]["inputs"][ff] = 0

    for conj in conj_dict:
        for d in conj_dict[conj]["dest"]:
            if (d in conj_dict):
                conj_dict[d]["inputs"][conj] = 0

    # Debugging
    #print(f'broadcaster: {bc_list}')
    #print(f'flip-flops: {ff_dict}')
    #print(f'conjunction: {conj_dict}')

    # Initialize dictionaries of ff periods
    ff_periods = {}
    ff_pushes = {}
    ff_prev_inv_state = {}
    ff_high_state = {}
    for ff in ALL_RELEVANT_FF:
        ff_periods[ff] = 0
        ff_pushes[ff] = []
        ff_prev_inv_state[ff] = 0
        ff_high_state[ff] = 0

    hp_high_state = {}
    for ff in HIGH_PERIOD:
        hp_high_state[ff] = {}
        hp_high_state[ff]['count1'] = []
        hp_high_state[ff]['count0'] = [1]
        hp_high_state[ff]['start1'] = []
        hp_high_state[ff]['start0'] = [0]
        hp_high_state[ff]['state'] = 0
        hp_high_state[ff]['ff_list_state'] = ['0']

    # Initialize dictionaries of conj periods
    conj_periods = {}
    conj_pushes = {}
    conj_prev_inv_state = {}
    for conj in ALL_RELEVANT_CONJ:
        conj_periods[conj] = 0
        conj_pushes[conj] = []
        conj_prev_inv_state[conj] = 0

    # Simulate
    queue = []
    low_pulses = 0
    high_pulses = 0
    PUSHES = 16
    #for p in range(1, PUSHES+1):
    #    print(f'Push #{p}')
    p = 0
    no_cycle_detected = True
    while no_cycle_detected:
        p += 1
        if (p % 10000 == 0):
            print(f'Push #{p}')
        low_pulses += 1 # pushing broadcaster counts
        for idx, b in enumerate(bc_list):
            queue.append((b, L, ""))

        while len(queue):
            q = queue.pop(0)
            mod, pulse, src = q

            if (mod == "rx"):
                if (pulse == 0):
                    output = p
                    return output

            if (pulse == L):
                low_pulses += 1
            elif (pulse == H):
                high_pulses += 1

            if (mod in ff_dict) and (pulse == L):
                state = ff_dict[mod]["state"]
                if (state == 0):
                    ff_dict[mod]["state"] = 1
                    for d in ff_dict[mod]["dest"]:
                        queue.append((d, H, mod))
                elif (state == 1):
                    ff_dict[mod]["state"] = 0
                    for d in ff_dict[mod]["dest"]:
                        queue.append((d, L, mod))
            elif (mod in conj_dict):
                dest_list, outpulse = update_conj(conj_dict, mod, pulse, src)
                for dest in dest_list:
                    queue.append((dest, outpulse, mod))

        #if state_repeated(ff_dict, conj_dict, p):
        #    print(f'States reset at push {p}')
        #    return

        for ff in HIGH_PERIOD:
            ff_state = ff_dict[ff]['state']

            if (hp_high_state[ff]['state'] % 2) == 0:
                # Record 0s
                if (ff_state == 0):
                    hp_high_state[ff]['count0'][-1] += 1
                else:
                    hp_high_state[ff]['count1'].append(1)
                    hp_high_state[ff]['start1'].append(p)
                    hp_high_state[ff]['state'] += 1
            else:
                # Record 1s
                if (ff_state == 1):
                    hp_high_state[ff]['count1'][-1] += 1
                else:
                    hp_high_state[ff]['count0'].append(1)
                    hp_high_state[ff]['start0'].append(p)
                    hp_high_state[ff]['state'] += 1
                    ff_list_state = check_state(FF_LIST_DICT[ff], ff_dict)
                    hp_high_state[ff]['ff_list_state'].append(ff_list_state)

        for ff in HIGH_PERIOD:
            if (hp_high_state[ff]['state'] < 10):
                break
        else:
            print(hp_high_state)
            no_cycle_detected = False

        # Cycle detection on relevant ff
        for ff in ALL_RELEVANT_FF:
            if (ff_dict[ff]['state'] != ff_prev_inv_state[ff]):
                ff_pushes[ff].append(p)
                ff_prev_inv_state[ff] = ff_dict[ff]['state']

            if (ff_dict[ff]['state'] == 1):
                ff_high_state[ff] = p

        for ff in ff_pushes:
            # If last MIN_CYCLES are periodic, then stop
            if (len(ff_pushes[ff]) > MIN_CYCLES):
                if (len(ff_pushes[ff]) > (MIN_CYCLES+1)):
                    ff_pushes[ff] = ff_pushes[ff][1:]

                push_list = ff_pushes[ff]
                len_ff_int = len(push_list)

                int_period = push_list[len_ff_int-MIN_CYCLES] - push_list[len_ff_int-(MIN_CYCLES+1)]
                for i in range(len_ff_int-(MIN_CYCLES-1), len_ff_int):
                    curr_period = push_list[i] - push_list[i-1]
                    if (curr_period != int_period):
                        #ff_pushes[ff] = curr_period
                        break
                else: # if did not break, then cycle was detected
                    #print(f'Cycle detected on flop {ff} with period {int_period}!')
                    ff_periods[ff] = int_period

        for ff in ff_periods:
            if (ff_periods[ff] == 0):
                break
        #else:
        #    no_cycle_detected = False

        # DEBUGGING
        if (p % 3930 == 0):
            print(f'ff_list_state 0 = {check_state(FF_LIST_DICT[HIGH_PERIOD[0]], ff_dict)}')
        elif (p % 3766 == 0):
            print(f'ff_list_state 1 = {check_state(FF_LIST_DICT[HIGH_PERIOD[1]], ff_dict)}')
        elif (p % 4006 == 0):
            print(f'ff_list_state 2 = {check_state(FF_LIST_DICT[HIGH_PERIOD[2]], ff_dict)}')
        elif (p % 3922 == 0):
            print(f'ff_list_state 3 = {check_state(FF_LIST_DICT[HIGH_PERIOD[3]], ff_dict)}')

        # Initial attempt to observe input features
        '''
        bit = 'qf'
        #if ((p & (p-1)) == 0):
        #    print(f'Push #{p}')
        for conj in conj_dict:
            state = ''
            #if (conj != bit):
            #    continue

            #print(f'{conj}: ', end="")
            for i in conj_dict[conj]["inputs"]:
                #print(f'{conj_dict[conj]["inputs"][i]}', end="")
                state = state + str(conj_dict[conj]["inputs"][i])
            #print("")

            #if (conj == 'll'):
            #    ll_state = state
            #elif (conj == 'rc'):
            #    rc_state = state
            #elif (conj == 'gv'):
            #    gv_state = state
            #elif (conj == 'qf'):
            #    qf_state = state

        #if (ll_state == "1"*len(ll_state)):
        #    print("ll is all 1s at push #{p}!")
        #if (rc_state == "1"*len(rc_state)):
        #    print("ll is all 1s at push #{p}!")
        #if (gv_state == "1"*len(gv_state)):
        #    print("ll is all 1s at push #{p}!")
        #if (qf_state == "1"*len(qf_state)):
        #    print("ll is all 1s at push #{p}!")
        '''

    print(f'Low pulses: {low_pulses}')
    print(f'High pulses: {high_pulses}')
    print(ff_periods)
    for ff_list in [RELEVANT_FF0, RELEVANT_FF1, RELEVANT_FF2, RELEVANT_FF3]:
        max_period = 0
        min_period = 1000000
        for ff in ff_list:
            max_period = max(max_period, ff_periods[ff])
            min_period = min(min_period, ff_periods[ff])
        print(f'{min_period}, {max_period}')

    start0 = 'start0'
    output = 1
    for ff in HIGH_PERIOD:
        print(f'ff {ff}: {hp_high_state[ff][start0][1]}')
        output = math.lcm(output, hp_high_state[ff]['start0'][1])
    #output = output - 1

    return output

#part1_example = process_inputs(example_file)
#part1 = process_inputs(input_file)

#part2_example = process_inputs2(example_file)
part2 = process_inputs2(input_file)

print(f'Part 1 example: {part1_example}')
print(f'Part 1: {part1}')
print("")
print(f'Part 2 example: {part2_example}')
print(f'Part 2: {part2}')
