import chess
import pygame
import os
import neat

from multiprocessing import Process
from agent.agent import Agent
from settings import *

# TODO:
# 1) *COMPLETED* pop all parallel arrays and insert in beginning to simulate round robin tournament
# 2) list of openings moves in theory book
# 3) endgame theory
# 4) look into how to know what depth to search to
# 5) work on currently looking through all possible moves opponent can play while they are processing

# SCHOLAR'S MATE FEN => r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4
generation = 0
pygame.init()


class Game:
    def __init__(self, white_player, black_player, id):
        self.white_player = white_player
        self.black_player = black_player
        self.board        = chess.Board()
        self.game_over    = False
        self.id           = id

    def play(self):
        run = True

        while run:
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
                run = False
                update_results(self.board.outcome().result())
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


def update_results(result, index):
    global ge
    
    if result == "1-0":
        ge[index].fitness += 1
    elif result == "0-1":
        ge[index + 1].fitness += 1
    else:
        ge[index].fitness += 0.5
        ge[index + 1].fitness += 0.5


def main(genomes, config):
    # setting up of the next generation
    # will play a round robin tournament and whatever network has the most points will reproduce
    global generation, ge
    generation += 1

    networks  = []
    players   = []
    ge        = []

    colour = "w"

    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        networks.append(network)
        players.append(Agent(colour=colour, network=network))

        if colour == "w":
            colour = "b"
        else:
            colour = "w"

        genome.fitness = 0
        ge.append(genome)

    for _ in range(len(players)):
        processes = []
        games     = []

        last_player = players.pop()
        players.insert(0, last_player)

        for player in players:
            player.flip_colour()

        for i in range(0, len(players), 2):
            games.append(Game(players[i], players[i + 1], id=i))
            
        for game in games:
            processes.append(Process(target=game.play))

        for process in processes:
            process.start()

        for process in processes:
            process.join()


def setup(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)

    # setup population
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # running games and training
    population.run(main, 12)


if __name__ == "__main__":
    config_path = os.path.join(os.getcwd(), "config-feedforward.txt")
    setup(config_path)
