def is_safe(report: list[int]) -> bool:
    if report[0] == report[1]:
        return False
    is_increasing = report[1] > report[0]
    for i, data in enumerate(report[:-1]):
        difference = report[i + 1] - data
        if is_increasing:
            if difference < 1 or difference > 3:
                return False
        else:
            if difference > -1 or difference < -3:
                return False
    return True

def is_safe_dampened(report: list[int]) -> bool:
    for i, data in enumerate(report):
        modified_report = report.copy()
        modified_report.pop(i)
        if is_safe(modified_report):
            return True
    return False

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
    safe_count = 0
    for line in lines:
        tokens = line.split()
        if is_safe_dampened([int(t) for t in tokens]):
            safe_count += 1
    print(safe_count)