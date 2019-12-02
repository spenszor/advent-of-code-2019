def solve_first(input, noun, verb):
    input[1] = noun
    input[2] = verb
    current_pos = 0
    while input[current_pos] != 99:
        if input[current_pos] == 1:
            pos1 = input[current_pos + 1]
            pos2 = input[current_pos + 2]
            res = input[pos1] + input[pos2]
            output_pos = input[current_pos + 3]
            input[output_pos] = res
        elif input[current_pos] == 2:
            pos1 = input[current_pos + 1]
            pos2 = input[current_pos + 2]
            res = input[pos1] * input[pos2]
            output_pos = input[current_pos + 3]
            input[output_pos] = res
        current_pos += 4
    return input[0]

def solve_second(original_input):
    for noun in range(100):
        for verb in range(100):
            input = list(original_input)
            input[1] = noun
            input[2] = verb
            solution = solve_first(input, noun, verb)
            if solution == 19690720:
                return 100 * noun + verb

with open('./inputs/day02') as input:
    parsed = map(lambda x: int(x), input.readline().split(','))
    print(solve_first(list(parsed), 12, 2))
    print(solve_second(list(parsed)))