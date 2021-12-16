import pygame
import chess

# each index is the corresponding square in chess library
# Example: positions index 0 = chess.A1
positions = []
alphabet = "abcdefgh"

for i in range(1, 9):
    for letter in alphabet:
        positions.append(f"{letter}{i}")

for square in positions:
    pass


class Player:
    def __init__(self, colour):
        if colour != "w" and colour != "b":
            raise ValueError("colour argument must either be w or b")

        self.colour = colour

    def get_move(self, board):
        pressed = pygame.mouse.get_pressed()

        if pressed[0]:
            (x, y) = pygame.mouse.get_pos()
            

        return None