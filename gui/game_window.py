import pygame
from pathlib import Path

from chess_engine.const import *
from chess_engine.game_state import GameState

from .board_view import BoardView
from .dragger import Dragger


class GameWindow:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Chess AI")

        self.clock = pygame.time.Clock()

        # ENGINE
        self.game_state = GameState()

        # GUI
        self.board_view = BoardView()

        self.dragger = Dragger()

        self.pending_promotion_moves = []

        self.running = True

        project_root = Path(__file__).resolve().parent.parent

        sound_path = (project_root/ "assets"/ "sounds")

        self.move_sound = pygame.mixer.Sound(sound_path / "move.wav")

        self.capture_sound = pygame.mixer.Sound(sound_path / "capture.wav")



    def is_capture_move(self, move):

        final_square = self.game_state.board.squares[move.final.row][move.final.col]

        return final_square.piece is not None or move.is_en_passant
        


    def play_move_sound(self, is_capture):

        if is_capture:
            self.capture_sound.play()
        else:
            self.move_sound.play()


    def get_square_from_mouse(self, pos):

        mouse_x, mouse_y = pos

        col = mouse_x // SQSIZE
        row = mouse_y //SQSIZE

        return row, col


    def handle_mouse_down(self, pos):

        if self.pending_promotion_moves:

            self.handle_promotion_click(pos)
            return

        row, col = self.get_square_from_mouse(pos)

        square = self.game_state.board.squares[row][col]

        if square.is_empty():
            return

        piece = square.piece

        if piece.color != self.game_state.turn:
            return

        # ENGINE tính legal moves
        legal_moves = self.game_state.get_legal_moves(row, col)

        mouse_x, mouse_y = pos

        # GUI chỉ lưu kết quả
        self.dragger.start_drag(row, col, piece,
                                mouse_x, mouse_y, legal_moves)


    def handle_mouse_up(self, pos):

        if not self.dragger.dragging:
            return

        row, col = self.get_square_from_mouse(pos)

        matching_moves = []

        for move in self.dragger.legal_moves:

            if (
                move.final.row == row
                and move.final.col == col
            ):
                matching_moves.append(move)

        # Không có nước đi hợp lệ
        if not matching_moves:

            self.dragger.stop_drag()
            return

        # Promotion: có nhiều lựa chọn cùng một ô đích
        promotion_moves = [
            move
            for move in matching_moves
            if move.promotion is not None
        ]

        if promotion_moves:

            self.pending_promotion_moves = promotion_moves

            self.dragger.stop_drag()

            return

        # Nước đi bình thường
        selected_move = matching_moves[0]

        is_capture = self.is_capture_move(
            selected_move
        )

        moved = self.game_state.make_move(
            selected_move
        )

        if moved:
            self.play_move_sound(is_capture)

        self.dragger.stop_drag()


    def handle_promotion_click(self, pos):

        promotion = self.board_view.get_promotion_choice(pos, self.screen)

        if promotion is None:
            return

        for move in self.pending_promotion_moves:

            if move.promotion == promotion:

                is_capture = self.is_capture_move(move)

                moved = self.game_state.make_move(move)

                if moved:
                    self.play_move_sound(is_capture)

                break

        self.pending_promotion_moves = []


    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.pending_promotion_moves:

                    self.handle_promotion_click(event.pos)
                    continue

                if event.button == 1:

                    self.handle_mouse_down(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:

                    self.handle_mouse_up(event.pos)

            elif event.type == pygame.MOUSEMOTION:

                if self.dragger.dragging:

                    self.dragger.update_mouse(event.pos[0], event.pos[1])


    def draw(self):

        self.board_view.draw_board(self.screen)

        self.board_view.draw_last_move(self.screen, self.game_state)

        self.board_view.draw_check(self.screen, self.game_state.board, self.game_state.turn)

        self.board_view.draw_coordinates(self.screen)

        self.board_view.draw_legal_moves(self.screen, self.game_state.board, self.dragger)

        self.board_view.draw_pieces(self.screen, self.game_state.board, self.dragger)

        self.board_view.draw_dragged_piece(self.screen, self.dragger)

        self.board_view.draw_move_history(self.screen, self.game_state.move_history)

        self.board_view.draw_game_over(self.screen, self.game_state)

        if self.pending_promotion_moves:
            self.board_view.draw_promotion_menu(self.screen, self.game_state.turn)

        pygame.display.flip()


    def run(self):

        while self.running:

            self.handle_events()

            self.draw()

            self.clock.tick(60)

        pygame.quit()