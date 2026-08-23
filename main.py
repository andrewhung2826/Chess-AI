from chess_engine.game_state import GameState
from chess_engine.square import Square
from chess_engine.move import Move


def main():
    game = GameState()

    print("TURN:", game.turn)

    # e2 -> e4
    move = Move(
        Square(6, 4),
        Square(4, 4)
    )

    success = game.make_move(move)

    print("MOVE SUCCESS:", success)
    print("TURN:", game.turn)

    game.board.print_board()


if __name__ == "__main__":
    main()