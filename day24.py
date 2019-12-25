from collections import defaultdict
from pprint import pprint

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

def your_neighbour_bugs(grid, x, y):
    return sum(1 for coords in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if grid[coords] == '#')

def calculate_diversity(grid):
    return sum(2**i for i, k in enumerate(grid) if grid[k] == '#')

def calculate_next_state(grid):
    current = defaultdict(int)
    for y in range(5):
        for x in range(5):
            proc = grid[(x, y)]
            if proc == '#':
                if your_neighbour_bugs(grid, x, y) == 1:
                    current[(x, y)] = '#'
                else:
                    current[(x, y)] = '.'
            elif proc == '.':
                bugs = your_neighbour_bugs(grid, x, y)
                if bugs == 1 or bugs == 2:
                    current[(x, y)] = '#'
                else:
                    current[(x, y)] = '.'
    return current

def solve_first(initial_state):
    current = initial_state
    seen = set()
    while (diversity := calculate_diversity(current)) not in seen:
        seen.add(diversity)
        current = calculate_next_state(current)

    return diversity

def your_neighbour_bugs_rec(grid, x, y, z):
    total = 0
    for (cx, cy) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if (cx, cy) == (2, 2): # neighbour is center => we must go deeper
            if x < cx:
                # inner left
                total += sum(1 for y in range(5) if grid[(0, y, z + 1)] == '#')
            elif x > cx:
                # inner right
                total += sum(1 for y in range(5) if grid[(4, y, z + 1)] == '#')
            elif y < cy:
                # inner top
                total += sum(1 for x in range(5) if grid[(x, 0, z + 1)] == '#')
            elif y > cy:
                # inner bottom
                total += sum(1 for x in range(5) if grid[(x, 4, z + 1)] == '#')
        if cx == -1 and grid[(1, 2, z - 1)] == '#':
            # calculate left middle
            total += 1
        if cx == 5 and grid[(3, 2, z - 1)] == '#':
            # calculate right middle
            total += 1
        if cy == -1 and grid[(2, 1, z - 1)] == '#':
            # calculate top middle
            total += 1
        if cy == 5 and grid[(2, 3, z - 1)] == '#':
            # calculate bottom middle
            total += 1
        if grid[(cx, cy, z)] == '#':
            total += 1
    return total

def mutate(grid, min_depth, max_depth):
    current = defaultdict(lambda:'.')
    for z in range(1) if min_depth == 0 and max_depth == 0 else range(min_depth, max_depth + 1):
        for y in range(5):
            for x in range(5):
                proc = grid[(x, y, z)]
                if x == 2 and y == 2: # don't process middle
                    continue
                if proc == '#':
                    if your_neighbour_bugs_rec(grid, x, y, z) == 1:
                        current[(x, y, z)] = '#'
                    else:
                        current[(x, y, z)] = '.'
                elif proc == '.':
                    bugs = your_neighbour_bugs_rec(grid, x, y, z)
                    if bugs == 1 or bugs == 2:
                        current[(x, y, z)] = '#'
                    else:
                        current[(x, y, z)] = '.'
    return current

def print_level(grid, level):
    temp = defaultdict(lambda: '.')
    for y in range(5):
        for x in range(5):
            temp[(x, y)] = grid[(x, y, level)]
    print(f'Printing level {level}')
    print_grid(temp)

def solve_second(initial_state):
    current = defaultdict(lambda: '.')
    for (x, y) in initial_state.keys():
        current[(x, y, 0)] = initial_state[(x, y)]
    for minute in range(1, 201):
        current = mutate(current, -1 * minute, 1 * minute)
    # print_level(current, -5)
    # print_level(current, -2)
    # print_level(current, -1)
    # print_level(current, 0)
    # print_level(current, 1)
    # print_level(current, 2)
    # print_level(current, 5)
    total_bugs = sum(1 for k in current if current[k] == '#')
    return total_bugs

with open('./inputs/day24') as data:
    initial_state = defaultdict(lambda: '.')
    # test = '''
    # ....#
    # #..#.
    # #..##
    # ..#..
    # #....
    # '''.strip().splitlines()
    for y, line in enumerate(data):
        for x, ch in enumerate(line.strip()):
            initial_state[(x, y)] = ch
    # print_grid(initial_state)
    print(f'First solution: {solve_first(initial_state)}')
    print(f'Second solution: {solve_second(initial_state)}')
    
            
    

