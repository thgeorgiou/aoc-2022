import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()
rows = input_raw.splitlines()


def sign(n: int):
    if n == 0:
        return 0
    elif n > 0:
        return 1
    else:
        return -1


def follow(head: complex, tail: complex):
    if abs(head - tail) <= abs(1 + 1j):
        return 0
    elif head.real == tail.real:
        return sign(head.imag - tail.imag) * 1j
    elif head.imag == tail.imag:
        return sign(head.real - tail.real)
    else:
        return sign(head.real - tail.real) + sign(head.imag - tail.imag) * 1j


rope = [0 + 0j] * 10
moves = {"R": 1, "L": -1, "U": 1j, "D": -1j}
visited = [set([rope[i]]) for i in range(10)]


for row in rows:
    direction, steps = row[0], int(row[1:])
    for _ in range(steps):
        rope[0] += moves[direction]
        for i in range(1, 10):
            rope[i] += follow(rope[i - 1], rope[i])
            visited[i].add(rope[i])

print(f"Part 1: {len(visited[1])}")
print(f"Part 2: {len(visited[9])}")
