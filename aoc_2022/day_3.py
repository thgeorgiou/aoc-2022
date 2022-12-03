import argparse
import pathlib
import string

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()

letter_priorities = {
    letter: priority + 1 for priority, letter in enumerate(string.ascii_letters)
}

## Part 1
inventories = []
for contents in input_raw.split("\n"):
    items = len(contents)
    first, second = contents[: items // 2], contents[items // 2 :]
    inventories.append((first, second))

total_priority = 0
for inv in inventories:
    first, second = set(inv[0]), set(inv[1])
    overlap = (first & second).pop()
    total_priority += letter_priorities[overlap]

print(f"Part 1: {total_priority}")

## Part 2
def groups():
    for i in range(0, len(inventories), 3):
        yield inventories[i : i + 3]


total_priority = 0
for elves in groups():
    inv = [set(a + b) for a, b in elves]
    common_item = (inv[0] & inv[1] & inv[2]).pop()
    total_priority += letter_priorities[common_item]

print(f"Part 2: {total_priority}")
