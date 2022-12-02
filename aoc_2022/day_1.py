import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()


## Part 1
elves = {}
for i, elf_inventory in enumerate(input_raw.split("\n\n")):
    elves[i] = 0

    for cal in elf_inventory.split("\n"):
        if cal.strip() == "":
            continue
        elves[i] += int(cal)

most_packed_elf = max(elves, key=elves.get)
print(f"Part 1: {elves[most_packed_elf]}")


## Part 2
elves = dict(sorted(elves.items(), key=lambda x: x[1], reverse=True))
elves = {k: elves[k] for k in list(elves.keys())[:3]}
print(f"Part 2: {sum(elves.values())}")
