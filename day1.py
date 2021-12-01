from itertools import pairwise, islice
from collections import deque

with open("day1_input.txt") as lines:
    data = [int(x) for x in lines.readlines()]

### Simple Solution

# Part 1
print(sum(1 for a, b in pairwise(data) if b > a))

# Part 2
def triplet_sums(iterable):
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a + b + c

print(sum(1 for a, b in pairwise(triplet_sums(data)) if int(b) > int(a)))


### Overcomplicated Solution

# sliding_window recipe ripped from python docs
def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

# Part 1
print(sum(1 for a, *_, b in sliding_window(data, 2) if b > a))

# Part 2
print(sum(1 for a, *_, b in sliding_window(data, 4) if b > a))