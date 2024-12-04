match_sequences = ["XMAS", "SAMX"]
match_count = 0
with open("input.txt", "r") as f:
    lines = f.readlines()

# horizontal
for line in lines:
    for i in range(len(line) - 4):
        if line[i:i + 4] in match_sequences:
            match_count += 1

# vertical
for j in range(len(lines[0])):
    for i in range(len(lines) - 3):
        sequence = "".join([lines[i][j], lines[i + 1][j], lines[i + 2][j], lines[i + 3][j]])
        if sequence in match_sequences:
            match_count += 1

# diagonal NW <=> SE
for j in range(len(lines[0]) - 3):
    for i in range(len(lines) - 3):
        sequence = "".join([lines[i][j], lines[i + 1][j + 1], lines[i + 2][j + 2], lines[i + 3][j + 3]])
        if sequence in match_sequences:
            match_count += 1

# diagonal NE <=> SW
for j in range(3, len(lines[0])):
    for i in range(len(lines) - 3):
        sequence = "".join([lines[i][j], lines[i + 1][j - 1], lines[i + 2][j - 2], lines[i + 3][j - 3]])
        if sequence in match_sequences:
            match_count += 1

print(match_count)

# part two
xmas_count = 0
for j in range(1, len(lines[0]) - 1):
    for i in range(1, len(lines) - 1):
        if lines[i][j] != "A":
            continue
        # does the diagonal NW <=> SE match?
        if not ((lines[i - 1][j - 1] == "M" and lines[i + 1][j + 1] == "S") or (lines[i - 1][j - 1] == "S" and lines[i + 1][j + 1] == "M")):
            continue
        # does the diagonal NE <=> SW match?
        if not ((lines[i - 1][j + 1] == "M" and lines[i + 1][j - 1] == "S") or (lines[i - 1][j + 1] == "S" and lines[i + 1][j - 1] == "M")):
            continue
        xmas_count += 1
print(xmas_count)