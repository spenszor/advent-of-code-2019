from_v = 278384
to_v = 824795

correct_pws = 0
for password in range(from_v, to_v+1):
    str_pw = str(password)
    if len(set(str_pw)) <= 5 and str_pw == ''.join(sorted(str_pw)):
        correct_pws += 1
print(f"Part 1: {correct_pws}")

from collections import Counter

correct_pws = 0
for password in range(from_v, to_v+1):
    str_pw = str(password)
    if 2 in Counter(str_pw).values() and str_pw == ''.join(sorted(str_pw)):
        correct_pws += 1
print(f"Part 2: {correct_pws}")