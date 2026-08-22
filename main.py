from chess_engine.square import Square
from chess_engine.move import Move


def main():
    move1 = Move(
        Square(6, 4),
        Square(4, 4)
    )

    move2 = Move(
        Square(6, 4),
        Square(4, 4)
    )

    print(move1 == move2)


if __name__ == "__main__":
    main()