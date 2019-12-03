center_x = 15000
center_y = 15000
max_size = 30000


def make_map(grid, raw_wire, symbol):
    pos_x = center_x
    pos_y = center_y
    for d in raw_wire:
        direction = d[0]
        length = int(d[1:])
        if direction == 'U':
            for y in range(pos_y, pos_y + length):
                pos_y += 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
        elif direction == 'D':
            for y in range(pos_y, pos_y + length):
                pos_y -= 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
        elif direction == 'L':
            for x in range(pos_x, pos_x + length):
                pos_x -= 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
        else:
            for x in range(pos_x, pos_x + length):
                pos_x += 1
                s = check(grid[pos_x][pos_y], symbol)
                grid[pos_x][pos_y] = s
    return grid

def check(value, current_symbol):
    if value != None and value != current_symbol:
        return 'X'
    else:
        return current_symbol

with open('./inputs/day03') as input:
    split_wire1 = input.readline().split(',')
    grid = [[None for _ in range(max_size)] for _ in range(max_size)]
    grid = make_map(grid, split_wire1, 'w1')
    print(filter(lambda x: x != None, grid[center_x]))
    split_wire2 = input.readline().split(',')
    grid = make_map(grid, split_wire2, 'w2')
    min_distance = 10000000
    for x in range(max_size):
        for y in range(max_size):
            if grid[x][y] == 'X':
                dist = abs(center_x - x) + abs(center_y - y)
                if dist != 0 and dist < min_distance:
                    min_distance = dist
    print(min_distance)
