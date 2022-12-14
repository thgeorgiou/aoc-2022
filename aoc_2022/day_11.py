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
instructions = input_raw.splitlines()


class Monkey:
    def __init__(self, description: str) -> None:
        lines = description.splitlines()
        self.id = lines[0].split()[1][:-1]
        self.items = deque([int(x) for x in lines[1].split(":")[1].split(", ")])
        self.operation = lines[2].split(":")[1]
        self.operation = self.operation.replace("new = ", "")
        self.test = int(re.findall("\d+", lines[3])[0])
        self.true_target = int(re.findall("\d+", lines[4])[0])
        self.false_target = int(re.findall("\d+", lines[5])[0])

        self.inspect_count = 0
        self.mod_base = 0
        self.divide_by_three = True

    def __repr__(self) -> str:
        return f"""Monkey {self.id}:
        Starting Items: {', '.join(str(x) for x in self.items)}
        Operation: new = {self.operation}
        Test: divisible by {self.test}
            If true: throw to monkey {self.true_target}
            If false: throw to monkey {self.false_target}
        """

    def play_round(self):
        while self.items:
            self.inspect_count += 1

            item = self.items.pop()
            item = eval(self.operation, {}, {"old": item})
            if self.divide_by_three:
                item = item // 3
            item = item % self.mod_base
            if item % self.test == 0:
                yield self.true_target, item
            else:
                yield self.false_target, item


monkeys = [Monkey(x) for x in input_raw.split("\n\n")]
mod_base = math.prod((monkey.test for monkey in monkeys))
for monkey in monkeys:
    monkey.mod_base = mod_base

# Part 1
for r in range(20):
    for monkey in monkeys:
        for target, item in monkey.play_round():
            monkeys[target].items.appendleft(item)

scores = sorted([monkey.inspect_count for monkey in monkeys], reverse=True)
monkey_busines = scores[0] * scores[1]
print(f"Part 1: {monkey_busines}")


# Part 2
monkeys = [Monkey(x) for x in input_raw.split("\n\n")]
mod_base = math.prod((monkey.test for monkey in monkeys))
for monkey in monkeys:
    monkey.mod_base = mod_base
    monkey.divide_by_three = False

for r in range(10000):
    for monkey in monkeys:
        for target, item in monkey.play_round():
            monkeys[target].items.appendleft(item)

scores = sorted([monkey.inspect_count for monkey in monkeys], reverse=True)
monkey_busines = scores[0] * scores[1]
print(f"Part 2: {monkey_busines}")
