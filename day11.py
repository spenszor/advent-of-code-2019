INSTRUCTION_POINTER_MAPPING = [-1, +4, +4, +2, +2, 0, 0, +4, +4, +2]

class Computer:
    def __init__(self, memory):
        self.memory = memory.copy()
        self.current_pos = 0
        self.halted = False
        self.last_output = 0
        self.relative_base = 0

    def calculate(self, params = []):
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
                if params:
                    self.write_by_mode(modes[-1], self.current_pos + 1, params.pop(0))
                else:
                    read_v = input('Give param: ')
                    self.write_by_mode(modes[-1], self.current_pos + 1, int(read_v))
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
                # print(f'Relative base changed to {self.relative_base}')
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

def move(field, direction):
    x, y = field
    if direction == 'up':
        return (x, y + 1)
    elif direction == 'right':
        return (x + 1, y)
    elif direction == 'down':
        return (x, y -1)
    elif direction == 'left':
        return (x - 1, y)

with open('./inputs/day11') as inpt:
    parsed = list(map(lambda x: int(x), inpt.readline().split(',')))
    c = Computer(parsed)
    directions = ['up', 'right', 'down', 'left']
    fields = dict()
    current_color = 1 # change to 0 for part one
    current_field = (0, 0)
    current_direction = 'up'
    i = 0
    first = True
    while not c.halted and i < 10:
        if not first:
            current_color = 0
        else:
            first = False
        if (current_field) in fields:
            current_color = fields[(current_field)]
        color = c.calculate([current_color])
        direction = c.calculate([])
        fields[current_field] = color
        if direction == 0:
            # turn left
            idx = (directions.index(current_direction) - 1) % 4
            # print(f'At {current_field} , turning left - from {current_direction} to {directions[idx]}')
            current_direction = directions[idx]
            current_field = move(current_field, current_direction)
        elif direction == 1:
            # turn right
            idx = (directions.index(current_direction) + 1) % 4
            # print(f'At {current_field} , turning right - from {current_direction} to {directions[idx]}')
            current_direction = directions[idx]
            current_field = move(current_field, current_direction)
        # i += 1

    # uncomment for first part
    # print(len(fields))
    arr = []
    for y in range(6):
        l = []
        for x in range(50):
            l.append(' ')
        arr.append(l)
    for x, y in fields:
        color = fields[(x, y)]
        if color == 1:
            arr[abs(y)][x] = "X"
            
    for y in arr:
        t = ''
        for x in y:
            t += x
        print(t)