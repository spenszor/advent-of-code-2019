from math import gcd
from copy import deepcopy

def compare_dim(d1, d2):
    if d1 > d2:
        return -1
    elif d1 < d2:
        return 1
    else:
        return 0

def lcm(x, y):
   lcm = (x * y) // gcd(x,y)
   return lcm

def part_one(moons, velocities):
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

def part_two(moons, velocities):
    axes = ['x', 'y', 'z']
    periods = []
    for d in range(3):
        steps = 0
        seen = set()
        while True:
            for i in range(4):
                cur_moon = moons[i]
                for o in range(i + 1, i + 4):
                    c = o % 4
                    for dim in axes:
                        velocities[i][dim] += compare_dim(cur_moon[dim], moons[c][dim])
            for i in range(4):
                for dim in axes:
                    moons[i][dim] += velocities[i][dim]
            # print(f'Step {step}, positions: {moons}, velos: {velocities}')
            current_state = []
            for j in range(4):
                current_state.append(moons[j][axes[d]])
                current_state.append(velocities[j][axes[d]])
            current_state = str(current_state)

            if current_state in seen:
                print(f'Found period for {axes[d]}: {steps}')
                periods.append(steps)
                break

            steps +=1
            seen.add(current_state)
            
    print(periods)
    print(lcm(periods[0], lcm(periods[1], periods[2])))

with open('./inputs/day12') as data:
    moons = []
    velocities = []
    for line in data:
        line = line.strip()
        line = line[1:-1]
        line = line.split(", ")
        moon = {}
        for e in line:
            k, v = e.split("=")
            moon[k] = int(v)
        moons.append(moon)
        velocities.append({'x': 0, 'y': 0, 'z': 0})
    part_one(deepcopy(moons), deepcopy(velocities))
    part_two(deepcopy(moons), deepcopy(velocities))
    
