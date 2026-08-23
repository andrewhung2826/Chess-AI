from .board import Board
from .rules.move_rules import MoveRules
from .rules.check_rules import CheckRules
from .rules.game_rules import GameRules



class GameState:

    def __init__(self):
        self.board = Board()
        self.turn = "white"

        self.game_over = False
        self.result = None

    def get_legal_moves(self, row, col):
        square = self.board.squares[row][col]

        if square.is_empty():
            return []
        piece = square.piece 

        if piece.color != self.turn:
            return []

        moves = MoveRules.get_moves(
            self.board, row, col, piece 
        )

        legal_moves = CheckRules.filter_legal_moves(
            self.board, piece, moves
        )

        return legal_moves

    def make_move(self, move):

        # CHECK GAME OVER
        if self.game_over:
            return False


        initial = move.initial 
        piece = self.board.squares[initial.row][initial.col].piece

        if piece is None:
            return False

        if piece.color != self.turn:
            return False

        legal_moves = self.get_legal_moves(
            initial.row, initial.col
        )

        if move not in legal_moves:
            return False

        self.board.move(move)

        self.switch_turn()

        self.update_game_status()

        return True


    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"


    def update_game_status(self):

        if GameRules.is_checkmate(self.board, self.turn):
            self.game_over = True

            winner = (
                "black"
                if self.turn == "white"
                else "white"
            )

            self.result = f"{winner} wins by checkmate"

        elif GameRules.is_stalemate(self.board, self.turn):
            self.game_over = True
            self.result = "draw by stalemate"