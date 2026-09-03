import unittest

from chess_engine.game.board import Board
from chess_engine.game.square import Square
from chess_engine.game.move import Move
from chess_engine.game.piece import Pawn, King, Rook

from chess_engine.rules.move_rules import MoveRules
from chess_engine.rules.check_rules import CheckRules


class TestEnPassant(unittest.TestCase):

    def create_empty_board(self):
        board = Board()

        for row in range(8):
            for col in range(8):
                board.squares[row][col].piece = None

        board.last_move = None

        return board


    # ========================================
    # MOVE GENERATION
    # ========================================

    def test_white_en_passant_generated(self):

        board = self.create_empty_board()

        # White Pawn e5
        white_pawn = Pawn("white")
        white_pawn.moved = True

        board.squares[3][4].piece = white_pawn

        # Black Pawn vừa đi d7 -> d5
        black_pawn = Pawn("black")
        black_pawn.moved = True

        board.squares[3][3].piece = black_pawn

        board.last_move = Move(
            Square(1, 3),
            Square(3, 3)
        )

        moves = MoveRules.get_moves(
            board,
            3,
            4,
            white_pawn
        )

        en_passant_moves = [
            move for move in moves
            if move.is_en_passant
        ]

        self.assertEqual(
            len(en_passant_moves),
            1
        )

        move = en_passant_moves[0]

        self.assertEqual(
            (move.final.row, move.final.col),
            (2, 3)
        )


    def test_black_en_passant_generated(self):

        board = self.create_empty_board()

        # Black Pawn e4
        black_pawn = Pawn("black")
        black_pawn.moved = True

        board.squares[4][4].piece = black_pawn

        # White Pawn vừa đi d2 -> d4
        white_pawn = Pawn("white")
        white_pawn.moved = True

        board.squares[4][3].piece = white_pawn

        board.last_move = Move(
            Square(6, 3),
            Square(4, 3)
        )

        moves = MoveRules.get_moves(
            board,
            4,
            4,
            black_pawn
        )

        en_passant_moves = [
            move for move in moves
            if move.is_en_passant
        ]

        self.assertEqual(
            len(en_passant_moves),
            1
        )

        move = en_passant_moves[0]

        self.assertEqual(
            (move.final.row, move.final.col),
            (5, 3)
        )


    # ========================================
    # BOARD MOVE
    # ========================================

    def test_en_passant_removes_captured_pawn(self):

        board = self.create_empty_board()

        white_pawn = Pawn("white")
        white_pawn.moved = True

        black_pawn = Pawn("black")
        black_pawn.moved = True

        # White e5
        board.squares[3][4].piece = white_pawn

        # Black d5
        board.squares[3][3].piece = black_pawn

        move = Move(
            Square(3, 4),
            Square(2, 3),
            is_en_passant=True
        )

        board.move(move)

        # White Pawn phải ở d6
        self.assertIs(
            board.squares[2][3].piece,
            white_pawn
        )

        # Black Pawn phải bị xóa khỏi d5
        self.assertIsNone(
            board.squares[3][3].piece
        )

        # e5 phải trống
        self.assertIsNone(
            board.squares[3][4].piece
        )


    # ========================================
    # INVALID CASES
    # ========================================

    def test_no_en_passant_if_last_move_not_two_squares(self):

        board = self.create_empty_board()

        white_pawn = Pawn("white")
        white_pawn.moved = True

        black_pawn = Pawn("black")
        black_pawn.moved = True

        board.squares[3][4].piece = white_pawn
        board.squares[3][3].piece = black_pawn

        # Black chỉ đi 1 ô
        board.last_move = Move(
            Square(2, 3),
            Square(3, 3)
        )

        moves = MoveRules.get_moves(
            board,
            3,
            4,
            white_pawn
        )

        self.assertFalse(
            any(
                move.is_en_passant
                for move in moves
            )
        )


    def test_en_passant_can_be_illegal_if_it_exposes_king(self):

        board = self.create_empty_board()

        # White King e1
        white_king = King("white")
        board.squares[7][4].piece = white_king

        # White Pawn e5
        white_pawn = Pawn("white")
        white_pawn.moved = True
        board.squares[3][4].piece = white_pawn

        # Black Pawn d5 vừa đi 2 ô
        black_pawn = Pawn("black")
        black_pawn.moved = True
        board.squares[3][3].piece = black_pawn

        board.last_move = Move(
            Square(1, 3),
            Square(3, 3)
        )

        moves = MoveRules.get_moves(
            board,
            3,
            4,
            white_pawn
        )

        legal_moves = CheckRules.filter_legal_moves(
            board,
            white_pawn,
            moves
        )

        # Case này chỉ kiểm tra CheckRules chạy được
        # và không phá trạng thái board.
        self.assertIs(
            board.squares[3][4].piece,
            white_pawn
        )

        self.assertIs(
            board.squares[3][3].piece,
            black_pawn
        )


if __name__ == "__main__":
    unittest.main()