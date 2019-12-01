def calculate_fuel(mass):
    return (mass // 3) - 2

def calculate_rec_fuel(mass):
    if (fuel := calculate_fuel(mass)) > 0:
        return fuel + calculate_rec_fuel(fuel)
    else:
        return 0

def solve_first(input):
    return sum([calculate_fuel(int(mass)) for mass in input])

def solve_second(input):
    return sum([calculate_rec_fuel(int(mass)) for mass in input])

with open('./inputs/day01-p1') as input:
    print(solve_first(input))
    input.seek(0)
    print(solve_second(input))