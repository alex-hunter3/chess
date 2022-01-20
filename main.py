import chess
import pygame
import os
import neat

from player import Player
from agent import Agent
from settings import *

# SCHOLAR'S MATE FEN => r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4
generation = 0

# if input("Human colour (W/B): ").lower() == "w":
#     white_player = Player(colour="w")
#     black_player = Agent(colour="b")
# else:
#     white_player = Agent(colour="w")
#     black_player = Player(colour="b")


# os.system("clear")


class Game:
    def __init__(self, white_player, black_player):
        self.white_player = white_player
        self.black_player = black_player
        self.board        = chess.Board()
        self.run          = True

        # setup board and widow
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_icon(pygame.image.load("./imgs/black/knight.png"))
        pygame.display.set_caption("Chess")

    def play(self):
        while self.run:
            # self.draw_board()
            # self.draw_pieces()

            # pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            turn = self.board.fen().split()[1]

            if turn == "w":
                move = self.white_player.get_move(self.board)
            else:
                move = self.black_player.get_move(self.board)

            if move:
                self.board.push(move)


    def draw_board(self):
        self.win.fill(WHITE)
        pygame.draw.rect(self.win, OAK, (0, 0, 800, 800))

        for rank in range(8):
            for square in range(rank % 2, 8, 2):
                pygame.draw.rect(
                    self.win,
                    WHITE,
                    (rank * SQUARE_SIZE, square * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

    def draw_pieces(self):
        fen = self.board.fen().split()[0].split("/")
        
        for rank, rank_pieces in enumerate(fen):
            file = 0

            for square in rank_pieces:
                if square.isnumeric():
                    file += int(square)
                else:
                    self.win.blit(
                        images[square],
                        (file * SQUARE_SIZE, rank * SQUARE_SIZE)
                    )
                    file += 1

    def get_material(self):
        total_material = 0
        fen = self.board.fen().split()[0].split("/")
        
        for rank_pieces in fen:
            for square in rank_pieces:
                if not square.isnumeric():
                    total_material += material[square]

        return total_material


def main(genomes, config):
    # setting up of the next generation
    # will play a round robin tournament and whatever network has the most points will progress
    global generation
    generation += 1

    games          = []
    white_networks = []
    black_networks = []
    ge             = []

    for _, genome in genomes:
        white_network = neat.nn.FeedForwardNetwork.create(genome, config)
        black_network = neat.nn.FeedForwardNetwork.create(genome, config)

        white_networks.append(white_network)
        black_networks.append(black_network)

        white_player = Agent(colour="w", network=white_network)
        black_player = Agent(colour="b", network=black_network)

        games.append(Game(white_player, black_player))


def setup(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)

    population = neat.Population(config)
    population.run(main, 12)


if __name__ == "__main__":
    config_path = os.path.join(os.getcwd(), "config-feedforward.txt")
    setup(config_path)
