from itertools import pairwise
from collections import Counter
with open("day14_input.txt") as f:
    template = next(f).strip()
    mappings = dict(l.strip().split(" -> ") for l in f if l.strip())

def next_step(state):
    new_state = Counter()
    for (lhs, rhs), middle in mappings.items():
        new_state[lhs, middle] += state[lhs, rhs]
        new_state[middle, rhs] += state[lhs, rhs]
    return new_state

def run(steps):
    state = Counter(pairwise(template))
    for _ in range(steps):
        state = next_step(state)

    counts = Counter({template[0]: 1})
    for (_, rhs), count in state.items():
        counts[rhs] += count
    return (max(counts.values()) - min(counts.values()))

print("Part 1:", run(10))
print("Part 2:", run(40))