import json
import os


class Openings:
    def __init__(self, colour):
        if colour != "w" and colour != "b":
            raise ValueError("colour argument must either be w or b")

        self.colour = colour
        self.openings = []

        self.init_openings()

        for i in range(10):
            print(self.openings[i])

    def init_openings(self):
        PATH = os.path.join(os.getcwd(), "agent", "openings.json")
        
        with open(PATH, "r") as f:
            self.openings = json.load(f)


if __name__ == "__main__":
    openings = Openings("w")