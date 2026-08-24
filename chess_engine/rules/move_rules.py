from chess_engine.piece import Pawn, Knight, Bishop, Rook, Queen, King
from chess_engine.square import Square
from chess_engine.move import Move


class MoveRules:


    @staticmethod
    def get_moves(board, row, col, piece):

        if isinstance(piece, Pawn):
            return MoveRules.pawn_moves(board, row, col, piece)

        elif isinstance(piece, Knight):
            return MoveRules.knight_moves(board, row, col, piece)

        elif isinstance(piece, Bishop):
            return MoveRules.bishop_moves(board, row, col, piece)

        elif isinstance(piece, Rook):
            return MoveRules.rook_moves(board, row, col, piece)

        elif isinstance(piece, Queen):
            return MoveRules.queen_moves(board, row, col, piece)

        elif isinstance(piece, King):
            return MoveRules.king_moves(board, row, col, piece)


    @staticmethod
    def pawn_moves(board, row, col, piece):

        moves = []

        steps = 1 if piece.moved else 2 
        # MOVE FORWARD
        start = row + piece.dir 
        end = row + (piece.dir * (1 + steps))

        for possible_move_row in range(start, end, piece.dir):
            if Square.in_range(possible_move_row):
                square = board.squares[possible_move_row][col]
                if square.is_empty():

                    MoveRules.add_pawn_move(
                        moves, row, col, possible_move_row, col, piece
                    )

                else: break 

            else: break 

        # CAPTURED 
        possible_move_row = row + piece.dir 
        possible_move_cols = [col-1, col+1]
        for possible_move_col in possible_move_cols:
            if Square.in_range(possible_move_row, possible_move_col):
                square = board.squares[possible_move_row][possible_move_col]
                if square.has_enemy_piece(piece.color):

                    MoveRules.add_pawn_move(
                        moves, row, col, possible_move_row, possible_move_col, piece
                    )

        # EN PASSANT
        MoveRules.add_en_passant_moves(
            board, row, col, piece, moves
        )

        return moves


    @staticmethod
    def add_pawn_move(moves, row, col, final_row, final_col, piece, captured_piece=None):

        initial = Square(row, col)
        final = Square(
            final_row, final_col, captured_piece
        )

        # white row 0
        # black row 7 
        promotion_row = (
            final_row == 0 if piece.color == "white"
            else final_row == 7
        )

        if promotion_row:

            for promotion in (
                "queen", "rook", "bishop", "knight"
            ):
                moves.append(
                    Move(initial, final, promotion)
                )

        else:
            moves.append(Move(initial, final))



    @staticmethod
    def add_en_passant_moves(board, row, col, piece, moves):

        # Không có nước đi trước đó
        if board.last_move is None:
            return

        last_move = board.last_move

        last_initial = last_move.initial
        last_final = last_move.final

        # Quân vừa đi
        last_piece = board.squares[
            last_final.row
        ][
            last_final.col
        ].piece

        # 1. Quân vừa đi phải là Pawn
        if not isinstance(last_piece, Pawn):
            return

        # 2. Phải là Pawn đối phương
        if last_piece.color == piece.color:
            return

        # 3. Pawn đó phải vừa đi 2 ô
        if abs(last_final.row - last_initial.row) != 2:
            return

        # 4. Pawn đó phải đang đứng cùng hàng với Pawn hiện tại
        if last_final.row != row:
            return

        # 5. Pawn đó phải đứng ngay cạnh
        if abs(last_final.col - col) != 1:
            return

        # 6. Ô đích của en passant
        target_row = row + piece.dir
        target_col = last_final.col

        # 7. Ô đích phải nằm trong bàn cờ
        if not Square.in_range(target_row, target_col):
            return

        # 8. Ô đích bắt buộc phải trống
        target_square = board.squares[target_row][target_col]

        if not target_square.is_empty():
            return

        # Tạo nước en passant
        moves.append(
            Move(
                Square(row, col),
                Square(target_row, target_col),
                is_en_passant=True
            )
        )


    @staticmethod
    def knight_moves(board, row, col, piece):

        moves = []

        possible_moves = [
            (row-2, col+1),
            (row-1, col+2),
            (row+1, col+2),
            (row+2, col+1),
            (row+2, col-1),
            (row+1, col-2),
            (row-1, col-2),
            (row-2, col-1),
        ]

        for possible_move in possible_moves:
            possible_move_row, possible_move_col = possible_move

            if Square.in_range(possible_move_row, possible_move_col):
                square = board.squares[possible_move_row][possible_move_col]
                if square.isempty_or_enemy(piece.color):
                    initial = Square(row, col)
                    final = Square(
                        possible_move_row,
                        possible_move_col,
                        square.piece
                    )
                    move = Move(initial, final)

                    moves.append(move)

        return moves


    @staticmethod
    def straightline_moves(board, row, col, piece, incrs):

        moves = []

        for incr in incrs:
            row_incr, col_incr = incr
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr

            while Square.in_range(possible_move_row, possible_move_col):

                square = board.squares[possible_move_row][possible_move_col]
                initial = Square(row, col)
                final = Square(
                    possible_move_row,
                    possible_move_col,
                    square.piece
                )
                move = Move(initial, final)

                if square.is_empty():
                    moves.append(move)
                elif square.has_enemy_piece(piece.color):
                    moves.append(move)
                    break
                else:
                    break

                possible_move_row = possible_move_row + row_incr
                possible_move_col = possible_move_col + col_incr


        return moves


    @staticmethod
    def bishop_moves(board, row, col, piece):
        return MoveRules.straightline_moves(
            board, row, col, piece,
            [
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ]
        )


    @staticmethod
    def rook_moves(board, row, col, piece):
        return MoveRules.straightline_moves(
            board, row, col, piece,
            [
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ]
        )


    @staticmethod
    def queen_moves(board, row, col, piece):
        return MoveRules.straightline_moves(
            board, row, col, piece,
            [
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ]
        )


    @staticmethod
    def king_moves(board, row, col, piece):

        moves = []

        adjs = [
            (row-1, col+0), # up
            (row-1, col+1), # up-right
            (row+0, col+1), # right
            (row+1, col+1), # down-right
            (row+1, col+0), # down
            (row+1, col-1), # down-left
            (row+0, col-1), # left
            (row-1, col-1), # up-left
        ]

        for possible_move in adjs:
            possible_move_row, possible_move_col = possible_move

            if Square.in_range(possible_move_row, possible_move_col):
                square = board.squares[possible_move_row][possible_move_col]
                if square.isempty_or_enemy(piece.color):
                    initial = Square(row, col)
                    final = Square(
                        possible_move_row,
                        possible_move_col,
                        square.piece
                    )
                    move = Move(initial, final)

                    moves.append(move)

        return moves