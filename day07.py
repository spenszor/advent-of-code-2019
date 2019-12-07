from itertools import permutations

INSTRUCTION_POINTER_MAPPING = [-1, +4, +4, +2, +2, 0, 0, +4, +4]

class Computer:
    def __init__(self, memory, phase):
        self.memory = memory.copy()
        self.phase = phase
        self.current_pos = 0
        self.halted = False
        self.last_output = 0
        self.third_calls = 0

    def calculate(self, input_signal):
        while True:
            raw_instr = self.memory[self.current_pos]
            proc = str(raw_instr).zfill(5)

            instr = int(proc[-2:])
            modes = list(map(lambda x: int(x), proc[:-2]))

            if instr == 1:
                v1 = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                v2 = read_by_mode(modes[-2], self.memory, self.current_pos + 2)
                res = v1 + v2
                write_by_mode(modes[-3], self.memory, self.current_pos + 3, res)
            elif instr == 2:
                v1 = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                v2 = read_by_mode(modes[-2], self.memory, self.current_pos + 2)
                res = v1 * v2
                write_by_mode(modes[0], self.memory, self.current_pos + 3, res)
            elif instr == 3:
                read_v = input_signal
                if self.third_calls == 0:
                    read_v = self.phase
                self.third_calls += 1
                # print(f'I am {self.phase}, input: {read_v}')
                write_by_mode(modes[-1], self.memory, self.current_pos + 1, int(read_v))
            elif instr == 4:
                v = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                self.last_output = v
                # print(f'I am {self.phase}, output: {v}')
                self.current_pos += INSTRUCTION_POINTER_MAPPING[instr]
                return v
            elif instr == 5:
                v1 = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                new_ptr = read_by_mode(modes[-2], self.memory, self.current_pos + 2)
                if v1 != 0:
                    self.current_pos = new_ptr
                else:
                    self.current_pos += 3
            elif instr == 6:
                v1 = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                new_ptr = read_by_mode(modes[-2], self.memory, self.current_pos + 2)
                if v1 == 0:
                    self.current_pos = new_ptr
                else:
                    self.current_pos += 3
            elif instr == 7:
                v1 = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                v2 = read_by_mode(modes[-2], self.memory, self.current_pos + 2)
                if v1 < v2:
                    write_by_mode(modes[0], self.memory, self.current_pos + 3, 1)
                else:
                    write_by_mode(modes[0], self.memory, self.current_pos + 3, 0)
            elif instr == 8:
                v1 = read_by_mode(modes[-1], self.memory, self.current_pos + 1)
                v2 = read_by_mode(modes[-2], self.memory, self.current_pos + 2)
                if v1 == v2:
                    write_by_mode(modes[0], self.memory, self.current_pos + 3, 1)
                else:
                    write_by_mode(modes[0], self.memory, self.current_pos + 3, 0)
            elif instr == 99:
                self.halted = True
                break
            self.current_pos += INSTRUCTION_POINTER_MAPPING[instr]

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

with open('./inputs/day07') as inpt:
    parsed = list(map(lambda x: int(x), inpt.readline().split(',')))

    first_solution = 0
    for phase in permutations('01234'):
        input_signal = 0
        computers = [Computer(parsed, int(p)) for p in phase]
        for c in computers:
            input_signal = c.calculate(input_signal)
        result = computers[-1].last_output
        first_solution = max(result, first_solution)
    print(first_solution)
    
    second_solution = 0
    for phase in permutations('56789'):
        input_signal = 0
        computers = [Computer(parsed, int(p)) for p in phase]
        while not computers[-1].halted:
            for c in computers:
                input_signal = c.calculate(input_signal)
        result = computers[-1].last_output
        second_solution = max(result, second_solution)
    print(second_solution)

