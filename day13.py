from collections import defaultdict

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
                    # read_v = params[0]
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

def solve_first(data):
    c = Computer(data)
    
    grid = defaultdict(int)
    while not c.halted:
        x = c.calculate()
        y = c.calculate()
        t = c.calculate()
        if x is not None and y is not None and t is not None:
            grid[(x, y)] = t
    count = sum(1 for v in grid.values() if v == 2)
    print(count)
    # print(grid)
    print_grid(grid)

OBJECTS = dict(zip([0, 1, 2, 3, 4], [' ', '|', '■', '-', 'o']))

def print_grid(grid):
    max_x = max(x for (x, y) in grid.keys()) + 1
    max_y = max(y for (x, y) in grid.keys()) + 1
    for y in range(max_y):
        line = ''
        for x in range(max_x):
            line += OBJECTS[grid[(x, y)]]
        print(line)

def next_move(ball_x, paddle_x):
    if ball_x < paddle_x:
      return -1
    elif ball_x == paddle_x:
      return 0
    else:
      return 1

with open('./inputs/day13') as inpt:
    parsed = list(map(lambda x: int(x), inpt.readline().split(',')))
    # solve_first(parsed.copy())
    # part 2
    parsed[0] = 2
    c = Computer(parsed)
    grid = defaultdict(int)
    current_score = 0
    current_command = 0
    ball_x = 0
    paddle_x = 0
    while not c.halted:
        x = c.calculate([current_command])
        if x == None:
            continue
        y = c.calculate()
        t = c.calculate()
        if x == -1 and y == 0:
            current_score = t
        if t == 4:
            ball_x = x
        if t == 3:
            paddle_x = x
        elif x != None and y != None and t != None:
            grid[(x, y)] = t
            current_command = next_move(ball_x, paddle_x)
        print_grid(grid)
    print(current_score)