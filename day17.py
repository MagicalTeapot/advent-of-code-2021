from itertools import product
x1, x2, y2, y1 = 96, 125, -144, -98

n = -y2 - 1
print("Part 1:", n * (n + 1) // 2) # Triangle numbers

def hits_target(dx, dy):
    x, y = 0, 0
    while x <= x2 and y >= y2:
        if x >= x1 and y <= y1:
            return True
        x += dx
        y += dy
        dx = max(dx - 1, 0)
        dy -= 1
    return False

# These run on the assumption that the target is down and to the right
# min x: smallest n for which the n-th triangle number is between x1 and x2. But I just used 0 here
# max x: x2, jumping there in one go
# min y: y2, jumping there in one go
# max y: "n" from part 1
print("Part 2:", sum(hits_target(*p) for p in product(range(x2 + 1), range(y2, n + 1))))