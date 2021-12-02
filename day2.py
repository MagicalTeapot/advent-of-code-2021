def read_lines():
    with open("day2_input.txt") as f:
        for line in f:
            x, y = line.split()
            yield x, int(y)

pos = 0
p1_depth = 0
p2_depth = 0
p2_aim = 0

for directive, value in read_lines():
    match directive:
        case "forward":
            pos += value
            p2_depth += value * p2_aim
        case "up":
            p1_depth -= value
            p2_aim -= value
        case "down":
            p1_depth += value
            p2_aim += value

print(pos * p1_depth) # Part 1
print(pos * p2_depth) # Part 2