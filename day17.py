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

def move(pos, vec):
    return (pos[0] + vec[0], pos[1] + vec[1])

def print_grid(grid):
    max_x = max(x for (x, y) in grid.keys()) + 1
    min_x = min(x for (x, y) in grid.keys())
    max_y = max(y for (x, y) in grid.keys()) + 1
    min_y = min(y for (x, y) in grid.keys())
    print(min_x, max_x)
    print(min_y, max_y)
    for y in range(min_y, max_y):
        line = ''
        for x in range(min_x, max_x):
            line += grid.get((x, y), ' ')
        print(line)

def is_intersection(grid, x, y):
    return grid[(x+1, y)] == '#' and grid[(x, y + 1)] == '#' and grid[(x - 1, y)] == '#' and grid[(x, y - 1)] == '#'

with open('./inputs/day17') as data:
    parsed = list(map(lambda x: int(x), data.readline().split(',')))
    # part one
    c = Computer(parsed)
    current_pos = (0, 0)
    grid = dict()
    while not c.halted:
        ch = c.calculate()
        if ch == 10:
            current_pos = (0, current_pos[1] + 1)
        elif ch:
            grid[current_pos] = chr(ch)
            current_pos = (current_pos[0] + 1, current_pos[1])
    
    # print_grid(grid)
    alignment_params = 0
    for y in range(1, 38):
        for x in range(1, 40):
            if grid[(x, y)] == '#' and is_intersection(grid, x, y):
                alignment_params += x * y
    print(f'First solution: {alignment_params}')

    #part two
    # ascii codes for characters
    R = ord('R')
    L = ord('L')
    CM = ord(',')
    NL = 10
    A = ord('A')
    B = ord('B')
    C = ord('C')
    parsed[0] = 2 # modifies the way program works (see instructions)
    # The path deduced manually (modern text editors help highlighting patterns if you write the path in a way suggested in instructions)
    encoded_path = [
        A, CM, B, CM, A, CM, B, CM, C, CM, A, CM, B, CM, C, CM, A, CM, C, NL, # path
        R, CM, ord('6'), CM, L, CM, ord('6'), CM, L, CM, ord('1'), ord('0'), NL, # instruction A
        L, CM, ord('8'), CM, L, CM, ord('6'), CM, L, CM, ord('1'), ord('0'), CM, L, CM, ord('6'), NL, # instruction B
        R, CM, ord('6'), CM, L, CM, ord('8'), CM, L, CM, ord('1'), ord('0'), CM, R, CM, ord('6'), NL, # instruction C
        ord('n'), NL
    ]
    c = Computer(parsed, encoded_path)
    while not c.halted:
        val = c.calculate()
        if val and val < 1000:
            print(chr(val), end='')
        elif val:
            print(f'Second solution: {val}')