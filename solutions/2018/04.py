from collections import defaultdict

input_file = "input4.txt"
example_file = "example04.txt"

part1_example = 0
part2_example = 0
part1 = 0
part2 = 0

def process_inputs(in_file):
    output = 0

    record_dict = defaultdict(str)
    shift_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            timestamp, activity = line.split("] ")

            # Parse times
            ymd, hm = timestamp.split(" ")
            ymd = ymd[1:]
            year, month, day = ymd.split("-")
            hour, minute = hm.split(":")

            # Record
            parsed_time = (int(year), int(month), int(day), int(hour), int(minute))
            assert(parsed_time not in record_dict)
            record_dict[parsed_time] = activity

            # Check IDs of guard and record their shifts
            if ("Guard #" in activity):
                guard_id = activity[7:].split(" ")[0]
                #guard_dict[guard_id].append(parsed_time)
                year, month, day, hour, minute = parsed_time
                shift_list.append((year, month, day, hour, minute, guard_id))

            line = file.readline()

    # Sort shift times of guards
    shift_list.sort()
    print(shift_list)

    # Check activity
    sleep_list = []
    wake_list = []
    for parsed_time in record_dict:
        activity = record_dict[parsed_time]
        year, month, day, hour, minute = parsed_time

        if ("falls asleep" in activity) or ("wakes up" in activity):
            # Find ID of guard with latest shift
            guard_id = None
            for idx, shift in enumerate(shift_list):
                prev_id = guard_id
                s_y, s_m, s_d, s_h, s_min, guard_id = shift

                # Since shift_list is sorted, once shift exceeds timestamp,
                #   then last guard ID was the latest shift
                if ((s_y, s_m, s_d, s_h, s_min) > parsed_time):
                    guard_id = prev_id
                    break
            print(f'Compared {parsed_time}, ID = {guard_id}')

            parsed_time_id = (year, month, day, hour, minute, guard_id)
            assert(hour == 0)
            if ("falls asleep" in activity):
                sleep_list.append(parsed_time_id)
            elif ("wakes up" in activity):
                wake_list.append(parsed_time_id)

    # Sort sleep and wake times
    sleep_list.sort()
    wake_list.sort()
    assert(len(sleep_list) == len(wake_list))

    # Compute times asleep
    asleep_min_dict = defaultdict(int)
    guard_asleep_dict = defaultdict(int)
    for idx, sleep_time_id in enumerate(sleep_list):
        y, m, d, h, minute, guard_id = sleep_time_id
        w_y, w_m, w_d, w_h, w_minute, w_guard_id = wake_list[idx]
        assert(guard_id == w_guard_id)

        guard_asleep_dict[guard_id] += (w_minute - minute)
        for sleep_minute in range(minute, w_minute):
            asleep_min_dict[(guard_id, sleep_minute)] += 1

    # Find guard ID with the most sleep
    max_sleep = 0
    for guard_id in guard_asleep_dict:
        guard_asleep = guard_asleep_dict[guard_id]
        if (guard_asleep > max_sleep):
            final_id = guard_id
            max_sleep = guard_asleep
    print(guard_asleep_dict)

    # Evaluate
    max_num = 0
    for id_min in asleep_min_dict:
        guard_id, minute = id_min

        if (guard_id != final_id):
            continue

        num = asleep_min_dict[id_min]
        if (num > max_num):
            max_num = num
            final_minute = minute
    output = int(final_id)*int(final_minute)
    print(f'Guard: {final_id}, final_minute: {final_minute}')

    return output

def process_inputs2(in_file):
    output = 0

    record_dict = defaultdict(str)
    shift_list = []
    with open(in_file) as file:
        line = file.readline()
    
        while line:
            line = line.strip()

            timestamp, activity = line.split("] ")

            # Parse times
            ymd, hm = timestamp.split(" ")
            ymd = ymd[1:]
            year, month, day = ymd.split("-")
            hour, minute = hm.split(":")

            # Record
            parsed_time = (int(year), int(month), int(day), int(hour), int(minute))
            assert(parsed_time not in record_dict)
            record_dict[parsed_time] = activity

            # Check IDs of guard and record their shifts
            if ("Guard #" in activity):
                guard_id = activity[7:].split(" ")[0]
                #guard_dict[guard_id].append(parsed_time)
                year, month, day, hour, minute = parsed_time
                shift_list.append((year, month, day, hour, minute, guard_id))

            line = file.readline()

    # Sort shift times of guards
    shift_list.sort()
    print(shift_list)

    # Check activity
    sleep_list = []
    wake_list = []
    for parsed_time in record_dict:
        activity = record_dict[parsed_time]
        year, month, day, hour, minute = parsed_time

        if ("falls asleep" in activity) or ("wakes up" in activity):
            # Find ID of guard with latest shift
            guard_id = None
            for idx, shift in enumerate(shift_list):
                prev_id = guard_id
                s_y, s_m, s_d, s_h, s_min, guard_id = shift

                # Since shift_list is sorted, once shift exceeds timestamp,
                #   then last guard ID was the latest shift
                if ((s_y, s_m, s_d, s_h, s_min) > parsed_time):
                    guard_id = prev_id
                    break
            print(f'Compared {parsed_time}, ID = {guard_id}')

            parsed_time_id = (year, month, day, hour, minute, guard_id)
            assert(hour == 0)
            if ("falls asleep" in activity):
                sleep_list.append(parsed_time_id)
            elif ("wakes up" in activity):
                wake_list.append(parsed_time_id)

    # Sort sleep and wake times
    sleep_list.sort()
    wake_list.sort()
    assert(len(sleep_list) == len(wake_list))

    # Compute times asleep
    asleep_min_dict = defaultdict(int)
    guard_asleep_dict = defaultdict(int)
    for idx, sleep_time_id in enumerate(sleep_list):
        y, m, d, h, minute, guard_id = sleep_time_id
        w_y, w_m, w_d, w_h, w_minute, w_guard_id = wake_list[idx]
        assert(guard_id == w_guard_id)

        guard_asleep_dict[guard_id] += (w_minute - minute)
        for sleep_minute in range(minute, w_minute):
            asleep_min_dict[(guard_id, sleep_minute)] += 1

    # Evaluate
    max_num = 0
    for id_min in asleep_min_dict:
        num = asleep_min_dict[id_min]

        if (num > max_num):
            max_num = num
            final_id, final_minute = id_min
    output = int(final_id)*int(final_minute)

    print(f'Guard: {final_id}, final_minute: {final_minute}')

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
