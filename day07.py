import statistics
with open("day07_input.txt") as f:
    crabs = [int(n) for n in f.read().split(",")]

median = int(statistics.median(crabs))
print("Part 1:", sum(abs(crab - median) for crab in crabs))