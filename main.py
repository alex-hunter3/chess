import chess
import pygame

from settings import *

# constants
# WIDTH = 800
# HEIGHT = 800
# SQUARE_SIZE = WIDTH // 8

# setup board and widow
board = chess.Board()
win = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("./imgs/black/knight.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Chess")

print(board.fen())
print(board)

images = {
    # black
    "r": pygame.image.load("./imgs/black/rook.png"),
    "n": pygame.image.load("./imgs/black/knight.png"),
    "b": pygame.image.load("./imgs/black/bishop.png"),
    "q": pygame.image.load("./imgs/black/queen.png"),
    "k": pygame.image.load("./imgs/black/king.png"),
    "p": pygame.image.load("./imgs/black/pawn.png"),

    # white
    "R": pygame.image.load("./imgs/white/rook.png"),
    "N": pygame.image.load("./imgs/white/knight.png"),
    "B": pygame.image.load("./imgs/white/bishop.png"),
    "Q": pygame.image.load("./imgs/white/queen.png"),
    "K": pygame.image.load("./imgs/white/king.png"),
    "P": pygame.image.load("./imgs/white/pawn.png"),
}

for image in images:
    images[image] = pygame.transform.scale(
        images[image],
        (SQUARE_SIZE, SQUARE_SIZE)
    )


def draw_board():
    win.fill(OAK)

    for rank in range(8):
        for square in range(rank % 2, 8, 2):
            pygame.draw.rect(
                win,
                WHITE,
                (rank * SQUARE_SIZE, square * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )


def draw_pieces():
    fen = board.fen().split()[0]
    print(fen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    draw_board()
    draw_pieces()
    pygame.display.update()   
