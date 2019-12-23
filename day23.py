from collections import deque
INSTRUCTION_POINTER_MAPPING = [-1, +4, +4, +2, +2, 0, 0, +4, +4, +2]

class Computer:
    def __init__(self, memory, parameters = []):
        self.memory = memory.copy()
        self.current_pos = 0
        self.halted = False
        self.last_output = 0
        self.relative_base = 0
        self.parameters = deque(parameters)

    def calculate(self, immediate_param = None):
        while True:
            raw_instr = self.memory[self.current_pos]
            proc = str(raw_instr).zfill(5)

            instr = int(proc[-2:])
            modes = list(map(lambda x: int(x), proc[:-2]))
            # print(f'Performing {instr}, modes: {modes}')
            if instr == 1:
                v1 = self.read_by_mode(modes[-1], self.current_pos + 1)
                v2 = self.read_by_mode(modes[-2], self.current_pos + 2)
                res = v1 + v2
                self.write_by_mode(modes[-3], self.current_pos + 3, res)
            elif instr == 2:
                v1 = self.read_by_mode(modes[-1], self.current_pos + 1)
                v2 = self.read_by_mode(modes[-2], self.current_pos + 2)
                res = v1 * v2
                self.write_by_mode(modes[0], self.current_pos + 3, res)
            elif instr == 3:
                if immediate_param:
                    self.write_by_mode(modes[-1], self.current_pos + 1, immediate_param)
                elif self.parameters:
                    self.write_by_mode(modes[-1], self.current_pos + 1, self.parameters.popleft())
                else:
                    return None
                    # read_v = input('Give param: ')
                    # read_v = -1
                    # self.write_by_mode(modes[-1], self.current_pos + 1, int(read_v))
            elif instr == 4:
                v = self.read_by_mode(modes[-1], self.current_pos + 1)
                self.last_output = v
                self.current_pos += INSTRUCTION_POINTER_MAPPING[instr]
                # print(f'Instr 4 triggered: {v}')
                return v
            elif instr == 5:
                v1 = self.read_by_mode(modes[-1], self.current_pos + 1)
                new_ptr = self.read_by_mode(modes[-2], self.current_pos + 2)
                if v1 != 0:
                    self.current_pos = new_ptr
                else:
                    self.current_pos += 3
            elif instr == 6:
                v1 = self.read_by_mode(modes[-1], self.current_pos + 1)
                new_ptr = self.read_by_mode(modes[-2], self.current_pos + 2)
                if v1 == 0:
                    self.current_pos = new_ptr
                else:
                    self.current_pos += 3
            elif instr == 7:
                v1 = self.read_by_mode(modes[-1], self.current_pos + 1)
                v2 = self.read_by_mode(modes[-2], self.current_pos + 2)
                if v1 < v2:
                    self.write_by_mode(modes[0], self.current_pos + 3, 1)
                else:
                    self.write_by_mode(modes[0], self.current_pos + 3, 0)
            elif instr == 8:
                v1 = self.read_by_mode(modes[-1], self.current_pos + 1)
                v2 = self.read_by_mode(modes[-2], self.current_pos + 2)
                if v1 == v2:
                    self.write_by_mode(modes[0], self.current_pos + 3, 1)
                else:
                    self.write_by_mode(modes[0], self.current_pos + 3, 0)
            elif instr == 9:
                new_base = self.read_by_mode(modes[-1], self.current_pos +1)
                self.relative_base += new_base
            elif instr == 99:
                self.halted = True
                break
            self.current_pos += INSTRUCTION_POINTER_MAPPING[instr]

    def read_by_mode(self, mode, address):
        if mode == 2:
            check_and_extend_arr(self.memory, self.memory[address] + self.relative_base)
            return self.memory[self.memory[address] + self.relative_base]
        elif mode == 1:
            check_and_extend_arr(self.memory, address)
            return self.memory[address]
        elif mode == 0:
            check_and_extend_arr(self.memory, address)
            addr = self.memory[address]
            check_and_extend_arr(self.memory, addr)
            return self.memory[addr]

    def write_by_mode(self, mode, address, value_to_write):
        if mode == 2:
            check_and_extend_arr(self.memory, self.memory[address] + self.relative_base)
            self.memory[self.memory[address] + self.relative_base] = value_to_write
        elif mode == 1:
            check_and_extend_arr(self.memory, address)
            self.memory[address] = value_to_write
        elif mode == 0:
            check_and_extend_arr(self.memory, address)
            addr = self.memory[address]
            check_and_extend_arr(self.memory, addr)
            self.memory[addr] = value_to_write

def check_and_extend_arr(arr, idx):
    if idx >= len(arr):
        arr.extend(((idx + 1) - len(arr)) * [0])
    return arr

def solve_first(data):
    computers = []
    for address in range(50):
        computers.append(Computer(parsed, [address]))

    run = True
    while run:
        for c in computers:
            address = c.calculate()
            if address:
                x = c.calculate()
                y = c.calculate()
                if address == 255:
                    print(f'Solution one: {y}')
                    run = False
                    break
                # print(f'Sending to {address}, {x} {y}')
                computers[address].parameters.append(x)
                computers[address].parameters.append(y)
        for c in computers:
            if not c.parameters:
                c.parameters.append(-1)

def solve_second(data):
    computers = []
    for address in range(50):
        computers.append(Computer(parsed, [address]))

    nat_x = None
    nat_y = None
    previous_nat_y = None
    idle = False
    run = True
    while run:
        idle = True
        for c in computers:
            address = c.calculate()
            if address:
                idle = False
                x = c.calculate()
                y = c.calculate()
                # print(f'Sending to {address}, {x} {y}')
                if address == 255:
                    nat_x = x
                    nat_y = y
                else:
                    computers[address].parameters.append(x)
                    computers[address].parameters.append(y)
        if idle and nat_x and nat_y:
            if nat_y == previous_nat_y:
                print(f'Solution two: {nat_y}')
                run = False
                break
            computers[0].parameters.append(nat_x)
            computers[0].parameters.append(nat_y)
            previous_nat_y = nat_y
        for c in computers:
            if not c.parameters:
                c.parameters.append(-1)


with open('./inputs/day23') as data:
    parsed = list(map(lambda x: int(x), data.readline().split(',')))
    solve_first(parsed)
    solve_second(parsed)