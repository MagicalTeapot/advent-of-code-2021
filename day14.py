import itertools
import collections
with open("day14_input.txt") as f:
    template = next(f).strip()
    mappings = {}
    lines = (l.strip() for l in f if l.strip())
    for line in lines:
        pair, middle = line.split(" -> ")
        mappings[pair] = middle

def next_step(template, mappings):
    ret = template[0]
    for lhs, rhs in itertools.pairwise(template):
        if lhs + rhs in mappings:
            ret += mappings[lhs + rhs]
        ret += rhs
    return ret

for _ in range(40):
    template = next_step(template, mappings)

counts = collections.Counter(template)
max_val = max(v for v in counts.values())
min_val = min(v for v in counts.values())
print(max_val - min_val)