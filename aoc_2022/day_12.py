import argparse
import pathlib
import numpy as np
import math
from collections import deque
import re

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()
lines = input_raw.splitlines()

map = np.empty((len(lines), len(lines[0])), dtype=int)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "S":
            start = (y, x)
            char = "a"
        elif char == "E":
            end = (y, x)
            char = "z"
        map[y, x] = ord(char)


def check_bounds(y, x) -> bool:
    return 0 <= y < map.shape[0] and 0 <= x < map.shape[1]


def print_map():
    for y in range(map.shape[1]):
        for x in range(map.shape[0]):
            print(chr(map[x, y]), end="")
        print()


def solve_for_start(start, end):
    distance = np.full(map.shape, np.inf)
    distance[start] = 0
    queue = deque([start])
    while queue:
        y, x = queue.popleft()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if not check_bounds(y + dy, x + dx):
                continue

            if map[y + dy, x + dx] > map[y, x] + 1:
                continue

            if distance[y + dy, x + dx] > distance[y, x] + 1:
                distance[y + dy, x + dx] = distance[y, x] + 1
                queue.append((y + dy, x + dx))

    return distance[end]


# Part 1
d = solve_for_start(start, end)
print(f"Part 1: {d}")


# Part 2 CHECK ALL POSSIBILITIES GO
starting_points = np.where(map == ord("a"))
distances = {}
for start in zip(*starting_points):
    distances[start] = solve_for_start(start, end)

print(f"Part 2: {min(distances.values())}")
