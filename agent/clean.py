import json
import os
import re


def open_file():
    PATH = os.path.join(os.getcwd(), "agent", "openings.json")

    with open(PATH, "r") as f:
        openings = json.load(f)

    return openings


def group(openings):
    grouped = {}
    current_opening = ""

    for opening in openings:
        if opening["name"] != current_opening:
            current_opening = opening["name"]
            # grouped[current_opening] = []

        moves = []

        for move in opening["moves"].split(" "):
            if not move[0].isnumeric():
                moves.append(move)

        grouped[current_opening] = moves

    return grouped


if __name__ == "__main__":
    openings = open_file()
    openings = group(openings)

    for opening in openings:
        print(openings[opening])