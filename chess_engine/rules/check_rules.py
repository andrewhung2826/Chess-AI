from .move_rules import MoveRules
from chess_engine.game.piece import King, Pawn
from chess_engine.game.const import ROWS, COLS


class CheckRules:

    @staticmethod
    def is_check(board, color):

        for row in range(ROWS):
            for col in range(COLS):

                piece = board.squares[row][col].piece

                if (
                    isinstance(piece, King)
                    and piece.color == color
                ):
                    return CheckRules.is_square_attacked(
                        board,
                        row,
                        col,
                        color
                    )

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

            # CASTLING 
            rook = None 
            rook_initial_square = None 
            rook_final_square = None 
            rook_final_piece = None

            if move.is_castling:

                # KINGSIDE
                if final.col > initial.col:
                    rook_initial_square = board.squares[initial.row][7]
                    rook_final_square = board.squares[initial.row][5]
                # QUEENSIDE
                else:
                    rook_initial_square = board.squares[initial.row][0]
                    rook_final_square = board.squares[initial.row][3]

                rook = rook_initial_square.piece 
                rook_piece_square = rook_final_square.piece

            # MAKE MOVE
            initial_square.piece = None

            if move.is_en_passant:
                board.squares[initial.row][final.col].piece = None

            # MOVE KING/ NORMAL PIECE
            final_square.piece = piece 

            # CASTLING ROOK MOVE
            if move.is_castling:
                rook_initial_square.piece = None 
                rook_final_square.piece = rook

            # PROMOTION
            if move.promotion is not None:
                moved_piece = board.promote_pawn(move, piece)

                final_square.piece = moved_piece

            # CHECK
            in_check = CheckRules.is_check(board, piece.color)

            # UNMAKE MOVE 
            initial_square.piece = piece
            final_square.piece = captured_piece

            # RESTORE EN PASSANT
            if move.is_en_passant:
                board.squares[initial.row][final.col].piece = en_passant_piece

            # RESTORE CASTLING ROOK
            if move.is_castling:
                rook_initial_square.piece = rook 
                rook_final_square.piece = rook_final_piece


            # LEGAL MOVE
            if not in_check:
                legal_moves.append(move)

        return legal_moves


    @staticmethod
    def is_square_attacked(board, row, col, color):

        # KIEM TRA SQUARE CO BI DOI PHUONG TAN CONG KHONG

        enemy_color = "black" if color == "white" else "white"

        for enemy_row in range(ROWS):
            for enemy_col in range(COLS):

                piece = board.squares[enemy_row][enemy_col].piece

                if piece is None:
                    continue

                if piece.color != enemy_color:
                    continue

                # PAWN ATTACK
                if isinstance(piece, Pawn):

                    attack_row = enemy_row + piece.dir 

                    if (
                        attack_row == row 
                        and abs(enemy_col - col) == 1
                    ):
                        return True

                    continue

                # OTHER PIECE
                moves = MoveRules.get_moves(
                    board, enemy_row, enemy_col, piece, include_castling=False 
                )

                for move in moves:
                    if (
                        move.final.row == row 
                        and move.final.col == col 
                    ):
                        return True 

        return False