from chess_engine.board import Board
from chess_engine.square import Square
from chess_engine.move import Move


def main():
    board = Board()

    print("BEFORE:")
    board.print_board()

    initial = Square(6, 4)
    final = Square(4, 4)

    move = Move(initial, final)

    board.move(move)

    print("\nAFTER:")
    board.print_board()


if __name__ == "__main__":
    main()