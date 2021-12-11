import itertools
with open("day11_input.txt") as f:
    data = [list(int(n) for n in l.strip()) for l in f]

def loop_board(board):
    for j, row in enumerate(board):
        for i, value in enumerate(row):
            yield (i, j), int(value)

def apply_flash(board, i, j):
    new_flashes = set()
    width = len(board[0])
    height = len(board)
    for di, dj in itertools.product((-1, 0, 1), (-1, 0, 1)):
        new_i, new_j = i + di, j + dj
        if ((di, dj) != (0, 0)) and (0 <= new_i < width) and (0 <= new_j < height):
            board[new_j][new_i] += 1
            if board[new_j][new_i] > 9:
                new_flashes.add((new_i, new_j))
    return new_flashes

def step(board):
    remaining_flashes = set()
    flashed = set()
    for (i, j), _ in loop_board(board):
        board[j][i] += 1
        if board[j][i] > 9:
            remaining_flashes.add((i, j))

    while len(remaining_flashes) > 0:
        p = remaining_flashes.pop()
        new_flashes = apply_flash(board, *p)
        remaining_flashes |= (new_flashes - flashed)
        flashed.add(p)

    for i, j in flashed:
        board[j][i] = 0

    return len(flashed)

print("Part 1:", sum(step(data) for _ in range(100)))
steps = 100
while len(set(n for line in data for n in line)) != 1:
    step(data)
    steps += 1
print("Part 2:", steps)