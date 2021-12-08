import statistics
import math
with open("day07_input.txt") as f:
    crabs = [int(n) for n in f.read().split(",")]

median = int(statistics.median(crabs))
print("Part 1:", sum(abs(crab - median) for crab in crabs))

def triangle(x, y):
    n = abs(x - y)
    return (n * (n + 1)) // 2

mean = sum(crabs) / len(crabs)
print("Part 2:", min(
    int(sum(triangle(crab, math.floor(mean)) for crab in crabs)),
    int(sum(triangle(crab, math.ceil(mean)) for crab in crabs))
))
