import neat
import math
from settings import *


class Agent:
    def __init__(self, colour, network):
        if colour != "w" and colour != "b":
            raise ValueError("colour argument must either be w or b")

        self.colour  = colour
        self.network = network

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
        return self.get_material(board)

    def minimax(self, board, maximizing_player, alpha, beta, depth=18):
        if board.outcome():
            if board.outcome().result() == "1-0" and self.colour == "w":
                return math.inf
            elif board.outcome().result() == "1-0" and self.colour == "b":
                return -math.inf

            if board.outcome().result() == "0-1" and self.colour == "b":
                return math.inf
            elif board.outcome().result() == "1-0" and self.colour == "w":
                return -math.inf

            if board.outcome().result() == "1/2-1/2":
                return 0

        if depth == 0:
            # return static evaluation of the position
            return self.evaluate(board)
        
        if maximizing_player:
            max_eval = -math.inf

            for child in self.legal_moves(board):
                board.push(child)
                eval = self.minimax(board, False, alpha, beta, depth - 1)
                board.pop()

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break
            
            return max_eval

        else:
            min_eval = math.inf

            for child in self.legal_moves(board):
                board.push(child)
                eval = self.minimax(board, True, alpha, beta, depth - 1)
                board.pop()

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break
            
            return min_eval
    
    def get_move(self, board, depth=18):
        # board, maximizing_player, alpha, beta, depth=18
        eval = self.minimax(board, True, -math.inf, math.inf, 5)
        print(eval)