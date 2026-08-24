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

            initial_square = board.squares[initial.row][initial.col]
            final_square = board.squares[final.row][final.col]

            captured_piece = board.squares[final.row][final.col].piece 

            en_passant_piece = None

            if move.is_en_passant:

                en_passant_square = board.squares[initial.row][final.col]

                en_passant_piece = en_passant_square.piece


            # MAKE MOVE
            initial_square.piece = None

            if move.is_en_passant:
                board.squares[initial.row][final.col].piece = None

            # PROMOTION
            moved_piece = piece 
            if move.promotion is not None:
                moved_piece = board.promotion_pawn(move, piece)

            final_square.piece = moved_piece

            # CHECK
            in_check = CheckRules.is_check(board, piece.color)

            # UNMAKE MOVE 
            initial_square.piece = piece
            final_square.piece = captured_piece

            if move.is_en_passant:
                board.squares[initial.row][final.col].piece = en_passant_piece

            # LEGAL MOVE
            if not in_check:
                legal_moves.append(move)

        return legal_moves