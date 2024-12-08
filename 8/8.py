from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.readlines()
# trim newlines
lines = [line[:-1] for line in lines]

antenna_locations = defaultdict(lambda: [])
for i, line in enumerate(lines):
    for j, cell in enumerate(line):
        if cell.isalnum():
            antenna_locations[cell].append((i, j))

antinode_locations = set()
for antenna_type, sites in antenna_locations.items():
    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            first_antenna_location = sites[i]
            second_antenna_location = sites[j]
            row_difference = second_antenna_location[0] - first_antenna_location[0]
            column_difference = second_antenna_location[1] - first_antenna_location[1]
            max_left_steps = first_antenna_location[0] // row_difference + 1
            max_right_steps = (len(lines[0]) - first_antenna_location[0]) // row_difference + 1
            for k in range(-max_left_steps, max_right_steps + 1):
                antinode_locations.add((
                    first_antenna_location[0] + row_difference * k,
                    first_antenna_location[1] + column_difference * k
                ))

max_row_index = len(lines) - 1
max_column_index = len(lines[0]) - 1
print(len([location for location in antinode_locations if all((
    0 <= location[0],
    location[0] <= max_row_index,
    0 <= location[1],
    location[1] <= max_column_index
))]))