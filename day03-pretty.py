directions_X = {'L': -1, 'R': 1, 'U': 0, 'D': 0}
directions_Y = {'L': 0, 'R': 0, 'U': 1, 'D': -1}


def get_points(A):
    x = 0
    y = 0
    total_length = 0
    path_points = {}
    for cmd in A:
        direction = cmd[0]
        length = int(cmd[1:])
        for _ in range(length):
            x += directions_X[direction]
            y += directions_Y[direction]
            total_length += 1
            if (x, y) not in path_points:
                path_points[(x, y)] = total_length
    return path_points


with open('./inputs/day03') as input:
    line_a = input.readline().strip().split(',')
    line_b = input.readline().strip().split(',')

    points_a = get_points(line_a)
    points_b = get_points(line_b)
    interesection_points = set(points_a.keys()) & set(points_b.keys())
    part1 = min([abs(x)+abs(y) for (x, y) in interesection_points])
    part2 = min([points_a[p]+points_b[p] for p in interesection_points])
    print(part1, part2)
