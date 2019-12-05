INSTRUCTION_POINTER_MAPPING = [-1, +4, +4, +2, +2, 0, 0, +4, +4]

def solve_first(memory):
    current_pos = 0
    while memory[current_pos] != 99:
        raw_instr = memory[current_pos]
        proc = str(raw_instr)
        temp = 5 - len(proc)
        for _ in range(temp):
            proc = '0' + proc
        proc = list(map(lambda x: int(x), proc))

        instr = proc[-1]
        modes = proc[:-2]

        if instr == 1:
            v1 = read_by_mode(modes[-1], memory, current_pos + 1)
            v2 = read_by_mode(modes[-2], memory, current_pos + 2)
            res = v1 + v2
            write_by_mode(modes[-3], memory, current_pos + 3, res)
        elif instr == 2:
            v1 = read_by_mode(modes[-1], memory, current_pos + 1)
            v2 = read_by_mode(modes[-2], memory, current_pos + 2)
            res = v1 * v2
            write_by_mode(modes[0], memory, current_pos + 3, res)
        elif instr == 3:
            read_v = input("Instruction 3, give argument: ")
            write_by_mode(modes[-1], memory, current_pos + 1, int(read_v))
        elif instr == 4:
            v = read_by_mode(modes[-1], memory, current_pos + 1)
            print(f"INSTRUCTION 4: {v}")
        elif instr == 5:
            v1 = read_by_mode(modes[-1], memory, current_pos + 1)
            new_ptr = read_by_mode(modes[-2], memory, current_pos + 2)
            if v1 != 0:
                current_pos = new_ptr
            else:
                current_pos += 3
        elif instr == 6:
            v1 = read_by_mode(modes[-1], memory, current_pos + 1)
            new_ptr = read_by_mode(modes[-2], memory, current_pos + 2)
            if v1 == 0:
                current_pos = new_ptr
            else:
                current_pos += 3
        elif instr == 7:
            v1 = read_by_mode(modes[-1], memory, current_pos + 1)
            v2 = read_by_mode(modes[-2], memory, current_pos + 2)
            if v1 < v2:
                write_by_mode(modes[0], memory, current_pos + 3, 1)
            else:
                write_by_mode(modes[0], memory, current_pos + 3, 0)
        elif instr == 8:
            v1 = read_by_mode(modes[-1], memory, current_pos + 1)
            v2 = read_by_mode(modes[-2], memory, current_pos + 2)
            if v1 == v2:
                write_by_mode(modes[0], memory, current_pos + 3, 1)
            else:
                write_by_mode(modes[0], memory, current_pos + 3, 0)   
        current_pos += INSTRUCTION_POINTER_MAPPING[instr]

def read_by_mode(mode, memory, address):
    if mode == 1:
        return memory[address]
    elif mode == 0:
        return memory[memory[address]]

def write_by_mode(mode, memory, address, value_to_write):
    if mode == 1:
        memory[address] = value_to_write
    elif mode == 0:
        memory[memory[address]] = value_to_write

with open('./inputs/day05') as inpt:
    parsed = map(lambda x: int(x), inpt.readline().split(','))
    solve_first(list(parsed))