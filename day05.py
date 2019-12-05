instr_mapping = [-1, +4, +4, +2, +2]

def solve_first(inpt):
    current_pos = 0
    while inpt[current_pos] != 99:
        raw_instr = inpt[current_pos]
        print(f"Raw {raw_instr}")
        proc = str(raw_instr)
        temp = 5 - len(proc)
        for _ in range(temp):
            proc = '0' + proc
        proc = list(map(lambda x: int(x), proc))
        print(f"Processed: {proc}")
        instr = proc[-1]

        modes = proc[:-2]
        print(f"modes: {modes}")
        if instr == 1:
            v1 = read_by_mode(modes[-1], inpt, current_pos + 1)
            v2 = read_by_mode(modes[-2], inpt, current_pos + 2)
            res = v1 + v2
            write_by_mode(modes[-3], inpt, current_pos + 3, res)
        elif instr == 2:
            v1 = read_by_mode(modes[-1], inpt, current_pos + 1)
            v2 = read_by_mode(modes[-2], inpt, current_pos + 2)
            res = v1 * v2
            write_by_mode(modes[0], inpt, current_pos + 3, res)
        elif instr == 3:
            read_v = input("Instruction 3, gib number: ")
            write_by_mode(modes[-1], inpt, current_pos + 1, int(read_v))
        elif instr == 4:
            v = read_by_mode(modes[-1], inpt, current_pos + 1)
            print(f"INSTRUCTION 4: {v}")
        current_pos += instr_mapping[instr]

def read_by_mode(mode, inpt, arg):
    if mode == 1:
        return inpt[arg]
    elif mode == 0:
        return inpt[inpt[arg]]

def write_by_mode(mode, inpt, arg, value_to_write):
    print("WRITE BY MODE START")
    print(mode)
    print(inpt)
    print(arg)
    print(value_to_write)
    if mode == 1:
        inpt[arg] = value_to_write
    elif mode == 0:
        inpt[inpt[arg]] = value_to_write
    print(inpt)
    print("WRITE BY MODE END")
# def solve_second(original_inpt):
#     for noun in range(100):
#         for verb in range(100):
#             inpt = list(original_inpt)
#             inpt[1] = noun
#             inpt[2] = verb
#             solution = solve_first(inpt, noun, verb)
#             if solution == 19690720:
#                 return 100 * noun + verb

with open('./inputs/day05') as inpt:
    parsed = map(lambda x: int(x), inpt.readline().split(','))
    solve_first(list(parsed))
    # print(solve_second(list(parsed)))