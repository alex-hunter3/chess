import chess
import os
import neat

from multiprocessing import Pool
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


def play(ge):
    global players
    run = True
    white_player = white_player
    black_player = black_player
    board = chess.Board()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        turn = board.fen().split()[1]

        if turn == "w":
            move = white_player.get_move(board)[1]
        else:
            move = black_player.get_move(board)[1]

        if move:
            board.push(move)
        else:
            print(move)

        if board.outcome():
            run = False
            result = board.outcome().result()

            print(f"***Game finished***")
            print(f"Result: {board.outcome().result()}")

            if result == "1-0":
                return [ge[0] + 1, ge[1]]
            elif result == "0-1":
                return [ge[0], ge[1] + 1]
            else:
                return [ge[0] + 0.5, ge[1] + 0.5]


def main(genomes, config):
    # setting up of the next generation
    global generation, players
    generation += 1

    networks = []
    players = []
    ge = []

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

    tournament_round = 1

    for _ in range(len(players)):
        last_player = players.pop()
        players.insert(0, last_player)
        last_network = networks.pop()
        networks.insert(0, last_network)
        last_ge = ge.pop()
        ge.insert(0, last_ge)

        # for i in range(0, len(players), 2):
        #     games.append(Game(players[i], players[i + 1], id=i))

        # grouping all networks together
        for i in range(0, len(ge), 2):
            ge[i] = [ge[i], ge[i + 1]]

        p = Pool()
        ge = p.map(play, ge)

        temp = []

        # reflattening ge list
        for group in ge:
            temp.append(group[0])
            temp.append(group[1])

        ge = temp

        # for game in games:
        #     processes.append(Process(target=game.play))

        # for process in processes:
        #     process.start()

        # for process in processes:
        #     process.join()

        # flip colours after all games are finished before moving onto next game
        for player in players:
            player.flip_colour()

        print(f"***All games completed moving onto round {tournament_round}***")
        tournament_round += 1


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
    config_path = os.path.join(os.getcwd(), "agent", "config-feedforward.txt")
    setup(config_path)
