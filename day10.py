from collections import defaultdict

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
    colinear_asteroids = defaultdict(set())
    for line in ast:
        for point in line:
            if point 
