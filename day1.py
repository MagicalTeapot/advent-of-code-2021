from itertools import pairwise

with open("day1_input.txt") as lines:
    data = [int(x) for x in lines.readlines()]

# Part 1
print(sum(1 for a, b in pairwise(data) if b > a))

# Part 2
def triplet_sums(iterable):
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a + b + c

print(sum(1 for a, b in pairwise(triplet_sums(data)) if int(b) > int(a)))