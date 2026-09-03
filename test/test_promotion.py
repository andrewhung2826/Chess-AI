import unittest

from chess_engine.game.board import Board
from chess_engine.game.piece import Pawn, Queen, Rook, Bishop, Knight
from chess_engine.game.move import Move
from chess_engine.game.square import Square
from chess_engine.rules.move_rules import MoveRules


class TestPromotion(unittest.TestCase):

    def create_empty_board(self):
        board = Board()

        for row in range(8):
            for col in range(8):
                board.squares[row][col].piece = None

        return board


    # ========================================
    # MOVE GENERATION
    # ========================================

    def test_white_pawn_has_four_promotion_moves(self):
        board = self.create_empty_board()

        pawn = Pawn("white")
        board.squares[1][0].piece = pawn

        moves = MoveRules.get_moves(
            board,
            1,
            0,
            pawn
        )

        promotion_moves = [
            move for move in moves
            if move.final.row == 0
            and move.final.col == 0
        ]

        self.assertEqual(
            len(promotion_moves),
            4
        )

        promotions = {
            move.promotion
            for move in promotion_moves
        }

        self.assertEqual(
            promotions,
            {"queen", "rook", "bishop", "knight"}
        )


    def test_black_pawn_has_four_promotion_moves(self):
        board = self.create_empty_board()

        pawn = Pawn("black")
        board.squares[6][0].piece = pawn

        moves = MoveRules.get_moves(
            board,
            6,
            0,
            pawn
        )

        promotion_moves = [
            move for move in moves
            if move.final.row == 7
            and move.final.col == 0
        ]

        self.assertEqual(
            len(promotion_moves),
            4
        )


    # ========================================
    # BOARD MOVE
    # ========================================

    def test_promote_to_queen(self):
        board = self.create_empty_board()

        pawn = Pawn("white")
        board.squares[1][0].piece = pawn

        move = Move(
            Square(1, 0),
            Square(0, 0),
            promotion="queen"
        )

        board.move(move)

        promoted_piece = board.squares[0][0].piece

        self.assertIsInstance(
            promoted_piece,
            Queen
        )

        self.assertEqual(
            promoted_piece.color,
            "white"
        )


    def test_promote_to_rook(self):
        board = self.create_empty_board()

        pawn = Pawn("white")
        board.squares[1][0].piece = pawn

        move = Move(
            Square(1, 0),
            Square(0, 0),
            promotion="rook"
        )

        board.move(move)

        self.assertIsInstance(
            board.squares[0][0].piece,
            Rook
        )


    def test_promote_to_bishop(self):
        board = self.create_empty_board()

        pawn = Pawn("white")
        board.squares[1][0].piece = pawn

        move = Move(
            Square(1, 0),
            Square(0, 0),
            promotion="bishop"
        )

        board.move(move)

        self.assertIsInstance(
            board.squares[0][0].piece,
            Bishop
        )


    def test_promote_to_knight(self):
        board = self.create_empty_board()

        pawn = Pawn("white")
        board.squares[1][0].piece = pawn

        move = Move(
            Square(1, 0),
            Square(0, 0),
            promotion="knight"
        )

        board.move(move)

        self.assertIsInstance(
            board.squares[0][0].piece,
            Knight
        )


if __name__ == "__main__":
    unittest.main()