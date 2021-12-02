import chess
import pygame

WIDTH = 800
HEIGHT = 800

board = chess.Board()
win = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
