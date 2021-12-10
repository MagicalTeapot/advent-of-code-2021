def parse_input():
    with open("day08_input.txt") as f:
        for line in f:
            data = line.strip()
            signal, output = data.split(" | ")
            yield [frozenset(x) for x in signal.split()], [frozenset(x) for x in output.split()]

def solve_line(signal, output):
    n = {}
    n[1] = [s for s in signal if len(s) == 2][0]
    n[4] = [s for s in signal if len(s) == 4][0]
    n[7] = [s for s in signal if len(s) == 3][0]
    n[8] = [s for s in signal if len(s) == 7][0]
    signal = [s for s in signal if s not in n.values()] # Remove 1, 4, 7, 8

    zero_two_six = {s for s in signal if (n[8] - n[4] - n[7]) <= s}
    two_three_five = frozenset({s for s in signal if len(s) == 5})
    zero_six_nine = frozenset({s for s in signal if len(s) == 6})

    [n[9]] = list(zero_six_nine - zero_two_six)
    [n[2]] = list(zero_two_six - zero_six_nine)

    three_five = two_three_five - {n[2]}
    n[5] = [x for x in three_five if (n[8] - n[2]) <= x][0]
    [n[3]] = list(three_five - {n[5]})

    zero_six = zero_six_nine - {n[9]}
    n[0] = [x for x in zero_six  if (n[8] - n[5]) <= x][0]
    [n[6]] = list(zero_six - {n[0]})

    lookup = {v: k for k, v in n.items()}
    return sum(10 ** power * lookup[num] for power, num in enumerate(reversed(output)))

print("Part 1:", sum(1 for _, x in parse_input() for y in x if len(y) in {2, 3, 4, 7}))
print("Part 2:", sum(solve_line(s, o) for s, o in parse_input()))