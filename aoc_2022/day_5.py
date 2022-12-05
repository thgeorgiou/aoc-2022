import argparse
import pathlib
from collections import deque
from typing import NamedTuple
import re

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()

# Find where state ends and instructions start
state_txt, instructions_txt = [x.split("\n") for x in input_raw.split("\n\n")]

# Create current state
def parse():
    num_of_stacks = int(state_txt[-1][-1])
    stacks = [deque() for _ in range(num_of_stacks)]

    for line in state_txt[-2::-1]:
        for stack_idx, i in enumerate(range(1, len(line) - 1, 4)):
            x = line[i]
            if x != " ":
                stacks[stack_idx].append(x)

    # Parse instructions
    class Instruction(NamedTuple):
        count: int
        source: int
        dest: int

    instructions = []
    for line in instructions_txt:
        count, source, dest = re.findall(r"\d+", line)
        instructions.append(Instruction(int(count), int(source) - 1, int(dest) - 1))

    return stacks, instructions


## Part 1
# Execute instructions
stacks, instructions = parse()
for instruction in instructions:
    for _ in range(instruction.count):
        stacks[instruction.dest].append(stacks[instruction.source].pop())

part_1 = []
for stack in stacks:
    part_1.append(stack[-1])
print("Part 1:", "".join(part_1))

## Part 2
stacks, instructions = parse()
for instruction in instructions:
    to_transfer = [stacks[instruction.source].pop() for _ in range(instruction.count)]
    to_transfer.reverse()
    for crate in to_transfer:
        stacks[instruction.dest].append(crate)

part_2 = []
for stack in stacks:
    part_2.append(stack[-1])
print("Part 2:", "".join(part_2))
