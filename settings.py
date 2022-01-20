import pygame

# RGB Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (40, 40, 40)
OAK = (120, 81, 45)

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 100

material = {
    "r": -5, "n": -3, "b": -3, "q": -9, "k": -0.5, "p": -1,
    "R": 5,  "N": 3,  "B": 3,  "Q": 9,  "K": 0.5,  "P": 1,
}

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