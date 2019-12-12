from math import gcd

def compare_dim(d1, d2):
    if d1 > d2:
        return -1
    elif d1 < d2:
        return 1
    else:
        return 0

def compute_lcm(x, y):
   lcm = (x*y)//gcd(x,y)
   return lcm

def part_one():
    velocities = [
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 0, 'y': 0, 'z': 0}, 
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 0, 'y': 0, 'z': 0}
    ]
    moons = [{'x': 3, 'y': 3, 'z': 0},
             {'x': 4, 'y': -16, 'z': 2}, 
             {'x': -10, 'y': -6, 'z': 5},
             {'x': -3, 'y': 0, 'z': -13}]

    dims = ['x', 'y', 'z']

    for step in range(1000):
        for i in range(4):
            cur_moon = moons[i]
            for o in range(i + 1, i + 4):
                c = o % 4
                for dim in dims:
                    velocities[i][dim] += compare_dim(cur_moon[dim], moons[c][dim])
        for i in range(4):
            for dim in dims:
                moons[i][dim] += velocities[i][dim]
        # print(f'Step {step}, positions: {moons}, velos: {velocities}')
    total = 0
    for i in range(4):
        t_potential = 0
        t_kinetic = 0
        for dim in dims:
            t_potential += abs(moons[i][dim])
            t_kinetic += abs(velocities[i][dim])
        total += (t_potential * t_kinetic)
    print(total)

with open('./inputs/day12') as data:
    # TODO add parsing?
    # moons = [{'x': -1, 'y': 0, 'z': 2},
    #          {'x': 2, 'y': 10, 'z': -7}, 
    #          {'x': 4, 'y': -8, 'z': 8},
    #          {'x': 3, 'y': 5, 'z': -1}]

    velocities = [
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 0, 'y': 0, 'z': 0}, 
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 0, 'y': 0, 'z': 0}
    ]
    moons = [{'x': 3, 'y': 3, 'z': 0},
             {'x': 4, 'y': -16, 'z': 2}, 
             {'x': -10, 'y': -6, 'z': 5},
             {'x': -3, 'y': 0, 'z': -13}]

    initial = [
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 0, 'y': 0, 'z': 0}, 
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 0, 'y': 0, 'z': 0}
    ]

    dims = ['x', 'y', 'z']

    partial = []

    # def comp(velo1, velo2, dim):


    for axe in dims:
        steps = 0
        while True:
            for i in range(4):
                cur_moon = moons[i]
                for o in range(i + 1, i + 4):
                    c = o % 4
                    for dim in dims:
                        velocities[i][dim] += compare_dim(cur_moon[dim], moons[c][dim])
            for i in range(4):
                for dim in dims:
                    moons[i][dim] += velocities[i][dim]
            # print(f'Step {step}, positions: {moons}, velos: {velocities}')
            steps +=1

            same = True
            for r in range(4):
                if velocities[r][axe] != 0:
                    same = False
            if same:
                partial.append(steps)
                break
    print(partial)
    print(compute_lcm(partial[0], compute_lcm(partial[1], partial[2])))