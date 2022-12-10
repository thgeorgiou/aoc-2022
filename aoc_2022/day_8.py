import argparse
import pathlib
import numpy as np
from itertools import product

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()
rows = input_raw.splitlines()

# Create map
height, width = len(rows), len(rows[0])

map = np.empty((height, width), dtype=np.int8)
for x, row in enumerate(rows):
    for y, char in enumerate(row):
        map[x, y] = int(char)

# Part 1
visible_count = 0
for x, y in product(range(height), range(width)):
    tree_height = map[x, y]

    if x == 0 or y == 0 or x == height - 1 or y == width - 1:
        visible_count += 1
    elif (
        (map[:x, y] < tree_height).all()
        or (map[x + 1 :, y] < tree_height).all()
        or (map[x, :y] < tree_height).all()
        or (map[x, y + 1 :] < tree_height).all()
    ):
        visible_count += 1

print(f"Part 1: {visible_count}")

# Part 2
best_scenic_score = 0
for x, y in np.ndindex(map.shape):
    tree_height = map[x, y]

    if x == 0 or y == 0 or x == height - 1 or y == width - 1:
        continue

    # Find distance in all directions
    distances = []
    for v in [
        map[x, y + 1 :],
        map[x, :y][::-1],
        map[:x, y][::-1],
        map[x + 1 :, y],
    ]:
        distances.append(
            next((i + 1 for i, h in enumerate(v) if h >= tree_height), len(v))
        )

    scenic_score = np.prod(distances)
    best_scenic_score = max(best_scenic_score, scenic_score)

print(f"Part 2: {best_scenic_score}")
