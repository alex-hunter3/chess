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

pygame.display.set_icon(pygame.image.load("./imgs/black/knight.png"))
pygame.display.set_caption("Chess")

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

material = {
    "r": -5, "n": -3, "b": -3, "q": -9, "k": 0, "p": -1,
    "R": 5, "N": 3, "B": 3, "Q": 9, "K": 0, "P": 1,
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
    fen = board.fen().split()[0].split("/")
    
    for rank, rank_pieces in enumerate(fen):
        file = 0

        for square in rank_pieces:
            if square.isnumeric():
                file += int(square)
            else:
                win.blit(
                    images[square],
                    (file * SQUARE_SIZE, rank * SQUARE_SIZE)
                )
                file += 1


def get_material():
    total_material = 0
    fen = board.fen().split()[0].split("/")
    
    for rank_pieces in fen:
        for square in rank_pieces:
            if not square.isnumeric():
                total_material += material[square]

    return total_material


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    draw_board()
    draw_pieces()
    pygame.display.update()   
