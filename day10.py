import statistics
with open("day10_input.txt") as f:
    data = [l.strip() for l in f.readlines()]

c2o = dict([")(", "][", "}{", "><"]) # closed -> open
o2c = {v: k for k, v in c2o.items()} # open -> closed
points_part_1 = {")": 3, "]": 57, "}": 1197, ">": 25137}
points_part_2 = {")": 1, "]": 2, "}": 3, ">": 4}

def parse_line(line):
    stack = []
    for bracket in line:
        if bracket in o2c:
            stack.append(bracket)
        elif stack[-1] == c2o[bracket]:
            stack.pop()
        else:
            return bracket, stack
    return None, stack

def loop_lines():
    for line in data:
        yield parse_line(line)
        
print("Part 1:", sum(points_part_1[b] for b, _ in loop_lines() if b))

def line_score(brackets):
    score = 0
    for b in reversed(brackets):
        score = 5 * score + points_part_2[o2c[b]]
    return score

line_stacks = (s for b, s in loop_lines() if not b)
line_scores = (line_score(s) for s in line_stacks)
print("Part 2:", statistics.median(line_scores))