import argparse
import pathlib
import json
import enum
import math
from functools import cmp_to_key

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()
packet_pairs = input_raw.split("\n\n")

packet_pairs = [
    (json.loads(p1), json.loads(p2)) for p1, p2 in [p.split("\n") for p in packet_pairs]
]


class Result(enum.IntEnum):
    CORRECT_ORDER = -1
    INCONCLUSIVE = 0
    WRONG_ORDER = 1


def compare(left, right) -> Result:
    match left, right:
        case int(), int():
            if left == right:
                return Result.INCONCLUSIVE
            return Result.CORRECT_ORDER if left < right else Result.WRONG_ORDER
        case list(), list():
            for res in map(compare, left, right):
                if res != Result.INCONCLUSIVE:
                    return res
            if len(left) == len(right):
                return Result.INCONCLUSIVE
            return (
                Result.CORRECT_ORDER if len(left) < len(right) else Result.WRONG_ORDER
            )
        case list(), int():
            return compare(left, [right])
        case int(), list():
            return compare([left], right)


## Part 1

correct_order = 0
for i, (p1, p2) in enumerate(packet_pairs):
    print("Checking packet pair:", p1, p2)
    res = compare(p1, p2)
    print(f"{i + 1} result: {res}")
    if res == Result.CORRECT_ORDER:
        correct_order += i + 1

print(f"Part 1: {correct_order}")


## Part 2
all_packets = [[[2]], [[6]]]
for line in input_raw.splitlines():
    if len(line.strip()) == 0:
        continue
    all_packets.append(json.loads(line))


sorted_packets = sorted(all_packets, key=cmp_to_key(compare))
divider_indices = list(
    i for i, p in enumerate(sorted_packets, 1) if p == [[2]] or p == [[6]]
)
decoder_key = math.prod(divider_indices)
print(f"Part 2: {decoder_key}")
print(f"{divider_indices=}")
