import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()

range_sorted = lambda start, stop: range(min(start, stop), max(start, stop) + 1)

map = set()
for line in input_raw.splitlines():
    string_points = [point.split(",") for point in line.split(" -> ")]
    points = [(int(x), int(y)) for x, y in string_points]

    for p1, p2 in zip(points, points[1:]):
        if p1[0] != p2[0]:
            map |= {complex(p, p1[1]) for p in range_sorted(p1[0], p2[0])}
        else:
            map |= {complex(p1[0], p) for p in range_sorted(p1[1], p2[1])}


def draw_map():
    min_x = int(min(p.real for p in map))
    max_x = int(max(p.real for p in map))
    min_y = int(min(p.imag for p in map))
    max_y = int(max(p.imag for p in map))

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if complex(x, y) in map:
                print("#", end="")
            else:
                print(".", end="")
        print()


max_depth = max(p.imag for p in map) + 1
print(f"{max_depth=}")


rocks = len(map)
part_1 = None
while 500 not in map:
    sand = 500 + 0j
    while True:
        if sand.imag == max_depth:
            if part_1 == None:
                part_1 = len(map) - rocks
            break
        for candidate in [sand + 1j, sand - 1 + 1j, sand + 1 + 1j]:
            if candidate not in map:
                sand = candidate
                break
        else:
            break

    map.add(sand)

print(f"Part 1: {part_1}")
print(f"Part 2: {len(map) - rocks}")
