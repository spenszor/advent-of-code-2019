
def make_map(grid, raw_wire, symbol):
    pos_x = 5000
    pos_y = 5000
    for d in raw_wire:
        direction = d[0]
        length = int(d[1:])
        if direction == 'U':
            for y in range(pos_y, length):
                pos_y += 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
        elif direction == 'D':
            for y in range(pos_y, length):
                pos_y -= 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
        elif direction == 'L':
            for x in range(pos_x, length):
                pos_x -= 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
        else:
            for x in range(pos_x, length):
                pos_x += 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s

def check(value, current_symbol):
    if value is not None and value != current_symbol:
        print('got cross')
        return 'X'
    else:
        return current_symbol

with open('./inputs/day03') as input:
    split_wire1 = input.readline().split(',')
    grid = [[None for _ in range(10000)] for _ in range(10000)]
    make_map(grid, split_wire1, 'w1')
    split_wire2 = input.readline().split(',')
    make_map(grid, split_wire2, 'w2')
    min_distance = 10000000
    for x in range(10000):
        for y in range(10000):
            if grid[x][y] == 'X':
                dist = abs(5000 - x) + abs(5000 - y)
                if dist < min_distance:
                    min_distance = dist
    print(min_distance)
