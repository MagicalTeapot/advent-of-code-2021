from dataclasses import dataclass, field, replace
from typing import Union
from itertools import combinations
from copy import deepcopy

@dataclass
class Node:
    lhs: Union[int, "Node"]
    rhs: Union[int, "Node"]
    depth: int = 0

    def __str__(self):
        return f"[{self.lhs},{self.rhs}]"

    def __iter__(self):
        if isinstance(self.lhs, Node):
            yield from iter(self.lhs)
        if isinstance(self.lhs, int) or isinstance(self.rhs, int):
            yield self
        if isinstance(self.rhs, Node):
            yield from iter(self.rhs)

    def __add__(self, other):
        new_node = Node(deepcopy(self), deepcopy(other), depth=0) # -1 so the next loop makes it 0
        update_depths(new_node)
        reduce_node(new_node)
        return new_node

def update_depths(root: Node, depth: int = 0):
    root.depth = depth
    if isinstance(root.lhs, Node):
        update_depths(root.lhs, depth+1)
    if isinstance(root.rhs, Node):
        update_depths(root.rhs, depth+1)

def from_string(string, depth = 0):
    if string.isdigit():
        return int(string)

    d = 0
    lhs, curr = "", ""
    for char in string[1:-1]:
        if char == "[":
            d += 1
        elif char == "]":
            d -= 1
        elif char == "," and d == 0: # string up until now has been the lhs
            lhs = curr
            curr = ""
            continue
        curr += char
    return Node(from_string(lhs, depth + 1), from_string(curr, depth + 1), depth)

def replace_node(root: Node, node: Node, val: int):
    if isinstance(root.lhs, Node):
        if root.lhs is node:
            root.lhs = val
            return True
        if replace_node(root.lhs, node, val):
            return True
    if isinstance(root.rhs, Node):
        if root.rhs is node:
            root.rhs = val
            return True
        if replace_node(root.rhs, node, val):
            return True
    return False

def explode(root: Node):
    value_nodes = list(iter(root))
    if all(n.depth < 4 for n in value_nodes): # No exploding
        return False

    for index, node in enumerate(value_nodes):
        if node.depth >= 4 and isinstance(node.lhs, int) and isinstance(node.rhs, int):
            break

    if isinstance(node.lhs, int):
        ptr = index - 1
        val = node.lhs
        node.lhs = 0
        while ptr >= 0:
            side_node = value_nodes[ptr]
            if isinstance(side_node.rhs, int):
                side_node.rhs += val
                break
            elif isinstance(side_node.lhs, int):
                side_node.lhs += val
                break
            ptr -= 1

    if isinstance(node.rhs, int):
        ptr = index + 1
        val = node.rhs
        node.rhs = 0
        while ptr < len(value_nodes):
            side_node = value_nodes[ptr]
            if isinstance(side_node.lhs, int):
                side_node.lhs += val
                break
            elif isinstance(side_node.rhs, int):
                side_node.rhs += val
                break
            ptr += 1

    replace_node(root, node, 0)
    return True

def split(root: Node):
    for node in root:
        if isinstance(node.lhs, int) and node.lhs >= 10:
            val = node.lhs
            node.lhs = Node(val//2, val-val//2, node.depth+1)
            return True
        if isinstance(node.rhs, int) and node.rhs >= 10:
            val = node.rhs
            node.rhs = Node(val//2, val-val//2, node.depth+1)
            return True
    return False

def reduce_node(node: Node):
    while explode(node) or split(node):
        pass

def magnitude(node: Node | int):
    if isinstance(node, int):
        return node
    return 3 * magnitude(node.lhs) + 2 * magnitude(node.rhs)

def get_numbers():
    with open("day18_input.txt") as f:
        return [from_string(l.strip()) for l in f]

total, *rest = get_numbers()
for num in rest:
    total += num
print("Part 1:", magnitude(total))

numbers = get_numbers()
print("Part 2:", max(max(magnitude(a + b), magnitude(b + a)) for a, b in combinations(numbers, 2)))