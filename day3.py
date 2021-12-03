from collections import Counter

def parse_input():
    with open("day3_input.txt") as f:
        for line in f:
            yield line.strip()

def bit_counts(values):
    bins = [Counter() for _ in range(12)]
    for value in values:
        for idx, bit in enumerate(value):
            bins[idx][bit] += 1
    return bins

# Part 1
gamma_bits = [b.most_common()[0][0] for b in bit_counts(parse_input())]
gamma_val = int("".join(gamma_bits), base=2)
epslion_val = int("111111111111", base=2) - gamma_val
print(gamma_val * epslion_val)

# Part 2
def filter_by_criteria(values, bit_criteria):
    for bit in range(12):
        counts = bit_counts(values)[bit]
        values = [v for v in values if v[bit] == bit_criteria(counts)]
        if len(values) == 1:
            break
    return int(values[0], base=2)

oxy_bit_criteria = lambda counts: "1" if counts["1"] >= counts["0"] else "0"
co2_bit_criteria = lambda counts: "0" if counts["0"] <= counts["1"] else "1"

oxy = filter_by_criteria(list(parse_input()), oxy_bit_criteria)
co2 = filter_by_criteria(list(parse_input()), co2_bit_criteria)
print(oxy * co2)
