import copy

class Guard:
    facing_directions = "^>v<"

    def __init__(self, starting_location: tuple[int, int], starting_tile: str):
        self.in_bounds = True
        self.location = starting_location
        self.visited_locations = {starting_location}
        self.facing_direction = starting_tile
        self.facing_direction_history = {starting_location: {starting_tile}}
    
    def is_in_bounds(self) -> bool:
        return self.in_bounds
    
    def is_blocked(self, board: list[str]) -> bool:
        if self.facing_direction == "^":
            return self.location[0] > 0 and board[self.location[0] - 1][self.location[1]] == "#"
        if self.facing_direction == ">":
            return self.location[1] < len(board[0]) - 1 and board[self.location[0]][self.location[1] + 1] == "#"
        if self.facing_direction == "v":
            return self.location[0] < len(board) - 1 and board[self.location[0] + 1][self.location[1]] == "#"
        if self.facing_direction == "<":
            return self.location[1] > 0 and board[self.location[0]][self.location[1] - 1] == "#"
    
    def record_location(self):
        self.visited_locations.add(self.location)
        if self.location not in self.facing_direction_history:
            self.facing_direction_history[self.location] = set()
        self.facing_direction_history[self.location].add(self.facing_direction)

    def rotate_right(self):
        self.record_location()
        i = self.facing_directions.find(self.facing_direction)
        new_direction = self.facing_directions[(i + 1) % len(self.facing_directions)]
        self.facing_direction = new_direction
        self.record_location()

    def step(self, board: list[str]):
        self.record_location()
        if self.facing_direction == "^":
            self.location = (self.location[0] - 1, self.location[1])
        elif self.facing_direction == ">":
            self.location = (self.location[0], self.location[1] + 1)
        elif self.facing_direction == "v":
            self.location = (self.location[0] + 1, self.location[1])
        elif self.facing_direction == "<":
            self.location = (self.location[0], self.location[1] - 1)
        if any((
            self.location[0] < 0,
            self.location[0] == len(board),
            self.location[1] < 0,
            self.location[1] == len(board[0])
        )):
            self.in_bounds = False
        self.record_location()

    def advance(self, board: list[str]):
        while self.is_blocked(board):
            self.rotate_right()
        self.step(board)

    def get_location(self) -> tuple[int, int]:
        return self.location

    def get_facing_direction(self) -> str:
        return self.facing_direction

    def get_visited_locations(self) -> set[tuple[int, int]]:
        return self.visited_locations
    
    def get_facing_direction_history(self) -> dict[tuple[int, int], set]:
        return self.facing_direction_history

with open("input.txt", "r") as f:
    board = [line.strip() for line in f.readlines()]

guard_found = False
for i, line in enumerate(board):
    for j, tile in enumerate(line):
        if tile in Guard.facing_directions:
            guard_found = True
            starting_location = (i, j)
            starting_tile = tile
            guard = Guard(starting_location=(i, j), starting_tile=tile)
            break
    if guard_found:
        break

while guard.is_in_bounds():
    guard.advance(board)

print(len(guard.get_visited_locations()))

potential_obstacle_locations = set()
facing_direction_history = guard.get_facing_direction_history()
for visited_location in guard.get_visited_locations():
    if all((
        visited_location[0] > 0,
        visited_location[1] < len(board[0]) - 1,
        visited_location[0] < len(board) - 1,
        visited_location[1] > 0
    )):
        potential_obstacle_locations.add(visited_location)
    facing_directions_here = facing_direction_history[visited_location]
    if "^" in facing_directions_here and visited_location[0] > 0:
        potential_obstacle_locations.add((visited_location[0] - 1, visited_location[1]))
    if ">" in facing_directions_here and visited_location[1] < len(board[0]) - 1:
        potential_obstacle_locations.add((visited_location[0], visited_location[1] + 1))
    if "v" in facing_directions_here and visited_location[0] < len(board) - 1:
        potential_obstacle_locations.add((visited_location[0] + 1, visited_location[1]))
    if "<" in facing_directions_here and visited_location[1] > 0:
        potential_obstacle_locations.add((visited_location[0], visited_location[1] - 1))

potential_obstacle_locations.remove(starting_location)

def state_count(history: dict[tuple[int, int], set]) -> int:
    count = 0
    for location in history:
        for orientation in history[location]:
            count += 1
    return count

def obstacle_succeeds(board: list[str], starting_location: tuple[int, int], starting_tile: str, obstacle_location: tuple[int, int]) -> bool:
    if board[obstacle_location[0]][obstacle_location[1]] == "#":
        return False
    board_with_obstacle = board.copy()
    obstacle_row = list(board_with_obstacle[obstacle_location[0]])
    obstacle_row[obstacle_location[1]] = "#"
    board_with_obstacle[obstacle_location[0]] = "".join(obstacle_row)
    guard = Guard(starting_location=starting_location, starting_tile=starting_tile)
    """
    If the guard ends up in a previously visited location with the same orientation,
    he's stuck in a loop.
    """
    while guard.is_in_bounds():
        old_state_count = state_count(guard.get_facing_direction_history())
        guard.advance(board_with_obstacle)
        new_state_count = state_count(guard.get_facing_direction_history())
        if old_state_count == new_state_count:
            return True
    return False

successful_obstacle_locations = []
for obstacle_location in potential_obstacle_locations:
    if obstacle_succeeds(board, starting_location, starting_tile, obstacle_location):
        successful_obstacle_locations.append(obstacle_location)
print(len(successful_obstacle_locations))