import math
import chess

from copy import deepcopy
from settings import *


class Agent:
    def __init__(self, colour, network, search_depth=18):
        if colour != "w" and colour != "b":
            raise ValueError("colour argument must either be w or b")

        self.colour       = colour
        self.network      = network
        self.search_depth = search_depth
        self.score        = 0
        self.best_move    = None

        # each index is the corresponding square in chess library
        # Example: positions index 0 = chess.A1
        self.positions = []
        alphabet = "abcdefgh"

        for i in range(1, 9):
            for letter in alphabet:
                self.positions.append(f"{letter}{i}")

    def legal_moves(self, board):
        legal_moves = []

        for move in board.legal_moves:
            legal_moves.append(move)

        return legal_moves

    def get_material(self, board):
        total_material = 0
        fen = board.fen().split()[0].split("/")
        
        for rank_pieces in fen:
            for square in rank_pieces:
                if not square.isnumeric():
                    total_material += material[square]

        return total_material

    def evaluate(self, board):
        fen = board.fen().split()[0].split("/")
        flattened_board = []

        for rank in fen:
            for square in rank:
                if square.isnumeric():
                    for _ in range(int(square)):
                        flattened_board.append(0)
                else:
                    flattened_board.append(material[square])

        # return self.get_material(board)
        return self.network.activate(tuple(flattened_board))[0]

    def minimax(self, board, maximizing_player, alpha, beta, depth):
        # board = deepcopy(board)
        
        if board.outcome():
            if board.outcome().result() == "1-0" and self.colour == "w":
                return math.inf, board
            elif board.outcome().result() == "1-0" and self.colour == "b":
                return -math.inf, board

            if board.outcome().result() == "0-1" and self.colour == "b":
                return math.inf, board
            elif board.outcome().result() == "1-0" and self.colour == "w":
                return -math.inf, board

            if board.outcome().result() == "1/2-1/2":
                return 0, board

        if depth == 0:
            # return static evaluation of the position
            return self.evaluate(board), board
        
        if maximizing_player:
            max_eval  = -math.inf
            best_move = None

            for child in self.legal_moves(board):
                board.push(child)
                eval = self.minimax(board, False, alpha, beta, depth - 1)[0]
                board.pop()

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if max_eval == eval:
                    best_move = child

                if beta <= alpha:
                    break
            
            return max_eval, best_move

        else:
            min_eval  = math.inf
            best_move = None

            for child in self.legal_moves(board):
                board.push(child)
                eval = self.minimax(board, True, alpha, beta, depth - 1)[0]
                board.pop()

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if min_eval == eval:
                    best_move = child

                if beta <= alpha:
                    break
            
            return min_eval, best_move
    
    def get_move(self, board):
        return self.minimax(board, True, -math.inf, math.inf, self.search_depth)


# for testing
if __name__ == "__main__":
    board = chess.Board()

    w_agent = Agent("w", None, 4)
    (eval, move) = w_agent.get_move(board)
    print(eval, move)