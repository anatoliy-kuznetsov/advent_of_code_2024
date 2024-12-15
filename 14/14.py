with open("input.txt", "r") as f:
    lines = f.readlines()

robots = []
for line in lines:
    tokens = line.split()
    position = tokens[0][2:]
    x0, y0 = position.split(",")
    velocity = tokens[1][2:]
    vx0, vy0 = velocity.split(",")
    robots.append({
        "p": (int(x0), int(y0)),
        "v": (int(vx0), int(vy0))
    })

BOARD_WIDTH = 101
BOARD_HEIGHT = 103

def evolve(robots: list[dict], seconds: int) -> list[dict]:
    new_robots = []
    for robot in robots:
        new_x = (robot["p"][0] + seconds * robot["v"][0]) % BOARD_WIDTH
        new_y = (robot["p"][1] + seconds * robot["v"][1]) % BOARD_HEIGHT
        new_robots.append({
            "p": (new_x, new_y),
            "v": (robot["v"][0], robot["v"][1])
        })
    return new_robots

def safety_factor(robots: list[dict]) -> int:
    middle_row = BOARD_HEIGHT // 2
    middle_column = BOARD_WIDTH // 2
    top_left_count = 0
    top_right_count = 0
    bottom_left_count = 0
    bottom_right_count = 0
    for robot in robots:
        x, y = robot["p"]
        if x == middle_column or y == middle_row:
            continue
        if x < middle_column and y < middle_row:
            top_left_count += 1
        elif x < middle_column and y > middle_row:
            top_right_count += 1
        elif x > middle_column and y < middle_row:
            bottom_left_count += 1
        elif x > middle_column and y > middle_row:
            bottom_right_count += 1

    return top_left_count * top_right_count * bottom_left_count * bottom_right_count

print(safety_factor(evolve(robots, 100)))

safety_factors = []
min_safety_factor = 9999999999999999
min_index = -1
for i in range(1, 100000):
    robots = evolve(robots, 1)
    factor = safety_factor(robots)
    safety_factors.append(factor)
    if factor < min_safety_factor:
        min_safety_factor = factor
        min_index = i
print(min_index)
