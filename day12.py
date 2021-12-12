from collections import defaultdict
graph = defaultdict(set)
with open("day12_input.txt") as f:
    for line in f:
        lhs, rhs = line.strip().split("-")
        graph[lhs].add(rhs)
        graph[rhs].add(lhs)

def process_node(visited, current, second_visit_used):
    completed = 0
    if current.islower():
        visited[current] += 1

    for child in graph[current]:
        if child == "start":
            continue
        if child == "end":
            completed += 1
        elif child.islower():
            if visited[child] == 1 and not second_visit_used:
                completed += process_node(visited, child, True)
            elif visited[child] == 0:
                completed += process_node(visited, child, second_visit_used)
        else:
            completed += process_node(visited, child, second_visit_used)

    if current.islower():
        visited[current] -= 1
    return completed

print("Part 1:", process_node(defaultdict(int), "start", True))
print("Part 2:", process_node(defaultdict(int), "start", False))