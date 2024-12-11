def expand_front(topo_map: list[str], front: list[tuple[int, int]]) -> list[tuple[int, int]]:
    front_value = int(topo_map[front[0][0]][front[0][1]])
    row_length = len(topo_map[0])
    col_length = len(topo_map)
    new_front = []
    for (i, j) in front:
        if i > 0:
            value = int(topo_map[i - 1][j])
            if value == front_value + 1:
                new_front.append((i - 1, j))
        if i < col_length - 1:
            value = int(topo_map[i + 1][j])
            if value == front_value + 1:
                new_front.append((i + 1, j))
        if j > 0:
            value = int(topo_map[i][j - 1])
            if value == front_value + 1:
                new_front.append((i, j - 1))
        if j < row_length - 1:
            value = int(topo_map[i][j + 1])
            if value == front_value + 1:
                new_front.append((i, j + 1))
    return list(set(new_front))

def find_reachable_peaks(topo_map: list[str], trailhead_indices: tuple[int, int]) -> list[tuple[int, int]]:
    front = [trailhead_indices]
    for _ in range(9):
        front = expand_front(topo_map, front)
    return front

def compute_score(topo_map: list[str], trailhead_indices: tuple[int, int]) -> int:
    return len(find_reachable_peaks(topo_map, trailhead_indices))

def score_trailheads(topo_map: list[str]) -> int:
    total_score = 0
    for i, line in enumerate(topo_map):
        for j, spot in enumerate(line):
            if spot != "0":
                continue
            total_score += compute_score(topo_map, (i, j))
    return total_score

with open("input.txt", "r") as f:
    lines = f.readlines()

topo_map = [line[:-1] for line in lines]
print(f"score: {score_trailheads(topo_map)}")

def expand_front_with_history(topo_map: list[str], front: list[list[tuple[int, int]]]) -> list[list[tuple[int, int]]]:
    front_value = int(topo_map[front[0][-1][0]][front[0][-1][1]])
    row_length = len(topo_map[0])
    col_length = len(topo_map)
    new_front = []
    for path in front:
        i = path[-1][0]
        j = path[-1][1]
        if i > 0:
            value = int(topo_map[i - 1][j])
            if value == front_value + 1:
                new_path = path.copy()
                new_path.append((i - 1, j))
                new_front.append(new_path)
        if i < col_length - 1:
            value = int(topo_map[i + 1][j])
            if value == front_value + 1:
                new_path = path.copy()
                new_path.append((i + 1, j))
                new_front.append(new_path)
        if j > 0:
            value = int(topo_map[i][j - 1])
            if value == front_value + 1:
                new_path = path.copy()
                new_path.append((i, j - 1))
                new_front.append(new_path)
        if j < row_length - 1:
            value = int(topo_map[i][j + 1])
            if value == front_value + 1:
                new_path = path.copy()
                new_path.append((i, j + 1))
                new_front.append(new_path)
    return new_front

def compute_rating(topo_map: list[str], trailhead_indices: tuple[int, int]) -> int:
    front = [[trailhead_indices]]
    for _ in range(9):
        front = expand_front_with_history(topo_map, front)
    return len(front)

def rate_trailheads(topo_map: list[str]) -> int:
    total_rating = 0
    for i, line in enumerate(topo_map):
        for j, spot in enumerate(line):
            if spot != "0":
                continue
            total_rating += compute_rating(topo_map, (i, j))
    return total_rating

print(f"rating: {rate_trailheads(topo_map)}")