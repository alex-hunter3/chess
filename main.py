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

        # setup board and widow
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_icon(pygame.image.load("./imgs/black/knight.png"))
        pygame.display.set_caption("Chess")

    def play(self):
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

        if self.board.outcome():
            if self.board.outcome().result() == "1-0":
                return (False, "w")
            elif self.board.outcome().result() == "0-1":
                return (False, "b")
            else:
                return (False, "d")
        else:
            return (True, None)

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
    # will play a round robin tournament and whatever network has the most points will reproduce
    global generation
    generation += 1

    games    = []
    networks = []
    players  = []
    ge       = []

    colour = "w"
    run    = True

    for _, genome in genomes:
        # might need to change so that the same nn gets training with both colours
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        networks.append(network)
        players.append(Agent(colour=colour, network=network))

        if colour == "w":
            colour = "b"
        else:
            colour = "w"

        genome.fitness = 0
        ge.append(genome)

    for i in range(0, len(players), 2):
        games.append(Game(players[i], players[i + 1]))

    while run:
        run = False

        for i, game in enumerate(games):
            # game.play returns true if game is still in progress and false if finished
            run, winner = game.play()

            if winner == "w":
                players[i].score += 1
            elif winner == "b":
                players[i + 1] += 1
            elif winner == "d":
                players[i] += 1
                players[i + 1] += 1


def setup(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)

    population = neat.Population(config)
    population.run(main, 12)


if __name__ == "__main__":
    config_path = os.path.join(os.getcwd(), "config-feedforward.txt")
    setup(config_path)
