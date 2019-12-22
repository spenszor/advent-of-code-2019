import re
from collections import deque

def deal_with_increment(deck, step):
    table = [None] * len(deck)
    dealt_cards = 0
    current_pos = 0 
    while dealt_cards < len(deck):
        table[current_pos] = deck[dealt_cards]
        dealt_cards += 1
        current_pos = (current_pos + step) % len(deck)
    return table

with open('./inputs/day22') as data:
#     data = '''
# deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1
#     '''.strip().splitlines()
    deck_size = 10007
    # deck_size = 10
    deck = list(range(deck_size))
    for instruction in data:
        # print(deck)
        if matches := re.match(r'deal with increment (-?\d+)', instruction):
            increment = int(matches.groups()[0])
            deck = deal_with_increment(deck, increment)
        elif matches := re.match(r'cut (-?\d+)', instruction):
            cut = int(matches.groups()[0])
            head = deck[:cut]
            tail = deck[cut:]
            tail.extend(head)
            deck = tail
        elif instruction.strip() == 'deal into new stack':
            deck.reverse()

    print(deck.index(2019))
# For part 2, just read the thorough explanation: https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
# There is no way I would come up with solution for this part