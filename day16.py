from collections import deque

def last_digit(n):
    return abs(n) % 10

def solve_first(data):
    digits = [int(num) for num in data]

    for phase in range(100):
        for pos in range(len(digits)):
            pattern = deque([p for p in [0, 1, 0, -1] for _ in range(pos+1)])
            pattern.rotate(-1)

            res = 0
            for i in range(len(digits)):
                res += digits[i] * pattern[0]
                pattern.rotate(-1)
            digits[pos] = last_digit(res)

    return "".join(str(x) for x in digits[:8])

with open('./inputs/day16') as data:
    test_1 = '80871224585914546619083218645595'
    test_2 = '19617804207202209144916044189917'
    test_3 = '69317163492948606335995924319873'
    print(f'First solution: {solve_first(data.readline().strip())}')
