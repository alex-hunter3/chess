import simple_term_menu


class Player:
    def __init__(self, colour):
        if colour != "w" and colour != "b":
            raise ValueError("colour argument must either be w or b")

        self.colour = colour

        # each index is the corresponding square in chess library
        # Example: positions index 0 = chess.A1
        self.positions = []
        alphabet = "abcdefgh"

        for i in range(1, 9):
            for letter in alphabet:
                self.positions.append(f"{letter}{i}")

    def get_move(self, board):
        legal_moves_string = []
        legal_moves_obj    = []

        for move in board.legal_moves:
            legal_moves_string.append(str(move))
            legal_moves_obj.append(move)

        menu = simple_term_menu.TerminalMenu(legal_moves_string)
        return legal_moves_obj[menu.show()]