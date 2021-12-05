from itertools import pairwise, islice
from collections import deque
with open("day01_input.txt") as lines:
    data = [int(x) for x in lines.readlines()]

### Simple Solution
def triplet_sums(iterable):
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a + b + c

print("Part 1:", sum(1 for a, b in pairwise(data) if b > a))
print("Part 2:", sum(1 for a, b in pairwise(triplet_sums(data)) if int(b) > int(a)))

### Overcomplicated Solution, sliding_window recipe ripped from python docs
def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

print("Part 1:", sum(1 for a, *_, b in sliding_window(data, 2) if b > a))
print("Part 2:", sum(1 for a, *_, b in sliding_window(data, 4) if b > a))