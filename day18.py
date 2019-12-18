from collections import deque, defaultdict
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


def move(pos, vec):
    return (pos[0] + vec[0], pos[1] + vec[1])

with open('./inputs/day18') as data:
    raw_grid = dict()
    important_points = dict()
    y = 0
    for row in data:
        stripped =  row.strip()
        for x in range(len(stripped)):
            raw_grid[(x, y)] = stripped[x]
            if stripped[x] != '.' and stripped[x] != '#':
                important_points[stripped[x]] = (x, y)
        y += 1
    print_grid(raw_grid)
    # traverse available space to build adjacency list
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    visited_fields = deque()
    current_pos = important_points['@']
    available_grid = dict()
    adjacency = defaultdict(set)
    available_grid[current_pos] = '.'
    while True:
        for d in directions:
            new_pos = move(current_pos, d)
            if new_pos not in available_grid and (raw_grid[new_pos] == '.' or raw_grid[new_pos].islower()):
                adjacency[current_pos].add(new_pos)
                adjacency[new_pos].add(current_pos)
                visited_fields.append(current_pos)
                current_pos = new_pos
                available_grid[new_pos] = '.'
                break
        else:
            if visited_fields:
                current_pos = visited_fields.pop()
            else:
                print_grid(available_grid)
                break

    # index distances to and between available keys and doors on the way (also include starting point):
    #{
    #   '@': {
    #     'a': (2, {}),
    #     'b': (4, {'A'})
    #     },
    #   'a': { 'b': (6, {'A'}) },
    #   'b': { 'a': (6, {'A'}) }
    #}
    # Finish once all keys collected