def colinear(x1, y1, x2, y2, x3, y3):
    return (0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))) == 0
    

with open('./inputs/day10') as data:
    ast = []
    for line in data:
        ast_line = []
        for c in line:
            if c == '#':
                ast_line.append(0)
            elif c == '.':
                ast_line.append(-1)
        ast.append(ast_line)
    colinear_asteroids = dict()
    for y in range(len(ast)):
        for x in range(len(ast[0])):
            if ast[y][x] == 0 and (x,y) not in colinear_asteroids:
                for k, v in colinear_asteroids:
                    px, py = k
                    if all(not colinear(px, py, cx, cy, x, y) for (cx, cy) in v):
                        colinear_asteroids[(x, y)] = set(k)
                        colinear_asteroids[k].add((x, y))
    print(colinear_asteroids)
