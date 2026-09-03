import unittest

from chess_engine.game.board import Board
from chess_engine.game.square import Square
from chess_engine.game.move import Move
from chess_engine.game.piece import King, Rook


class TestCastlingExecution(unittest.TestCase):

    def create_empty_board(self):
        board = Board()

        for row in range(8):
            for col in range(8):
                board.squares[row][col].piece = None

        board.last_move = None

        return board

    # ========================================
    # WHITE KINGSIDE CASTLING
    # ========================================

    def test_white_kingside_castling_execution(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        move = Move(
            Square(7, 4),
            Square(7, 6),
            is_castling=True
        )

        board.move(move)

        # King: e1 -> g1
        self.assertIsNone(
            board.squares[7][4].piece
        )

        self.assertIs(
            board.squares[7][6].piece,
            king
        )

        # Rook: h1 -> f1
        self.assertIsNone(
            board.squares[7][7].piece
        )

        self.assertIs(
            board.squares[7][5].piece,
            rook
        )

        # moved state
        self.assertTrue(king.moved)
        self.assertTrue(rook.moved)

    # ========================================
    # WHITE QUEENSIDE CASTLING
    # ========================================

    def test_white_queenside_castling_execution(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")

        board.squares[7][4].piece = king
        board.squares[7][0].piece = rook

        move = Move(
            Square(7, 4),
            Square(7, 2),
            is_castling=True
        )

        board.move(move)

        # King: e1 -> c1
        self.assertIsNone(
            board.squares[7][4].piece
        )

        self.assertIs(
            board.squares[7][2].piece,
            king
        )

        # Rook: a1 -> d1
        self.assertIsNone(
            board.squares[7][0].piece
        )

        self.assertIs(
            board.squares[7][3].piece,
            rook
        )

        # moved state
        self.assertTrue(king.moved)
        self.assertTrue(rook.moved)

    # ========================================
    # BLACK KINGSIDE CASTLING
    # ========================================

    def test_black_kingside_castling_execution(self):

        board = self.create_empty_board()

        king = King("black")
        rook = Rook("black")

        board.squares[0][4].piece = king
        board.squares[0][7].piece = rook

        move = Move(
            Square(0, 4),
            Square(0, 6),
            is_castling=True
        )

        board.move(move)

        self.assertIsNone(board.squares[0][4].piece)
        self.assertIs(board.squares[0][6].piece, king)

        self.assertIsNone(board.squares[0][7].piece)
        self.assertIs(board.squares[0][5].piece, rook)

        self.assertTrue(king.moved)
        self.assertTrue(rook.moved)

    # ========================================
    # BLACK QUEENSIDE CASTLING
    # ========================================

    def test_black_queenside_castling_execution(self):

        board = self.create_empty_board()

        king = King("black")
        rook = Rook("black")

        board.squares[0][4].piece = king
        board.squares[0][0].piece = rook

        move = Move(
            Square(0, 4),
            Square(0, 2),
            is_castling=True
        )

        board.move(move)

        self.assertIsNone(board.squares[0][4].piece)
        self.assertIs(board.squares[0][2].piece, king)

        self.assertIsNone(board.squares[0][0].piece)
        self.assertIs(board.squares[0][3].piece, rook)

        self.assertTrue(king.moved)
        self.assertTrue(rook.moved)


if __name__ == "__main__":
    unittest.main()