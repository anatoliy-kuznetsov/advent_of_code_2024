with open("input.txt", "r") as f:
    lines = f.readlines()
lists = [[], []]
for line in lines:
    tokens = line.split()
    lists[0].append(int(tokens[0]))
    lists[1].append(int(tokens[1]))
lists[0].sort()
lists[1].sort()
print(sum(abs(lists[1][i] - lists[0][i]) for i in range(len(lists[0]))))

second_counts = {}
for number in lists[1]:
    if number not in second_counts.keys():
        second_counts[number] = 1
    else:
        second_counts[number] += 1

similarity_score = 0
for number in lists[0]:
    if number not in second_counts.keys():
        continue
    similarity_score += number * second_counts[number]
print(similarity_score)