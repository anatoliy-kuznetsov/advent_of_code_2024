with open("input.txt", "r") as f:
    lines = f.readlines()

locks = []
keys = []
for i, line in enumerate(lines):
    if i % 8 == 0:
        is_lock = "#" in line
        heights = [0] * 5
        heights_set = [False] * 5
        continue
    if line.isspace() or i == len(lines) - 1:
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)
        continue
    for j, char in enumerate(line[:5]):
        if heights_set[j] or char == ".":
            continue
        if is_lock: 
            heights[j] += 1
        else: # top of key
            heights[j] = 6 - (i % 8)
            heights_set[j] = True

def fit(lock: list[int], key: list[int]) -> bool:
    HEIGHT = 5
    for i in range(len(lock)):
        if lock[i] + key[i] > HEIGHT:
            return False
    return True

# fit_pairs = [(lock, key) for lock in locks for key in keys if fit(lock, key)]
fit_pairs = []
for lock in locks:
    for key in keys:
        if fit(lock, key):
            fit_pairs.append((lock, key))
print(f"{len(fit_pairs)} lock/key pairs fit without overlapping.")