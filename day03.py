from collections import Counter
with open("day03_input.txt") as f:
    data = tuple(line.strip() for line in f)

def bit_counts(values):
    bins = [Counter() for _ in range(12)]
    for value in values:
        for idx, bit in enumerate(value):
            bins[idx][bit] += 1
    return bins

def filter_by_criteria(values, bit_criteria):
    for bit in range(12):
        counts = bit_counts(values)[bit]
        if len(values := [v for v in values if v[bit] == bit_criteria(counts)]) == 1:
            return int(values[0], base=2)

gamma_bits = [b.most_common()[0][0] for b in bit_counts(data)]
gamma_val = int("".join(gamma_bits), base=2)
print("Part 1:", gamma_val * (int("1"*12, base=2) - gamma_val))

oxy = filter_by_criteria(data, lambda c: "1" if c["1"] >= c["0"] else "0")
co2 = filter_by_criteria(data, lambda c: "0" if c["0"] <= c["1"] else "1")
print("Part 2:", oxy * co2)