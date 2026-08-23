from .move_rules import MoveRules
from chess_engine.piece import King
from chess_engine.const import ROWS, COLS


class CheckRules:

    @staticmethod
    def is_check(board, color):

        king = None
        king_row = None
        king_col = None 

        for row in range(ROWS):
            for col in range(COLS):

                piece = board.squares[row][col].piece

                if isinstance(piece, King) and piece.color == color:
                    king = piece
                    king_row = row 
                    king_col = col 
                    break 

            if king:
                break 

        if king is None:
            return False


        # Kiem tra quan dich
        for row in range(ROWS):
            for col in range(COLS):

                piece = board.squares[row][col].piece

                if piece and piece.color != color:

                    enemy_moves = MoveRules.get_moves(board, row, col, piece)

                    for move in enemy_moves:
                        if (
                            move.final.row == king_row and 
                            move.final.col == king_col 
                        ):
                            return True 

        return False


    @staticmethod
    def filter_legal_moves(board, piece, moves):

        legal_moves = []

        for move in moves:

            initial = move.initial
            final = move.final 

            captured_piece = board.squares[final.row][final.col].piece 

            # MAKE MOVE
            board.squares[initial.row][initial.col].piece = None 
            board.squares[final.row][final.col].piece = piece 

            # CHECK
            in_check = CheckRules.is_check(board, piece.color)

            # UNMAKE MOVE 
            board.squares[initial.row][initial.col].piece = piece
            board.squares[final.row][final.col].piece = captured_piece

            # LEGAL MOVE
            if not in_check:
                legal_moves.append(move)

        return legal_moves