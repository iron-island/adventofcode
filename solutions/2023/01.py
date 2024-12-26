inputfile = "input1.txt"
#inputfile = "example01.txt"

total = 0
total_part2 = 0
with open(inputfile) as file:
    line = file.readline()

    while (line):
        line = line.strip()

        unmodified_line = line
        if ("oneight" in line):
            line = line.replace('oneight', '18')
        if ("eightwo" in line):
            line = line.replace('eightwo', '82')
        if ("eighthree" in line):
            line = line.replace('eighthree', '83')
        if ("twone" in line):
            line = line.replace('twone', '21')
        if ("sevenine" in line):
            line = line.replace('sevenine', '79')
        if ("nineight" in line):
            line = line.replace('nineight', '98')
        if ("one" in line):
            line = line.replace('one', '1')
        if ("two" in line):
            line = line.replace('two', '2')
        if ("three" in line):
            line = line.replace('three', '3')
        if ("four" in line):
            line = line.replace('four', '4')
        if ("five" in line):
            line = line.replace('five', '5')
        if ("six" in line):
            line = line.replace('six', '6')
        if ("seven" in line):
            line = line.replace('seven', '7')
        if ("eight" in line):
            line = line.replace('eight', '8')
        if ("nine" in line):
            line = line.replace('nine', '9')
        print(f'{unmodified_line} = {line}')

        first_digit = None
        last_digit = None
        digit_count = 0
        for digit in line:
            if (digit.isdigit()):
                digit_count = digit_count + 1
                if (first_digit == None):
                    first_digit = int(digit)
                else:
                    last_digit = int(digit)

        if (digit_count == 1):
            cal_val = first_digit*11
        else:
            cal_val = first_digit*10 + last_digit
        total = total + cal_val

        #if ("one" in line):
        #    digit1 = 1
        #    idx1 = line.find("one")
        #    line1 = line.replace('one', '')
        #elif ("two" in line):
        #    digit1 = 2
        #    idx1 = line.find("two")
        #    line1 = line.replace('two', '')
        #elif ("three" in line):
        #    digit1 = 3
        #    idx1 = line.find("three")
        #    line1 = line.replace('three', '')
        #elif ("four" in line):
        #    digit1 = 4
        #    idx1 = line.find("fource")
        #    line1 = line.replace('four', '')
        #elif ("five" in line):
        #    digit1 = 5
        #    idx1 = line.find("five")
        #    line1 = line.replace('five', '')
        #elif ("six" in line):
        #    digit1 = 6
        #    idx1 = line.find("six")
        #    line1 = line.replace('six', '')
        #elif ("seven" in line):
        #    digit1 = 7
        #    idx1 = line.find("seven")
        #    line1 = line.replace('seven', '')
        #elif ("eight" in line):
        #    digit1 = 8
        #    idx1 = line.find("eight")
        #    line1 = line.replace('eight', '')
        #elif ("nine" in line):
        #    digit1 = 9
        #    idx1 = line.find("nine")
        #    line1 = line.replace('nine', '')

        #digit2 = None
        #if ("one" in line1):
        #    digit2 = 1
        #    idx2 = line.find("one")
        #    line2 = line1.replace('one', '')
        #elif ("two" in line1):
        #    digit2 = 2
        #    idx2 = line.find("two")
        #    line2 = line1.replace('two', '')
        #elif ("three" in line1):
        #    digit2 = 3
        #    idx2 = line.find("three")
        #    line2 = line1.replace('three', '')
        #elif ("four" in line1):
        #    digit2 = 4
        #    idx2 = line.find("fource")
        #    line2 = line1.replace('four', '')
        #elif ("five" in line1):
        #    digit2 = 5
        #    idx2 = line.find("five")
        #    line2 = line1.replace('five', '')
        #elif ("six" in line1):
        #    digit2 = 6
        #    idx2 = line.find("six")
        #    line2 = line1.replace('six', '')
        #elif ("seven" in line1):
        #    digit2 = 7
        #    idx2 = line.find("seven")
        #    line2 = line1.replace('seven', '')
        #elif ("eight" in line1):
        #    digit2 = 8
        #    idx2 = line.find("eight")
        #    line2 = line1.replace('eight', '')
        #elif ("nine" in line1):
        #    digit2 = 9
        #    idx2 = line.find("nine")
        #    line2 = line1.replace('nine', '')

        #if (digit2 == None):
        #    idx2 = 100000

        #if (min(first_idx, last_idx, idx1, idx2) == first_idx):
        #    left = first_digit
        #elif (min(first_idx, last_idx, idx1, idx2) == last_idx):
        #    left = last_digit
        #elif (min(first_idx, last_idx, idx1, idx2) == idx1):
        #    left = digit1
        #elif (min(first_idx, last_idx, idx1, idx2) == idx2):
        #    left = digit2

        #if (max(first_idx, last_idx, idx1, idx2) == first_idx):
        #    right = first_digit
        #elif (max(first_idx, last_idx, idx1, idx2) == last_idx):
        #    right = last_digit
        #elif (max(first_idx, last_idx, idx1, idx2) == idx1):
        #    right = digit1
        #elif (max(first_idx, last_idx, idx1, idx2) == idx2):
        #    right = digit2

        #cal_val_p2 = left*10 + right

        #if (idx2 > idx1):
        #    cal_val_p2 = digit1*10 + digit2
        #else:
        #    cal_val_p2 = digit2*10 + digit1

        #total_part2 = total_part2 + cal_val_p2
            
        line = file.readline()

print(total)
