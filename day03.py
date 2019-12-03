from tqdm import tqdm

center_x = 1954
center_y = 1759
max_size_y = 20000
max_size_x = 17000

#227
#1954
#18497
#1759
#21809

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

def path_to_point(raw_wire, px, py):
    distance = 0
    pos_x = center_x
    pos_y = center_y
    for d in raw_wire:
        direction = d[0]
        length = int(d[1:])
        if direction == 'U':
            for y in range(pos_y, pos_y + length):
                pos_y += 1
                distance += 1
                if pos_x == px and pos_y == py:
                    return distance
        elif direction == 'D':
            for y in range(pos_y, pos_y + length):
                pos_y -= 1
                distance += 1
                if pos_x == px and pos_y == py:
                    return distance
        elif direction == 'L':
            for x in range(pos_x, pos_x + length):
                pos_x -= 1
                distance += 1
                if pos_x == px and pos_y == py:
                    return distance                
        else:
            for x in range(pos_x, pos_x + length):
                pos_x += 1
                distance += 1
                if pos_x == px and pos_y == py:
                    return distance                
    return distance

def check(value, current_symbol):
    if value != None and value != current_symbol:
        return 'X'
    else:
        return current_symbol

with open('./inputs/day03') as input:
    split_wire1 = input.readline().strip().split(',')
    grid = [[None for _ in range(max_size_y)] for _ in range(max_size_x)]
    grid = make_map(grid, split_wire1, 'w1')
    split_wire2 = input.readline().strip().split(',')
    grid = make_map(grid, split_wire2, 'w2')
    min_distance = 10000000
    points = []
    for x in tqdm(range(max_size_x)):
        for y in range(max_size_y):
            if grid[x][y] == 'X':
                points.append((x, y))
                dist = abs(center_x - x) + abs(center_y - y)
                if dist != 0 and dist < min_distance:
                    min_distance = dist
    print(min_distance)

    shortest_path = 10000000
    for (x, y) in tqdm(points):
        p1 = path_to_point(split_wire1, x, y)
        p2 = path_to_point(split_wire2, x, y)
        total = p1 + p2
        if total < shortest_path:
            shortest_path = total
    print(shortest_path)