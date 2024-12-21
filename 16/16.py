import sys
from collections import defaultdict

sys.setrecursionlimit(50000)

def apart_by_90_degrees(node1: tuple[tuple[int, int], str], node2: tuple[tuple[int, int], str]) -> bool:
    if node1[0] != node2[0]:
        return False
    orientation1 = node1[1]
    orientation2 = node2[1]
    match orientation1:
        case "N" | "S":
            return orientation2 in ("E", "W")
        case "E" | "W":
            return orientation2 in ("N", "S")
        case _:
            exit(f"Invalid orientation of {orientation1} for node {node1}")

class Maze:
    turn_cost = 1000
    step_cost = 1
    MAX_DISTANCE = 18446744073709551615
    def __init__(self, maze_text: list[str]):
        self.width = len(maze_text[0]) - 1
        self.height = len(maze_text)
        self.nodes = set()
        self.adjacencies = defaultdict(lambda: {})
        self.distances_from_start = {}
        self.shortest_distance_found = self.MAX_DISTANCE
        self.preceding_nodes = defaultdict(lambda: set())
        self.cells_along_path = set()
        for i, line in enumerate(maze_text):
            for j, char in enumerate(line):
                if char in ("#", "\n"):
                    continue
                if char == "S":
                    self.start = ((i, j), "E")
                    self.nodes.add(self.start)
                    self.distances_from_start[self.start] = 0
                    self.cells_along_path.add((i, j))

                    turned_starts = [
                        ((i, j), "N"),
                        ((i, j), "S"),
                        ((i, j), "W"),
                    ]
                    for node in turned_starts:
                        self.nodes.add(node)
                        self.distances_from_start[node] = self.MAX_DISTANCE
                        self.update_adjacencies(node)
                    self.update_adjacencies(self.start)
                    continue
                if char == "E":
                    self.cells_along_path.add((i, j))
                    self.ends = [
                        ((i, j), "N"),
                        ((i, j), "E"),
                        ((i, j), "S"),
                        ((i, j), "W"),
                    ]
                    for end in self.ends:
                        self.nodes.add(end)
                        self.distances_from_start[end] = self.MAX_DISTANCE
                        self.update_adjacencies(end)
                    continue
                states = [
                    ((i, j), "N"),
                    ((i, j), "E"),
                    ((i, j), "S"),
                    ((i, j), "W"),
                ]
                for state in states:
                    self.nodes.add(state)
                    self.distances_from_start[state] = self.MAX_DISTANCE
                    self.update_adjacencies(state)

    def update_adjacencies(self, new_node: tuple[tuple[int, int], str]):
        # adjacencies with other states at the same location
        coordinates = new_node[0]
        colocated_states = [
            (coordinates, "N"),
            (coordinates, "E"),
            (coordinates, "S"),
            (coordinates, "W"),
        ]
        for state in colocated_states:
            if state == new_node:
                continue
            if state not in self.nodes:
                continue
            if apart_by_90_degrees(state, new_node):
                self.adjacencies[new_node][state] = self.turn_cost
                self.adjacencies[state][new_node] = self.turn_cost
        # adjacencies with neighboring locations
        orientation = new_node[1]
        match orientation:
            case "N":
                direction = (-1, 0)
            case "E":
                direction = (0, 1)
            case "S":
                direction = (1, 0)
            case "W":
                direction = (0, -1)
        source = (
            (coordinates[0] - direction[0], coordinates[1] - direction[1]),
            orientation
        )
        if source in self.nodes:
            self.adjacencies[source][new_node] = self.step_cost
        destination = (
            (coordinates[0] + direction[0], coordinates[1] + direction[1]),
            orientation
        )
        if destination in self.nodes:
            self.adjacencies[new_node][destination] = self.step_cost

    def update_distances_from_start(self, node: tuple[tuple[int, int], str]):
        for neighbor in self.adjacencies[node]:
            distance = self.distances_from_start[node] + self.adjacencies[node][neighbor]
            if distance > self.distances_from_start[neighbor] or distance > self.shortest_distance_found:
                continue
            elif distance == self.distances_from_start[neighbor]:
                self.preceding_nodes[neighbor].add(node)
                continue
            self.distances_from_start[neighbor] = distance
            self.preceding_nodes[neighbor].clear()
            self.preceding_nodes[neighbor].add(node)
            if neighbor in self.ends:
                self.shortest_distance_found = min(
                    self.shortest_distance_found,
                    self.distances_from_start[neighbor]
                )
            else:
                self.update_distances_from_start(neighbor)
    
    def solve(self) -> int:
        self.update_distances_from_start(self.start)
        return self.shortest_distance_found
    
    def add_cells_along_path(self, node: tuple[tuple[int, int], str]):
        if self.start in self.preceding_nodes[node]:
            return
        self.cells_along_path.add(node[0])
        for preceding_node in self.preceding_nodes[node]:
            self.add_cells_along_path(preceding_node)

    def count_cells_along_path(self) -> int:
        destination_states = set()
        for state in self.ends:
            if self.distances_from_start[state] > self.shortest_distance_found:
                continue
            destination_states.add(state)
        for state in destination_states:
            self.add_cells_along_path(state)
        return len(self.cells_along_path)
    
    def __repr__(self):
        drawing = [["" for _ in range(self.width + 1)] for _ in range(self.height)]
        result = ""
        for i in range(self.height):
            for j in range(self.width):
                if ((i, j), "E") == self.start:
                    drawing[i][j] = "S"
                elif ((i, j), "E") in self.ends:
                    drawing[i][j] = "E"
                elif (i, j) in self.cells_along_path:
                    drawing[i][j] = "O"
                elif ((i, j), "N") in self.nodes:
                    drawing[i][j] = "."
                else:
                    drawing[i][j] = "#"
            result += "".join(drawing[i]) + "\n"
        return result

with open("input.txt", "r") as f:
    lines = f.readlines()
maze = Maze(lines)
shortest_path_length = maze.solve()
print(f"Shortest path length is {shortest_path_length}")
cell_along_path_count = maze.count_cells_along_path()
print(f"There are {cell_along_path_count} cells on a shortest path")