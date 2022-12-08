import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()

# Part 1
for i in range(4, len(input_raw)):
    marker = input_raw[i - 4 : i]
    if len(set(marker)) == 4:
        print(f"Part 1: {i} w/ marker {marker}")
        break

# Part 2
for i in range(14, len(input_raw)):
    marker = input_raw[i - 14 : i]
    if len(set(marker)) == 14:
        print(f"Part 11: {i} w/ marker {marker}")
        break
