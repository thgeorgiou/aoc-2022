import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()


def string_range_to_set(r: str) -> set:
    start, end = r.split("-")
    return set(range(int(start), int(end) + 1))


fully_overlapping_ranges = 0
partially_overlapping_ranges = 0
for line in input_raw.splitlines():
    assignments = [string_range_to_set(x) for x in line.split(",")]
    if assignments[0].issubset(assignments[1]) or assignments[1].issubset(
        assignments[0]
    ):
        fully_overlapping_ranges += 1
    if assignments[0] & assignments[1]:
        partially_overlapping_ranges += 1

print(f"Part 1: {fully_overlapping_ranges}")
print(f"Part 2: {partially_overlapping_ranges}")
