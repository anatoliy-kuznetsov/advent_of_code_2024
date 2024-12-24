from collections import defaultdict

impossible_fragments = set()
def is_possible(design: str, patterns: set[str]) -> bool:
    if design in patterns:
        return True
    if len(design) < min(len(pattern) for pattern in patterns):
        impossible_fragments.add(design)
        return False
    for pattern in patterns:
        if design[:len(pattern)] != pattern:
            continue
        if is_possible(design[len(pattern):], patterns):
            return True
    impossible_fragments.add(design)
    return False

ways_to_make = defaultdict(lambda: 0)
def count_ways_to_make(original_design: str, design: str, patterns: set[str], min_pattern_length: int):
    if design in ways_to_make.keys():
        ways_to_make[original_design] += ways_to_make[design]
        return
    if design in patterns:
        ways_to_make[original_design] += 1
    if len(design) == 0:
        return
    if len(design) < min_pattern_length:
        impossible_fragments.add(design)
        return
    if design in impossible_fragments:
        return
    for pattern in patterns:
        if design[:len(pattern)] != pattern:
            continue
        old_ways_to_make = ways_to_make[original_design]
        count_ways_to_make(original_design, design[len(pattern):], patterns, min_pattern_length)
        new_ways_to_make = ways_to_make[original_design] - old_ways_to_make
        ways_to_make[design[len(pattern):]] = new_ways_to_make

with open("input.txt", "r") as f:
    lines = f.readlines()

patterns = set([token.strip() for token in lines[0].split(",")])
min_pattern_length = min(len(pattern) for pattern in patterns)
designs = [line[:-1] for line in lines[2:]]
possible_designs = [design for design in designs if is_possible(design, patterns)]
print(f"{len(possible_designs)} designs are possible")
for i, design in enumerate(designs):
    count_ways_to_make(design, design, patterns, min_pattern_length)
print(f"The sum of ways to make each possible design is {sum(ways_to_make[design] for design in designs)}")