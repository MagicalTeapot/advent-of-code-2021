from typing import final


coords = set()
folds = []
with open("day13_input.txt") as f:
    lines = (l.strip() for l in f if l.strip())
    for i, line in enumerate(lines):
        if line.startswith("fold"):
            _, _, fold = line.split()
            axis, position = fold.split("=")
            folds.append((axis, int(position)))
        else:
            x, y = line.split(",")
            coords.add((int(x), int(y)))

def apply_fold(axis, pos, coords):
    new_coords = set()
    for x, y in coords:
        if axis == "x" and x >= pos:
            new_coords.add((2 * pos - x, y))
        elif axis == "y" and y >= pos:
            new_coords.add((x, 2 * pos - y))
        else:
            new_coords.add((x, y))
    return new_coords

print("Part 1:", len(apply_fold(*folds[0], coords)))

print("Part 2:")
final_coords = coords
for fold in folds:
    final_coords = apply_fold(*fold, final_coords)

max_x = max(x for x, _ in final_coords)
max_y = max(y for _, y in final_coords)
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if (x, y) in final_coords:
            print("█", end="")
        else:
            print(" ", end="")
    print()