from collections import deque, defaultdict
from pprint import pprint
from itertools import combinations

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

def neighs(p):
    return [(p[0]+1, p[1]), (p[0], p[1]-1), (p[0]-1, p[1]), (p[0], p[1]+1)]

def build_graph(floor):
    graph = {}
    for n in floor:
        neigh = set()
        for x in neighs(n):
            if x in floor and floor[x] != '#':
                neigh.add(x)
        graph[n] = neigh
    return graph

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

def solve_first():
    with open('./inputs/day18') as data:
        test = '''
            ########################
            #@..............ac.GI.b#
            ###d#e#f################
            ###A#B#C################
            ###g#h#i################
            ########################
        '''.strip().splitlines()
        # data = test
        raw_grid = dict()
        important_points = dict()
        door_locs = dict()
        keys = dict()
        start = None
        for y, row in enumerate(data):
            stripped =  row.strip()
            for x in range(len(stripped)):
                raw_grid[(x, y)] = stripped[x]
                if stripped[x] != '.' and stripped[x] != '#':
                    important_points[stripped[x]] = (x, y)
                    if stripped[x].islower():
                        keys[stripped[x]] = (x, y)
                    elif stripped[x].isupper():
                        door_locs[(x, y)] = stripped[x]
                    elif stripped[x] == '@':
                        start = (x, y)

        adjacency = build_graph(raw_grid)
        print('Grid traversed')

        # index distances to and between available keys and doors on the way (also include starting point):
        #{
        #   '@': {
        #     'a': (2, {}),
        #     'b': (4, {'A'})
        #     },
        #   'a': { 'b': (6, {'A'}) },
        #   'b': { 'a': (6, {'A'}) }
        #}

        keys['@'] = start
        distances = defaultdict(dict)
        for combination in combinations(keys.keys(), 2):
            start_symbol, end_symbol = combination
            start = keys[start_symbol]
            end = keys[end_symbol]
            path = bfs_shortest_path(adjacency, start, end) # -1 on path len as it contains start
            doors_on_path = set(door_locs[step].lower() for step in path if step in door_locs)
            if end_symbol != '@':
                distances[start_symbol][end_symbol] = (len(path) - 1, doors_on_path)
            if start_symbol != '@':
                distances[end_symbol][start_symbol] = (len(path) - 1, doors_on_path)
        # pprint(distances)
        keys.pop('@')
        print('Distances build, searching for answer')

        cache = {}
        def traverse(current_key, keys_to_collect):
            if len(keys_to_collect) == 0:
                return 0

            cache_key = current_key + ''.join(keys_to_collect)
            if cache_key in cache:
                return cache[cache_key]

            shortest = 10e10
            for k in keys_to_collect:
                length, doors = distances[current_key][k]
                if length >= shortest: 
                    continue # don't bother - too long path
                if not doors.isdisjoint(keys_to_collect): 
                    continue # don't have all needed keys
                tail = traverse(k, keys_to_collect - {k})
                if shortest > length + tail: 
                    shortest = length + tail
            cache[cache_key] = shortest
            return shortest
        
        solution_one = traverse('@', set(keys.keys()))
        print(f'Solution one: {solution_one}')

def solve_second():
    with open('./inputs/day18_p2') as data:
        test = '''
                #############
                #g#f.D#..h#l#
                #F###e#E###.#
                #dCba@#@BcIJ#
                #############
                #nK.L@#@G...#
                #M###N#H###.#
                #o#m..#i#jk.#
                #############
            '''.strip().splitlines()
        # data = test

        raw_grid = dict()
        important_points = dict()
        door_locs = dict()
        keys = dict()
        starting_points = []
        for y, row in enumerate(data):
            stripped =  row.strip()
            for x in range(len(stripped)):
                raw_grid[(x, y)] = stripped[x]
                if stripped[x] != '.' and stripped[x] != '#':
                    important_points[stripped[x]] = (x, y)
                    if stripped[x].islower():
                        keys[stripped[x]] = (x, y)
                    elif stripped[x].isupper():
                        door_locs[(x, y)] = stripped[x]
                    elif stripped[x] == '@':
                        starting_points.append((x, y))

        adjacency = build_graph(raw_grid)
        print('Grid traversed')

        for i, start in enumerate(starting_points):
            keys[str(i)] = start
        distances = defaultdict(dict)
        for combination in combinations(keys.keys(), 2):
            start_symbol, end_symbol = combination
            start = keys[start_symbol]
            end = keys[end_symbol]
            path = bfs_shortest_path(adjacency, start, end) # -1 on path len as it contains start
            if path: # path between different parts of maze might not exist
                doors_on_path = set(door_locs[step].lower() for step in path if step in door_locs)
                if not end_symbol.isdigit():
                    distances[start_symbol][end_symbol] = (len(path) - 1, doors_on_path)
                if not start_symbol.isdigit():
                    distances[end_symbol][start_symbol] = (len(path) - 1, doors_on_path)
        # pprint(distances)
        for i in range(4):
            keys.pop(str(i))
        print('Distances build, searching for answer')
        cache = {}
        def traverse(current_keys, keys_to_collect):
            if len(keys_to_collect) == 0:
                return 0

            cache_key = ''.join(sorted(current_keys)) + ''.join(sorted(keys_to_collect))
            if cache_key in cache:
                return cache[cache_key]

            shortest = 10e10
            for k in keys_to_collect:
                for current_key in current_keys:
                    if k not in distances[current_key]: 
                        continue
                    length, doors = distances[current_key][k]
                    if length >= shortest: 
                        continue # don't bother - too long path
                    if not doors.isdisjoint(keys_to_collect): 
                        continue # don't have all needed keys
                    tail = traverse((current_keys - {current_key}) | {k}, keys_to_collect - {k})
                    if shortest > length + tail: 
                        shortest = length + tail
            cache[cache_key] = shortest
            return shortest
            
        solution_two = traverse({'0','1','2','3'}, set(keys.keys()))
        print(f'Solution two: {solution_two}')

solve_first()
solve_second()


        