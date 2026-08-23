from .move_rules import MoveRules
from .check_rules import CheckRules

from chess_engine.const import ROWS, COLS 



class GameRules:

    @staticmethod
    def has_legal_moves(board, color):

        for row in range(ROWS):
            for col in range(COLS):

                square = board.squares[row][col]

                if square.is_empty():
                    continue

                piece = square.piece 

                if piece.color != color:
                    continue

                moves = MoveRules.get_moves(
                    board, row, col, piece 
                )

                legal_moves = CheckRules.filter_legal_moves(
                    board, piece, moves 
                )

                if legal_moves:
                    return True 

        return False


    @staticmethod
    def is_checkmate(board, color):
        if not CheckRules.is_check(board, color):
            return False

        return not GameRules.has_legal_moves(board, color)


    @staticmethod
    def is_stalemate(board, color):

        if CheckRules.is_check(board, color):
            return False

        return not GameRules.has_legal_moves(board, color)