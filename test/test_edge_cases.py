import unittest

from chess_engine.game.board import Board
from chess_engine.game.square import Square
from chess_engine.game.move import Move
from chess_engine.game.piece import Pawn, Rook, King, Queen

from chess_engine.rules.move_rules import MoveRules
from chess_engine.rules.check_rules import CheckRules


class TestEdgeCases(unittest.TestCase):

    def create_empty_board(self):
        board = Board()

        for row in range(8):
            for col in range(8):
                board.squares[row][col].piece = None

        board.last_move = None

        return board

    # ========================================
    # 1. PINNED PIECE
    # ========================================

    def test_pinned_piece_cannot_expose_king(self):

        board = self.create_empty_board()

        white_king = King("white")
        white_rook = Rook("white")
        black_rook = Rook("black")

        # Black Rook e8
        board.squares[0][4].piece = black_rook

        # White Rook e2
        board.squares[6][4].piece = white_rook

        # White King e1
        board.squares[7][4].piece = white_king

        moves = MoveRules.get_moves(
            board,
            6,
            4,
            white_rook
        )

        legal_moves = CheckRules.filter_legal_moves(
            board,
            white_rook,
            moves
        )

        # Rook không được đi ngang vì sẽ expose King
        for move in legal_moves:
            self.assertEqual(
                move.final.col,
                4
            )

    # ========================================
    # 2. EN PASSANT EXPOSES CHECK
    # ========================================

    def test_en_passant_cannot_expose_king(self):

        board = self.create_empty_board()

        white_king = King("white")
        white_pawn = Pawn("white")
        black_pawn = Pawn("black")
        black_rook = Rook("black")

        # Black Rook e8
        board.squares[0][4].piece = black_rook

        # Black Pawn d5
        board.squares[3][3].piece = black_pawn

        # White Pawn e5
        board.squares[3][4].piece = white_pawn

        # White King e1
        board.squares[7][4].piece = white_king

        # Tạo last_move giả:
        # Black Pawn từ d7 -> d5
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

        # e5 x d6 en passant phải bị loại
        for move in legal_moves:
            self.assertFalse(
                move.is_en_passant
            )

    # ========================================
    # 3. CASTLING TEMPORARY MOVE
    # ========================================

    def test_castling_filter_does_not_change_board(self):

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

        CheckRules.filter_legal_moves(
            board,
            king,
            moves
        )

        # Board phải được restore hoàn toàn
        self.assertIs(
            board.squares[7][4].piece,
            king
        )

        self.assertIs(
            board.squares[7][7].piece,
            rook
        )

        self.assertIsNone(
            board.squares[7][5].piece
        )

        self.assertIsNone(
            board.squares[7][6].piece
        )

        # Temporary move không được thay đổi moved state
        self.assertFalse(king.moved)
        self.assertFalse(rook.moved)

    # ========================================
    # 4. PROMOTION CAN RESOLVE CHECK
    # ========================================

    def test_promotion_is_simulated_when_checking_legality(self):

        board = self.create_empty_board()

        white_king = King("white")
        white_pawn = Pawn("white")
        black_rook = Rook("black")

        # White King e1
        board.squares[7][4].piece = white_king

        # Black Rook e8 đang chiếu xuống cột e
        board.squares[0][4].piece = black_rook

        # White Pawn e7
        board.squares[1][4].piece = white_pawn

        # Promotion move:
        # Pawn e7 -> e8 = Queen
        move = Move(
            Square(1, 4),
            Square(0, 4),
            promotion="queen"
        )

        legal_moves = CheckRules.filter_legal_moves(
            board,
            white_pawn,
            [move]
        )

        # Nước promotion capture phải được xem xét hợp lệ
        self.assertEqual(
            len(legal_moves),
            1
        )

        # Board phải restore
        self.assertIs(
            board.squares[1][4].piece,
            white_pawn
        )

        self.assertIs(
            board.squares[0][4].piece,
            black_rook
        )



if __name__ == "__main__":
    unittest.main()