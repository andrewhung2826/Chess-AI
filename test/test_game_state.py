import unittest

from chess_engine.game.game_state import GameState
from chess_engine.game.square import Square
from chess_engine.game.move import Move
from chess_engine.game.piece import King, Rook, Queen


class TestGameState(unittest.TestCase):

    # ========================================
    # 1. INITIAL POSITION
    # ========================================

    def test_initial_turn_is_white(self):

        game = GameState()

        self.assertEqual(
            game.turn,
            "white"
        )


    # ========================================
    # 2. ALL LEGAL MOVES
    # ========================================

    def test_initial_position_has_legal_moves(self):

        game = GameState()

        moves = game.get_all_legal_moves()

        self.assertGreater(
            len(moves),
            0
        )


    # ========================================
    # 3. CANNOT MOVE OPPONENT PIECE
    # ========================================

    def test_cannot_get_moves_for_opponent_piece(self):

        game = GameState()

        # Black pawn at row 1, col 0
        moves = game.get_legal_moves(
            1,
            0
        )

        self.assertEqual(
            moves,
            []
        )


    # ========================================
    # 4. VALID MOVE SWITCHES TURN
    # ========================================

    def test_valid_move_switches_turn(self):

        game = GameState()

        # White pawn e2 -> e4
        move = Move(
            Square(6, 4),
            Square(4, 4)
        )

        success = game.make_move(move)

        self.assertTrue(success)

        self.assertEqual(
            game.turn,
            "black"
        )


    # ========================================
    # 5. INVALID MOVE DOES NOT SWITCH TURN
    # ========================================

    def test_invalid_move_does_not_switch_turn(self):

        game = GameState()

        # White pawn e2 -> e5
        move = Move(
            Square(6, 4),
            Square(3, 4)
        )

        success = game.make_move(move)

        self.assertFalse(success)

        self.assertEqual(
            game.turn,
            "white"
        )


    # ========================================
    # 6. GAME OVER BLOCKS MOVE
    # ========================================

    def test_game_over_blocks_move(self):

        game = GameState()

        game.game_over = True

        move = Move(
            Square(6, 4),
            Square(4, 4)
        )

        success = game.make_move(move)

        self.assertFalse(success)

        self.assertEqual(
            game.turn,
            "white"
        )

    def test_initial_position_has_20_legal_moves(self):

        game = GameState()

        moves = game.get_all_legal_moves()

        self.assertEqual(
            len(moves),
            20
        )

    def test_get_all_black_moves_when_white_turn(self):

        game = GameState()

        self.assertEqual(
            game.turn,
            "white"
        )

        black_moves = game.get_all_legal_moves(
            "black"
        )

        self.assertEqual(
            len(black_moves),
            20
        )

    def test_checkmate_updates_game_status(self):

        game = GameState()

        # Clear board
        for row in range(8):
            for col in range(8):
                game.board.squares[row][col].piece = None

        # White King a8
        game.board.squares[0][0].piece = King("white")

        # Black Queen b7
        game.board.squares[1][1].piece = Queen("black")

        # Black King b6
        game.board.squares[2][1].piece = King("black")

        game.turn = "white"

        game.update_game_status()

        self.assertTrue(game.game_over)

        self.assertEqual(
            game.result,
            "black wins by checkmate"
        )

    def test_stalemate_updates_game_status(self):

        game = GameState()

        # Clear board
        for row in range(8):
            for col in range(8):
                game.board.squares[row][col].piece = None

        # White King a8
        game.board.squares[0][0].piece = King("white")

        # Black Queen b6
        game.board.squares[2][1].piece = Queen("black")

        # Black King c7
        game.board.squares[1][2].piece = King("black")

        # White's turn
        game.turn = "white"

        game.update_game_status()

        self.assertTrue(
            game.game_over
        )

        self.assertEqual(
            game.result,
            "draw by stalemate"
        )

if __name__ == "__main__":
    unittest.main()