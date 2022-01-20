import neat


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
    
    def get_move(self, board, depth=18):
        moves = self.legal_moves(board)