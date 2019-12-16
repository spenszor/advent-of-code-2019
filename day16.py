from collections import deque
from math import ceil

def last_digit(n):
    return abs(n) % 10

def solve_first(data):
    digits = [int(num) for num in data]

    for phase in range(100): 
        for pos in range(len(digits)): # also treat pos as offset
            pattern = deque([p for p in [1, 0, -1, 0] for _ in range(pos+1)])

            res = 0
            for i in range(pos, len(digits)): # skip offset (always 0) 
                res += digits[i] * pattern[0]
                pattern.rotate(-1)
            digits[pos] = last_digit(res)
    return ''.join(str(x) for x in digits[:8])

def solve_second(data):
    # offset value slices the input way beyond the half of initial value -> this means that all coeficients have value 1
    # this means that in the example for initial value 12345678, I should be looking only at rows that have coeficient 1 in 'second half'
    # (so new values for digits 5, 6 ,7 ,8)
    offset = int(data[:7])
    digits = [int(num) for num in (data * 10000)][offset:]

    # last digit always remains the same (regardless of phase)!
    # new second to last digit is (second to last digit + last digit) % 10
    # new third to last digit is (third to last digit + new second to last digit) % 10
    for _ in range(100):
        for i in range(-2, -len(digits)-1, -1):
            digits[i] = (digits[i] + digits[i+1]) % 10

    return "".join([str(x) for x in digits[:8]])

with open('./inputs/day16') as data:
    raw = data.readline().strip()
    test_1_1 = '80871224585914546619083218645595'
    test_1_2 = '19617804207202209144916044189917'
    test_1_3 = '69317163492948606335995924319873'
    print(f'First solution: {solve_first(raw)}')
    test_2_1 = '03036732577212944063491565474664' # 84462026
    test_2_2 = '02935109699940807407585447034323' # 78725270
    test_2_3 = '03081770884921959731165446850517' # 53553731
    print(f'Second solution: {solve_second(raw)}')
