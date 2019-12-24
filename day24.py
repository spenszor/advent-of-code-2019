from collections import defaultdict

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

with open('./inputs/day24') as data:
    initial_state = defaultdict(int)
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
    seen = set()
    current = initial_state
    while (diversity := calculate_diversity(current)) not in seen:
        seen.add(diversity)
        current = calculate_next_state(current)

    print(diversity)
            
    

