from collections import deque, defaultdict
from pprint import pprint
INSTRUCTION_POINTER_MAPPING = [-1, +4, +4, +2, +2, 0, 0, +4, +4, +2]

class Computer:
    def __init__(self, memory):
        self.memory = memory.copy()
        self.current_pos = 0
        self.halted = False
        self.last_output = 0
        self.relative_base = 0

    def calculate(self, param = None):
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
                if param:
                    self.write_by_mode(modes[-1], self.current_pos + 1, param)
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

def move(pos, vec):
    return (pos[0] + vec[0], pos[1] + vec[1])

def print_grid(grid):
    max_x = max(x for (x, y) in grid.keys()) + 1
    min_x = min(x for (x, y) in grid.keys())
    max_y = max(y for (x, y) in grid.keys()) + 1
    min_y = min(y for (x, y) in grid.keys())
    for y in range(min_y, max_y):
        line = ''
        for x in range(min_x, max_x):
            line += grid.get((x, y), ' ')
        print(line)

def bfs_shortest_path(graph, start, goal):
    explored = []
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    return new_path
            explored.append(node)

def deepest(grid, oxy_pos):
    directions = [1, 2, 3, 4]
    mappings = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    q = [oxy_pos]
    depths = {oxy_pos: 0}
    while q:
        cur = q.pop(0)
        for d in directions:
            nx = move(cur, mappings[d - 1])
            if grid[nx] == ' ' and nx not in depths:
                q.append(nx)
                depths[nx] = depths[cur] + 1
    return max(depths.values())
# north (1), south (2), west (3), and east (4)
with open('./inputs/day15') as inpt:
    parsed = list(map(lambda x: int(x), inpt.readline().split(',')))
    c = Computer(parsed)
    current_pos = (0, 0)
    grid = dict()
    adj = defaultdict(set)
    directions = [1, 2, 3, 4]
    mappings = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    visited_fields = deque()
    i = 0
    while not c.halted and i < 5000:
        for d in directions:
            if move(current_pos, mappings[d - 1]) not in grid:
                new_pos = move(current_pos, mappings[d - 1])
                res = c.calculate(d)
                if res == 0:
                    grid[new_pos] = '▮'
                elif res == 1:
                    visited_fields.appendleft((current_pos, d))
                    # adj[current_pos].add(new_pos)
                    adj[new_pos].add(current_pos)
                    current_pos = new_pos
                    grid[new_pos] = ' '
                    break
                elif res == 2:
                    visited_fields.appendleft((current_pos, d))
                    # adj[current_pos].add(new_pos)
                    adj[new_pos].add(current_pos)
                    current_pos = new_pos
                    grid[new_pos] = 'O'
                    break
        else:
            if visited_fields:
                current_pos, d = visited_fields.popleft()
                if d == 1:
                    d = 2
                elif d == 2:
                    d = 1
                elif d == 3:
                    d = 4
                elif d == 4:
                    d = 3
                c.calculate(d)
            i += 1
    dest = list(grid.keys())[list(grid.values()).index('O')]
    print_grid(grid)
    path = bfs_shortest_path(adj, dest, (0, 0))
    print(f'First solution: {len(path) - 1}')
    print(f'Second solution: {deepest(grid, dest)}')

    
