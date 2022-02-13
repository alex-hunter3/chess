import math
import chess


class Agent:
    def __init__(self, colour, network):
        if colour != "w" and colour != "b":
            raise ValueError("colour argument must either be w or b")

        self.colour       = colour
        self.network      = network
        self.score        = 0
        self.material     = {
            "r": -5, "n": -3, "b": -3.5, "q": -9, "k": -0.5, "p": -1,
            "R": 5,  "N": 3,  "B": 3.5,  "Q": 9,  "K": 0.5,  "P": 1,
        }

    def get_material(self, board):
        total_material = 0
        fen = board.fen().split()[0].split("/")
        
        for rank_pieces in fen:
            for square in rank_pieces:
                if not square.isnumeric():
                    total_material += self.material[square]

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
                    flattened_board.append(self.material[square])

        # return self.get_material(board)
        return self.network.activate(tuple(flattened_board))[0]

    def minimax(self, board, maximizing_player, alpha, beta, depth):
        if board.outcome():
            if board.outcome().result() == "1-0" and self.colour == "w":
                return math.inf, None
            elif board.outcome().result() == "1-0" and self.colour == "b":
                return -math.inf, None

            if board.outcome().result() == "0-1" and self.colour == "b":
                return math.inf, None
            elif board.outcome().result() == "1-0" and self.colour == "w":
                return -math.inf, None

            if board.outcome().result() == "1/2-1/2":
                return 0, None

        if depth == 0:
            # return static evaluation of the position
            return self.evaluate(board), None
        
        if maximizing_player:
            max_eval  = -math.inf
            best_move = None

            for child in board.legal_moves:
                board.push(child)
                eval = self.minimax(board, False, alpha, beta, depth - 1)[0]
                board.pop()

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                # might be == instead
                if max_eval >= eval:
                    best_move = child

                if beta <= alpha:
                    break
            
            return max_eval, best_move

        else:
            min_eval  = math.inf
            best_move = None

            for child in board.legal_moves:
                board.push(child)
                eval = self.minimax(board, True, alpha, beta, depth - 1)[0]
                board.pop()

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                # might be == instead
                if min_eval <= eval:
                    best_move = child

                if beta <= alpha:
                    break
            
            return min_eval, best_move
    
    def get_move(self, board, search_depth=4):
        if self.colour == "w":
            return self.minimax(board, True, -math.inf, math.inf, search_depth)
        else:
            return self.minimax(board, False, -math.inf, math.inf, search_depth)

    def flip_colour(self):
        if self.colour == "w":
            self.colour = "b"
        else:
            self.colour = "w"


# for testing
if __name__ == "__main__":
    board = chess.Board()

    w_agent = Agent("w", None)
    (eval, move) = w_agent.get_move(board, 6)
    print(eval, move)