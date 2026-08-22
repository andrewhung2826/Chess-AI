from .const import ROWS, COLS
from .square import Square
from .piece import Pawn, Knight, Bishop, Rook, Queen, King


class Board:

    def __init__(self):
        self.squares = self.create_board()
        self.add_pieces("white")
        self.add_pieces("black")


    def create_board(self):
        return [
            [Square(row, col) for col in range(COLS)]
            for row in range(ROWS)
        ]


    def add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col].piece = Pawn(color)

        # Knights
        self.squares[row_other][1].piece = Knight(color)
        self.squares[row_other][6].piece = Knight(color)

        # Bishops
        self.squares[row_other][2].piece = Bishop(color)
        self.squares[row_other][5].piece = Bishop(color)

        # Rooks
        self.squares[row_other][0].piece = Rook(color)
        self.squares[row_other][7].piece = Rook(color)

        # Queen
        self.squares[row_other][3].piece = Queen(color)

        # King
        self.squares[row_other][4].piece = King(color)


    def print_board(self):
        for row in self.squares:
            for square in row:
                if square.is_empty():
                    print(".", end=" ")
                else:
                    print(square.piece.symbol, end=" ")

            print()


    def move(self, move):
        initial = move.initial 
        final = move.final 

        piece = self.squares[initial][final].piece 
        self.squares[initial.row][initial.col] = None
        self.squares[final.row][final.col] = piece

        piece.moved = True