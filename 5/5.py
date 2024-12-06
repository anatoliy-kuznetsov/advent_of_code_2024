from collections import defaultdict

def parse_rules(lines: list[str]) -> dict:
    """
    Returns a dictionary of ordering rules.
    The key is the page that must come first.
    The value is a list of pages that must come after it.
    """
    rules = defaultdict(lambda: [])
    for line in lines:
        if "|" not in line:
            break
        tokens = line.split("|")
        rules[tokens[0]].append(tokens[1].strip())
    return rules

def parse_updates(lines: list[str]) -> list[str]:
    return [line for line in lines if "," in line]

def find_first_violation(pages: list[str], rules: dict) -> tuple[int, int]:
    """
    Returns indices of two pages out of order according to the rules.
    If all pages are in order, returns (-1, -1).
    """
    page_positions = {page: i for i, page in enumerate(pages)}
    for i, page in enumerate(pages):
        for later_page in rules[page]:
            if later_page not in page_positions.keys():
                continue
            if page_positions[page] > page_positions[later_page]:
                return (i, pages.index(later_page))
    return (-1, -1)

def is_correctly_ordered(update: str, rules: dict) -> bool:
    """
    Checks ordering of pages in an update
    """
    pages = update.split(",")
    pages[-1] = pages[-1].strip()
    return find_first_violation(pages, rules) == (-1, -1)

with open("input.txt", "r") as f:
    lines = f.readlines()

rules = parse_rules(lines)
updates = parse_updates(lines)
correctly_ordered_updates = [update.split(",") for update in updates if is_correctly_ordered(update, rules)]
middle_pages = [int(update[len(update) // 2]) for update in correctly_ordered_updates]
print(sum(middle_pages))

def reorder_update(update: str, rules: dict) -> list[str]:
    """
    Reorders update to follow rules, returns as list of pages
    """
    pages = update.split(",")
    pages[-1] = pages[-1].strip()
    i, j = find_first_violation(pages, rules)
    while not (i == -1 and j == -1):
        pages[i], pages[j] = pages[j], pages[i]
        i, j = find_first_violation(pages, rules)
    return pages

incorrectly_ordered_updates = [update for update in updates if not is_correctly_ordered(update, rules)]
reordered_updates = [reorder_update(update, rules) for update in incorrectly_ordered_updates]
middle_pages = [int(update[len(update) // 2]) for update in reordered_updates]
print(sum(middle_pages))
