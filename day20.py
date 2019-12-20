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


directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def neighbours(x, y):
    for d in directions:
        yield (x + d[0], y + d[1])


with open('./inputs/temp') as data:
    raw_grid = dict()
    for y, line in enumerate(data):
        for x, char in enumerate(line.rstrip()):
            raw_grid[(x, y)] = char

    portals = defaultdict(list)
    position_to_portal = {}
    for (x, y), char in raw_grid.items():
        if char in '.# ':
            continue
        pos = None
        first_letter = char
        second_letter = None
        for n in neighbours(x, y):
            if n not in raw_grid:
                continue
            if raw_grid[n] == '.':
                pos = n
            elif raw_grid[n] not in '.# ':
                second_letter = raw_grid[n]
        if pos is None or second_letter is None:
            continue
        [first_letter, second_letter] = list(sorted([first_letter, second_letter]))
        portals[first_letter + second_letter].append(pos)
        position_to_portal[pos] = first_letter + second_letter
    # print_grid(raw_grid)
    # pprint(portals)
    # pprint(position_to_portal)

    current_pos = portals['AA'][0]
    visited_fields = deque()
    available_grid = dict()
    adjacency = defaultdict(set)
    available_grid[current_pos] = '.'
    while True:
        for d in directions:
            new_pos = move(current_pos, d)
            if new_pos not in available_grid and raw_grid[new_pos] == '.':
                if new_pos in position_to_portal:
                    telported_to = list(filter(lambda x: x != new_pos, portals[position_to_portal[new_pos]]))
                    if telported_to:
                        new_pos = telported_to[0]
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

    print(adjacency[(32,21)])