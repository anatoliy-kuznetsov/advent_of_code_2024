def parse_line(line: str) -> tuple[int, tuple[int]]:
    tokens = line.split()
    target = int(tokens[0][:-1])
    numbers = [int(t) for t in tokens[1:]]
    return target, numbers

with open("input.txt", "r") as f:
    lines = f.readlines()

def target_achievable(target: int, numbers: tuple[int]) -> bool:
    if len(numbers) == 0:
        return target == 0
    if target < 0:
        return False
    if target == 0:
        return len(numbers) == 0
    achievable_with_addition = target_achievable(target - numbers[-1], numbers[:-1])
    if target % numbers[-1] == 0:
        achievable_with_multiplication = target_achievable(int(target / numbers[-1]), numbers[:-1])
    else:
        achievable_with_multiplication = False
    target_as_str = str(target)
    if target_as_str.endswith(str(numbers[-1])):
        truncated_target = target_as_str[:-len(str(numbers[-1]))]
        if len(truncated_target) == 0:
            truncated_target = 0
        else:
            truncated_target = int(truncated_target)
        achievable_with_concatenation = target_achievable(truncated_target, numbers[:-1])
    else:
        achievable_with_concatenation = False
    return any((achievable_with_addition,
                achievable_with_multiplication,
                achievable_with_concatenation
                ))

data = [parse_line(line) for line in lines]
result = 0
for target, numbers in data:
    if target_achievable(target, numbers):
        result += target

print(result)