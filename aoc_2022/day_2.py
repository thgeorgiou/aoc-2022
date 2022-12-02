import argparse
import pathlib
from enum import IntEnum

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()


class Play(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def match_points(opponent: Play, you: Play) -> int:
    if opponent == you:
        return 3
    if opponent == Play.ROCK:
        return 0 if you == Play.SCISSORS else 6
    if opponent == Play.PAPER:
        return 0 if you == Play.ROCK else 6
    if opponent == Play.SCISSORS:
        return 0 if you == Play.PAPER else 6


## Part 1
def letter_to_play(letter: str) -> Play:
    match letter:
        case "A" | "X":
            return Play.ROCK
        case "B" | "Y":
            return Play.PAPER
        case "C" | "Z":
            return Play.SCISSORS


matches = []
for match in input_raw.split("\n"):
    if match.strip() == "":
        continue
    matches.append([letter_to_play(x) for x in match.split(" ")])

points = 0
for match in matches:
    points += match_points(*match) + int(match[1])


print(f"Part 1: {points}")

## Part 2
def get_winning(play: Play) -> Play:
    match play:
        case Play.ROCK:
            return Play.PAPER
        case Play.PAPER:
            return Play.SCISSORS
        case Play.SCISSORS:
            return Play.ROCK


def get_losing(play: Play) -> Play:
    match play:
        case Play.ROCK:
            return Play.SCISSORS
        case Play.PAPER:
            return Play.ROCK
        case Play.SCISSORS:
            return Play.PAPER


matches = []
for match in input_raw.split("\n"):
    if match.strip() == "":
        continue
    opponent, outcome = match.split(" ")
    matches.append([letter_to_play(opponent), outcome])

points = 0
for match in matches:
    match match[1]:
        case "X":
            play = get_losing(match[0])
            points += match_points(match[0], play) + int(play)
        case "Y":
            play = match[0]
            points += match_points(match[0], play) + int(play)
        case "Z":
            play = get_winning(match[0])
            points += match_points(match[0], play) + int(play)

print(f"Part 2: {points}")
