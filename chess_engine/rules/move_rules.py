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
                    initial = Square(row, col)
                    final = Square(
                        possible_move_row,
                        col,
                        square.piece
                    )
                    move = Move(initial, final)

                    moves.append(move)

                else: break 

            else: break 

        # CAPTURED 
        possible_move_row = row + piece.dir 
        possible_move_cols = [col-1, col+1]
        for possible_move_col in possible_move_cols:
            if Square.in_range(possible_move_row, possible_move_col):
                square = board.squares[possible_move_row][possible_move_col]
                if square.has_enemy_piece(piece.color):
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