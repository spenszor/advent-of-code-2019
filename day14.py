from collections import defaultdict
from math import ceil

def parse_substance(s):
    amount, chemical = s.split()
    return chemical, int(amount)


def parse_reaction(reaction):
    source, result  = reaction.split(' => ')
    output, num_units = parse_substance(result)
    ingredients = dict(parse_substance(s) for s in source.split(', '))
    return (output, (num_units, ingredients))


def parse_input(s):
    return dict(parse_reaction(line) for line in s.splitlines())

with open('./inputs/day14') as f:
    reactions = parse_input(f.read())

def calculate_components(chemical, amount, wastes):
    quantity, ingredients = reactions[chemical]
    multiples = ceil(amount / quantity)

    wastes[chemical] += multiples * quantity - amount

    components_needed = dict()
    for chemical, amount in ingredients.items():
        total_amount_needed = amount * multiples
        usable_waste = min(total_amount_needed, wastes[chemical])
        total_amount_needed -= usable_waste
        wastes[chemical] -= usable_waste
        components_needed[chemical] = total_amount_needed

    return components_needed


def calculate_needed_ore(fuel):
    substances_needed = defaultdict(int)
    substances_needed['FUEL'] = fuel

    wastes = defaultdict(int)

    total_ore = 0
    while substances_needed:
        chemical, amount = substances_needed.popitem()

        components_needed = calculate_components(chemical, amount, wastes)
        if 'ORE' in components_needed:
            total_ore += components_needed.pop('ORE')

        for chemical, amount in components_needed.items():
            substances_needed[chemical] += amount

    return total_ore

def binary_search(start, end, fun):
    while end - start > 1:
        middle = start + (end - start) // 2
        if fun(middle) == -1:
            end = middle
        else:
            start = middle
    return start

print(f'First solution {calculate_needed_ore(1)}')
print(f'Second soultion {int(binary_search(0, 1e12, lambda fuel: -1 if calculate_needed_ore(fuel) > 1e12 else 1))}')
