from collections import Counter
with open("day06_input.txt") as f:
    state = [0] * 9
    for n in [int(n) for n in f.read().split(",")]:
        state[n] += 1

def next_state(state):
    new_state = state[1:] + state[:1]
    new_state[6] += new_state[-1]
    return new_state

for _ in range(80):
    state = next_state(state)
print("Part 1:", sum(state))

for _ in range(256 - 80):
    state = next_state(state)
print("Part 2:", sum(state))