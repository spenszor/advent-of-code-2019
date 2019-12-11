from math import gcd, atan2

def normalize_change(pov, p):
    dx, dy = p[0] - pov[0], p[1] - pov[1]
    g = abs(gcd(dx, dy))
    return dx // g, dy // g

# if normalized vector of change between two asteroids is the same it means they are colinear
def visible_from(pov, other_points):
    return set(map(lambda p: normalize_change(pov, p) ,other_points))

def add_pairs(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]

with open('./inputs/day10') as data:
    ast = []
    for line in data:
        ast_line = []
        for c in line.strip():
            ast_line.append(c)
        ast.append(ast_line)
    asteroids = []
    for y in range(len(ast)):
        for x in range(len(ast[0])):
            if ast[x][y] == '#':
                asteroids.append((x, y))
    part1 = max(len(visible_from(p, filter(lambda pt: pt != p, asteroids))) for p in asteroids)
    print(part1)

    # part 2
    t = [(p, visible_from(p, filter(lambda pt: pt != p, asteroids))) for p in asteroids]
    t.sort(key = lambda x: len(x[1]), reverse=True)
    base, targets = t[0]
    temp = [(atan2(change_y, change_x), (change_x, change_y)) for change_x, change_y in targets]
    temp.sort(reverse=True) # sort by angle descending
    change_x, change_y = temp[199][1]
    x, y = base[0]+change_x, base[1] + change_y
    while (x, y) not in asteroids:
        x = x + change_x
        y = y + change_y
    part2 = 100*y+x
    print(part2)
    
# Original solution to first task
# def is_between(p1, p2, p3):
#     return p1 <= p3 <= p2 or p2 <= p3 <= p1
#
# def are_colinear(p1, p2, p3):
#     return (p2[0] - p1[0]) * (p3[1] - p1[1]) == (p3[0] - p1[0]) * (p2[1] - p1[1])
#
# def location(ast_map):
#     pos_locs = []
#     for y, row in enumerate(ast_map):
#         for x, col in enumerate(row):
#             if col == '#':
#                 pos_locs.append((x, y))
#     print(len(pos_locs))
#     max_vis = [0]
#     for p1 in pos_locs:  # current location
#         count = 0
#         for p2 in pos_locs:  # can curr see this location
#             blocked = False
#             for p3 in pos_locs:  # is p2 blocked by p3
#                 if p1 == p2 or p2 == p3 or p3 == p1:
#                     # same points
#                     continue
#                 if are_colinear(p1, p2, p3):
#                     if p1[0] != p2[0]:
#                         if is_between(p1[0], p3[0], p2[0]):
#                             blocked = True
#                     else:
#                         if is_between(p1[1], p3[1], p2[1]):
#                             blocked = True
#                 if blocked:
#                     break
#             if not blocked:
#                 count += 1
#         if count > max_[0]:
#             max_vis = [count-1, p1]
#     return max_vis


# print(location(data))
