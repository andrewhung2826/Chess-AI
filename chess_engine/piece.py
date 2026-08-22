


class Piece:

    def __init__(self, name, color, symbol):
        self.color = color
        self.name = name 
        self.symbol = symbol

        self.moved = False


class Pawn(Piece):

    def __init__(self, color):
        super().__init__("pawn", color, "P")


class Knight(Piece):

    def __init__(self, color):
        super().__init__("knight", color, "N")


class Bishop(Piece):

    def __init__(self, color):
        super().__init__("bishop", color, "B")


class Rook(Piece):

    def __init__(self, color):
        super().__init__("rook", color, "R")


class Queen(Piece):

    def __init__(self, color):
        super().__init__("queen", color, "Q")


class King(Piece):

    def __init__(self, color):
        super().__init__("king", color, "K")