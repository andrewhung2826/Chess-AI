import unittest

from chess_engine.board import Board
from chess_engine.square import Square
from chess_engine.piece import King, Queen, Rook
from chess_engine.rules.game_rules import GameRules


class TestGameRules(unittest.TestCase):

    def create_empty_board(self):
        board = Board()

        # Xóa toàn bộ quân khỏi bàn cờ
        for row in range(8):
            for col in range(8):
                board.squares[row][col].piece = None

        return board


    def place_piece(self, board, row, col, piece):
        board.squares[row][col].piece = piece


    # ========================================
    # CHECKMATE
    # ========================================

    def test_white_is_checkmated(self):
        board = self.create_empty_board()

        # White King: a1
        self.place_piece(
            board, 7, 0,
            King("white")
        )

        # Black King: c3
        self.place_piece(
            board, 5, 2,
            King("black")
        )

        # Black Queen: b2
        self.place_piece(
            board, 6, 1,
            Queen("black")
        )

        self.assertTrue(
            GameRules.is_checkmate(board, "white")
        )


    def test_not_checkmate_if_king_has_escape(self):
        board = self.create_empty_board()

        # White King: a1
        self.place_piece(
            board, 7, 0,
            King("white")
        )

        # Black Rook: a8
        self.place_piece(
            board, 0, 0,
            Rook("black")
        )

        # White King đang bị check nhưng vẫn có đường chạy
        self.assertFalse(
            GameRules.is_checkmate(board, "white")
        )


    # ========================================
    # STALEMATE
    # ========================================

    def test_white_is_stalemated(self):
        board = self.create_empty_board()

        # White King: a1
        self.place_piece(
            board, 7, 0,
            King("white")
        )

        # Black King: c2
        self.place_piece(
            board, 6, 2,
            King("black")
        )

        # Black Queen: b3
        self.place_piece(
            board, 5, 1,
            Queen("black")
        )

        self.assertTrue(
            GameRules.is_stalemate(board, "white")
        )


    def test_not_stalemate_if_king_has_move(self):
        board = self.create_empty_board()

        # White King: a1
        self.place_piece(
            board, 7, 0,
            King("white")
        )

        # Black King: c3
        self.place_piece(
            board, 5, 2,
            King("black")
        )

        self.assertFalse(
            GameRules.is_stalemate(board, "white")
        )


    # ========================================
    # HAS LEGAL MOVES
    # ========================================

    def test_has_legal_moves(self):
        board = self.create_empty_board()

        self.place_piece(
            board, 7, 4,
            King("white")
        )

        self.place_piece(
            board, 0, 4,
            King("black")
        )

        self.assertTrue(
            GameRules.has_legal_moves(board, "white")
        )

        self.assertTrue(
            GameRules.has_legal_moves(board, "black")
        )


if __name__ == "__main__":
    unittest.main()