import unittest

from chess_engine.board import Board
from chess_engine.square import Square
from chess_engine.piece import King, Rook, Bishop
from chess_engine.rules.move_rules import MoveRules


class TestCastling(unittest.TestCase):

    def create_empty_board(self):
        board = Board()

        for row in range(8):
            for col in range(8):
                board.squares[row][col].piece = None

        board.last_move = None

        return board


    # ========================================
    # KINGSIDE
    # ========================================

    def test_white_kingside_castling_generated(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertTrue(
            any(
                move.is_castling
                and move.final.row == 7
                and move.final.col == 6
                for move in moves
            )
        )


    # ========================================
    # QUEENSIDE
    # ========================================

    def test_white_queenside_castling_generated(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")

        board.squares[7][4].piece = king
        board.squares[7][0].piece = rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertTrue(
            any(
                move.is_castling
                and move.final.row == 7
                and move.final.col == 2
                for move in moves
            )
        )


    # ========================================
    # KING / ROOK ALREADY MOVED
    # ========================================

    def test_no_castling_if_king_moved(self):

        board = self.create_empty_board()

        king = King("white")
        king.moved = True

        rook = Rook("white")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                for move in moves
            )
        )


    def test_no_castling_if_rook_moved(self):

        board = self.create_empty_board()

        king = King("white")

        rook = Rook("white")
        rook.moved = True

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                for move in moves
            )
        )


    # ========================================
    # PIECE BETWEEN
    # ========================================

    def test_no_kingside_castling_if_piece_between(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")
        bishop = Bishop("white")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        # Bishop ở f1
        board.squares[7][5].piece = bishop

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                for move in moves
            )
        )


    def test_no_queenside_castling_if_piece_between(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")
        bishop = Bishop("white")

        board.squares[7][4].piece = king
        board.squares[7][0].piece = rook

        # Bishop ở b1
        board.squares[7][1].piece = bishop

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                for move in moves
            )
        )


    # ========================================
    # ATTACKED SQUARES
    # ========================================

    def test_no_castling_if_king_in_check(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")
        enemy_rook = Rook("black")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        # Black Rook attack e1
        board.squares[0][4].piece = enemy_rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                for move in moves
            )
        )


    def test_no_kingside_castling_if_king_passes_through_attack(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")
        enemy_rook = Rook("black")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        # Black Rook attack f1
        board.squares[0][5].piece = enemy_rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                and move.final.col == 6
                for move in moves
            )
        )


    def test_no_kingside_castling_if_final_square_attacked(self):

        board = self.create_empty_board()

        king = King("white")
        rook = Rook("white")
        enemy_rook = Rook("black")

        board.squares[7][4].piece = king
        board.squares[7][7].piece = rook

        # Black Rook attack g1
        board.squares[0][6].piece = enemy_rook

        moves = MoveRules.get_moves(
            board,
            7,
            4,
            king
        )

        self.assertFalse(
            any(
                move.is_castling
                and move.final.col == 6
                for move in moves
            )
        )


if __name__ == "__main__":
    unittest.main()