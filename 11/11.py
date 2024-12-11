from collections import defaultdict

def trim_leading_zeros(stone: str) -> str:
    """
    Removes leading zeros. For a string of all zeros,
    returns '0'.
    """
    first_nonzero_index = 0
    while stone[first_nonzero_index] == "0":
        first_nonzero_index += 1
        if first_nonzero_index == len(stone):
            first_nonzero_index -= 1
            break
    return stone[first_nonzero_index:]

def evolve_stones(stones: dict) -> dict:
    new_stones = defaultdict(lambda: 0)
    for stone, count in stones.items():
        if stone == "0":
            new_stones["1"] += count
        elif len(stone) % 2 == 0:
            split_index = len(stone) // 2
            left_half = stone[:split_index]
            right_half = stone[split_index:]
            new_stones[left_half] += count
            trimmed_right_half = trim_leading_zeros(right_half)
            new_stones[trimmed_right_half] += count
        else:
            new_stone = str(2024 * int(stone))
            new_stones[new_stone] += count
    return new_stones

with open("input.txt", "r") as f:
    stones = f.readlines()[0].split()
# format: stones[stone] = count
stones = {stone: 1 for stone in stones}
for _ in range(25):
    stones = evolve_stones(stones)
print(f"After 25 blinks, there are {sum(stones.values())} stones")

for _ in range(50):
    stones = evolve_stones(stones)
print(f"After 75 blinks, there are {sum(stones.values())} stones")