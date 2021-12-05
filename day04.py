from collections import defaultdict
def solve_board(board, balls):
    lines = defaultdict(int)
    for ball_count, ball in enumerate(balls):
        if ball in board:
            i, j = board.pop(ball)
            lines[f"r{i}"] += 1
            lines[f"c{j}"] += 1
            if lines[f"r{i}"] == 5 or lines[f"c{j}"] == 5:
                return (ball_count, ball * sum(board.keys()))

with open("day04_input.txt") as f:
    balls = [int(x) for x in next(f).split(",")]
    results = []
    for _ in f:
        board = {}
        for i in range(5):
            for j, val in enumerate(next(f).split()):
                board[int(val)] = (i, j)
        results.append(solve_board(board, balls))

print("Part 1:", min(results, key=lambda x: x[0])[1])
print("Part 2:", max(results, key=lambda x: x[0])[1])