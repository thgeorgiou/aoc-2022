import argparse
import pathlib
import re

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
parser.add_argument("part_1_row", type=int)
parser.add_argument("part_2_maxdim", type=int)
args = parser.parse_args()

input_raw = args.input.read_text()


class Sensor:
    def __init__(self, row: str) -> None:
        matches = re.findall(r"-?\d+", row)
        self.loc = complex(int(matches[0]), int(matches[1]))
        self.beacon = complex(int(matches[2]), int(matches[3]))

        r = self.loc - self.beacon
        self.rad = int(abs(r.real) + abs(r.imag))

    def __repr__(self) -> str:
        return f"{self.loc} -> {self.beacon} ({self.rad=})"


sensors = [Sensor(row) for row in input_raw.splitlines()]
for s in sensors:
    print(s)
print("---")

# Part 1
y = args.part_1_row
no_beacon = set()
for sensor in sensors:
    rad = sensor.rad
    delta = int(abs(sensor.loc.imag - y))
    if delta <= rad:
        for i in range(0, rad - delta + 1):
            no_beacon |= set(
                [complex(sensor.loc.real - i, y), complex(sensor.loc.real + i, y)]
            )
    if sensor.beacon in no_beacon:
        no_beacon.remove(sensor.beacon)
    if sensor.loc in no_beacon:
        no_beacon.remove(sensor.loc)

print(f"Part 1: {len(no_beacon)}")


# Part 2
candidate_points = set()
beacon_locations = set([sensor.beacon for sensor in sensors])
sensor_locations = set([sensor.loc for sensor in sensors])

for sensor in sensors:
    rad = sensor.rad + 1
    for i in range(0, rad + 1):
        boundaries = [
            complex(sensor.loc.real - i, sensor.loc.imag + rad - i),
            complex(sensor.loc.real + i, sensor.loc.imag + rad - i),
            complex(sensor.loc.real - i, sensor.loc.imag - rad + i),
            complex(sensor.loc.real + i, sensor.loc.imag - rad + i),
        ]
        boundaries = filter(
            lambda p: 0 <= p.real <= args.part_2_maxdim
            and 0 <= p.imag <= args.part_2_maxdim
            and p not in sensor_locations
            and p not in beacon_locations,
            boundaries,
        )

        candidate_points |= set(boundaries)

for candidate in candidate_points:
    for sensor in sensors:
        if (
            abs(candidate.real - sensor.loc.real)
            + abs(candidate.imag - sensor.loc.imag)
            <= sensor.rad
        ):
            break
    else:
        frequency = candidate.real * 4000000 + candidate.imag
        print(f"Part 2: {frequency}")
        break
