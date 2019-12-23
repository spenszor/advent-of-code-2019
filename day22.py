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

def solve_first(data):
    # data = '''
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

# For part 2... There is no way I would come up with solution for this. 
# Just read the thorough explanation: https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
# At least I learned somethin new
def solve_second(data):
    cards = 119315717514047
    repeats = 101741582076661

    def inv(n):
        # gets the modular inverse of n
        # as cards is prime, use Euler's theorem
        return pow(n, cards-2, cards)
    def get(offset, increment, i):
        # gets the ith number in a given sequence
        return (offset + i * increment) % cards
    
    # increment = 1 = the difference between two adjacent numbers
    # doing the process will multiply increment by increment_mul.
    increment_mul = 1
    # offset = 0 = the first number in the sequence.
    # doing the process will increment this by offset_diff * (the increment before the process started).
    offset_diff = 0
    
    for instruction in data:
        # print(deck)
        if matches := re.match(r'deal with increment (-?\d+)', instruction):
            increment = int(matches.groups()[0])
            # difference between two adjacent numbers is multiplied by the
            # inverse of the increment.
            increment_mul *= inv(increment)
            increment_mul %= cards
        elif matches := re.match(r'cut (-?\d+)', instruction):
            cut = int(matches.groups()[0])
            # shift cut left
            offset_diff += cut * increment_mul
            offset_diff %= cards
        elif instruction.strip() == 'deal into new stack':
            # reverse sequence.
            # instead of going up, go down.
            increment_mul *= -1
            increment_mul %= cards
            # then shift 1 left
            offset_diff += increment_mul
            offset_diff %= cards

    def get_sequence(iterations):
        # calculate (increment, offset) for the number of iterations of the process
        # increment = increment_mul^iterations
        increment = pow(increment_mul, iterations, cards)
        # offset = 0 + offset_diff * (1 + increment_mul + increment_mul^2 + ... + increment_mul^iterations)
        # use geometric series.
        offset = offset_diff * (1 - increment) * inv((1 - increment_mul) % cards)
        offset %= cards
        return increment, offset

    increment, offset = get_sequence(repeats)
    print(get(offset, increment, 2020))

with open('./inputs/day22') as data:
    solve_first(data)
    data.seek(0)
    solve_second(data)