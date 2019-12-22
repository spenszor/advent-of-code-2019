def parse(raw_data):
    n, m = len(raw_data), len(raw_data[0])
    grid = set() 
    portals = {}
    for i in range(n):
        for j in range(m):
            if raw_data[i][j] == '.':
                grid.add((i, j))
            elif raw_data[i][j].isupper():
                if i < n-1 and raw_data[i+1][j].isupper():
                    t = (i-1, j) if raw_data[i-1][j] == '.' else (i+2, j)
                    if raw_data[i][j]+raw_data[i+1][j] in portals:
                        portals[raw_data[i][j]+raw_data[i+1][j]].append(t)
                    else:
                        portals[raw_data[i][j]+raw_data[i+1][j]] = [t]
                elif j < m-1 and raw_data[i][j+1].isupper():
                    t = (i, j-1) if raw_data[i][j-1] == '.' else (i, j+2)
                    if raw_data[i][j]+raw_data[i][j+1] in portals:
                        portals[raw_data[i][j]+raw_data[i][j+1]].append(t)
                    else:
                        portals[raw_data[i][j]+raw_data[i][j+1]] = [t]
    return grid, portals

def neighs(p):
    return [(p[0]+1, p[1]), (p[0], p[1]-1), (p[0]-1, p[1]), (p[0], p[1]+1)]

def build_graph(floor, gates):
    graph = {}
    for n in floor:
        neigh = []
        for x in neighs(n):
            if x in floor:
                neigh.append(x)
        for g in gates.values():
            if len(g) == 2 and n in g:
                neigh.append(g[(g.index(n)+1) % 2])
        graph[n] = neigh
    return graph

def bfs(graph, start, end):
    queue = [(start, 0)]
    seen = set([start])
    while queue:
        v = queue.pop(0)
        if v[0] == end:
            return v[1]
        for n in graph[v[0]]:
            if n not in seen:
                queue.append((n, v[1]+1))
                seen.add(n)

def solve_first(data):
    grid, portals = parse(data)
    graph = build_graph(grid, portals)
    return bfs(graph, portals['AA'][0], portals['ZZ'][0])

def build_graph2(floor, gates, inp):
    h, w = len(inp), len(inp[0])
    graph = {}
    for n in floor:
        neigh = []
        for x in neighs(n):
            if x in floor:
                neigh.append((x, 0))
        for g in gates.values():
            if len(g) == 2 and n in g:
                if n[0] in [2, h-3] or n[1] in [2, w-3]:
                    neigh.append((g[(g.index(n)+1) % 2], -1))
                else:
                    neigh.append((g[(g.index(n)+1) % 2], 1))
        graph[n] = neigh
    return graph

def bfs2(graph, start, end):
    queue = [(start, 0, 0)]
    seen = set([(start, 0)])
    while queue:
        v = queue.pop(0)
        if v[0] == end and v[1] == 0:
            return v[2]
        for n in graph[v[0]]:
            if v[1] + n[1] < 0:
                continue
            if (n[0], v[1]+n[1]) not in seen:
                queue.append((n[0], v[1]+n[1], v[2]+1))
                seen.add((n[0], v[1]+n[1]))

def solve_second(data):
    grid, portals = parse(data)
    graph = build_graph2(grid, portals, data)
    return bfs2(graph, portals['AA'][0], portals['ZZ'][0])

with open('./inputs/day20') as data:
    raw_input = data.read().split('\n')[:-1]
    print(f'Solution one: {solve_first(raw_input)}')
    print(f'Solution two: {solve_second(raw_input)}')