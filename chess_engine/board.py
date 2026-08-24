from .const import ROWS, COLS
from .square import Square
from .piece import Pawn, Knight, Bishop, Rook, Queen, King


class Board:

    def __init__(self):
        self.squares = self.create_board()
        self.add_pieces("white")
        self.add_pieces("black")

        self.last_move = None


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

        initial_square = self.squares[initial.row][initial.col]
        final_square = self.squares[final.row][final.col]

        piece = initial_square.piece 

        initial_square.piece = None

        # EN PASSANT
        if move.is_en_passant:
            self.squares[initial.row][final.col].piece = None 

        # NORMAL MOVE
        final_square.piece = piece

        # CASTLING
        if move.is_castling:

            # KINGSIDE
            if final.col > initial.col:
                rook_initial_col = 7
                rook_final_col = 5

            # QUEENSIDE
            else:
                rook_initial_col = 0
                rook_final_col = 3

            rook = self.squares[initial.row][rook_initial_col].piece

            self.squares[initial.row][rook_initial_col].piece = None

            self.squares[initial.row][rook_final_col].piece = rook

            rook.moved = True

        # PROMOTION
        if isinstance(piece, Pawn) and move.promotion:
            promoted_piece = self.promote_pawn(move, piece)

            final_square.piece = promoted_piece
            piece = promoted_piece

        piece.moved = True

        self.last_move = move


    def promote_pawn(self, move, piece):

        if move.promotion is None:
            return piece 

        color = piece.color 

        if move.promotion == "queen":
            return Queen(color)

        elif move.promotion == "rook":
            return Rook(color)

        elif move.promotion == "bishop":
            return Bishop(color)

        elif move.promotion == "knight":
            return Knight(color)