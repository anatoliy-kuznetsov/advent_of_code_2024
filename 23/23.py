import itertools
from collections import defaultdict

connections = defaultdict(lambda: set())
with open("input.txt", "r") as f:
    lines = f.readlines()
for line in lines:
    computer1, computer2 = line[:2], line[3:5]
    connections[computer1].add(computer2)
    connections[computer2].add(computer1)

t_containing_set_count = 0
for computer, connected_computers in connections.items():
    for computer1, computer2 in itertools.product(connected_computers, repeat=2):
        if computer1 not in connections[computer2]:
            continue
        if any((
            computer[0] == "t",
            computer1[0] == "t",
            computer2[0] == "t",
        )):
            t_containing_set_count += 1

print(f"{t_containing_set_count // 6} 3-cliques contain a computer whose name starts with 't'")

def max_clique_containing(node: str, connected_nodes: set[str]) -> set[str]:
    max_clique = set([node])
    if len(connected_nodes) == 0:
        return max_clique
    potential_connections = {}
    for neighbor in connected_nodes:
        potential_connections[neighbor] = connected_nodes & connections[neighbor]
    for neighbor in connected_nodes:
        potential_clique = set([node]) | max_clique_containing(neighbor, potential_connections[neighbor])
        if len(potential_clique) > len(max_clique):
            max_clique = potential_clique
        for other_node in potential_clique:
            for other_neighbor in connected_nodes:
                if other_neighbor == neighbor:
                    continue
                if other_node not in potential_connections[other_neighbor]:
                    continue
                potential_connections[other_neighbor].remove(other_node)

    return max_clique

max_clique_size_found = 0
max_clique = set("")
for node, neighbors in connections.items():
    if len(neighbors) < max_clique_size_found:
        continue
    largest_clique_containing = max_clique_containing(node, neighbors)
    if len(largest_clique_containing) > max_clique_size_found:
        max_clique_size_found = len(largest_clique_containing)
        max_clique = largest_clique_containing
    for other_node, other_connections in connections.items():
        if node not in other_connections:
            continue
        other_connections.remove(node)

max_clique_sorted = [node for node in max_clique]
max_clique_sorted.sort()
password = ",".join(max_clique_sorted)
print(f"The password is {password}")