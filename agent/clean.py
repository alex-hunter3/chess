import json
import os

PATH = os.path.join(os.getcwd(), "agent", "openings.json")

with open(PATH, "r") as f:
    openings = json.load(f)

