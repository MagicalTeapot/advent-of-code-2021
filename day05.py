from collections import Counter
import re
def parse_input():
    with open("day05_input.txt") as f:
        for line in f:
            yield tuple(int(n) for n in re.findall(r"\d+", line))

def walk_line(x1, y1, x2, y2, include_diagnals):
    if x1 == x2:
        return [(x1, i) for i in range(min(y1, y2), max(y1, y2) + 1)]
    if y1 == y2:
        return [(i, y1) for i in range(min(x1, x2), max(x1, x2) + 1)]
    if include_diagnals:
        x_coords = [*range(x1, x2, 1 if x2 > x1 else -1), x2]
        y_coords = [*range(y1, y2, 1 if y2 > y1 else -1), y2]
        return zip(x_coords, y_coords)
    return []

def count_overlaps(include_diagnals):
    points = Counter([p for x in parse_input() for p in walk_line(*x, include_diagnals)])
    return sum(1 for v in points.values() if v > 1)

print("Part 1:", count_overlaps(False))
print("Part 2:", count_overlaps(True))