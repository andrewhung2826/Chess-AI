from pathlib import Path
import pygame

from chess_engine.const import ROWS, COLS, SQSIZE



class BoardView:

    def __init__(self):

        self.piece_images = {}
        self.drag_piece_images = {}

        self.load_piece_images()


    def load_piece_images(self):

            project_root = Path(__file__).resolve().parent.parent

            normal_path = (project_root/ "assets"/ "images"/ "imgs-80px")

            drag_path = (project_root/ "assets"/ "images"/ "imgs-128px")

            colors = ["white", "black"]

            pieces = [
                "pawn",
                "knight",
                "bishop",
                "rook",
                "queen",
                "king"
            ]

            for color in colors:
                for piece in pieces:

                    key = f"{color}_{piece}"

                    # Ảnh bình thường
                    self.piece_images[key] = (
                        pygame.image.load(normal_path / f"{key}.png").convert_alpha()
                    )

                    # Ảnh khi kéo
                    self.drag_piece_images[key] = (
                        pygame.image.load(drag_path / f"{key}.png").convert_alpha()
                    )


    def draw_board(self, screen):

        for row in range(ROWS):
            for col in range(COLS):

                rect = pygame.Rect(
                    col * SQSIZE,
                    row * SQSIZE,
                    SQSIZE,
                    SQSIZE
                )

                color = (
                    (235, 236, 208)
                    if (row + col) % 2 == 0
                    else (119, 149, 86)
                )

                pygame.draw.rect(screen, color, rect)


    def draw_pieces(self, screen, board, dragger=None):

        for row in range(ROWS):
            for col in range(COLS):

                piece = board.squares[row][col].piece

                if piece is None:
                    continue

                # Không vẽ quân đang được kéo
                if (
                    dragger is not None
                    and dragger.dragging
                    and row == dragger.initial_row
                    and col == dragger.initial_col
                ):
                    continue

                key = (f"{piece.color}_"f"{piece.name.lower()}")

                image = self.piece_images[key]

                x = (
                    col * SQSIZE
                    + (SQSIZE - image.get_width()) // 2
                )

                y = (
                    row * SQSIZE
                    + (SQSIZE - image.get_height()) // 2
                )

                screen.blit(image, (x, y))


    def draw_dragged_piece(self, screen, dragger):

        if not dragger.dragging:
            return

        piece = dragger.piece

        if piece is None:
            return

        key = (f"{piece.color}_"f"{piece.name.lower()}")

        image = self.drag_piece_images[key]

        x = (
            dragger.mouse_x
            - image.get_width() // 2
        )

        y = (
            dragger.mouse_y
            - image.get_height() // 2
        )

        screen.blit(image, (x, y))


    def draw_legal_moves(self, screen, board, dragger):

        if not dragger.dragging:
            return

        for move in dragger.legal_moves:

            final = move.final

            square = board.squares[final.row][final.col]

            center = (
                final.col * SQSIZE
                + SQSIZE // 2,

                final.row * SQSIZE
                + SQSIZE // 2
            )

            is_capture = (
                square.piece is not None
                or move.is_en_passant
            )

            if is_capture:

                pygame.draw.circle(
                    screen,
                    (60, 60, 60),
                    center,
                    SQSIZE // 2 - 8,
                    width=6
                )

            # Nước đi thường
            else:

                pygame.draw.circle(
                    screen,
                    (60, 60, 60),
                    center,
                    SQSIZE // 8
                )


    def draw_game_over(self, screen, game_state):

        if not game_state.game_over:
            return

        # Lớp nền tối
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 150))

        screen.blit(overlay,(0, 0))

        # Fonts
        title_font = pygame.font.SysFont("Arial",45,bold=True)

        result_font = pygame.font.SysFont("Arial",28)

        # Checkmate
        if "checkmate" in game_state.result:

            title = "CHECKMATE"

            winner = game_state.result.split()[0]

            result = f"{winner.upper()} WINS"

        # Stalemate
        elif "stalemate" in game_state.result:

            title = "STALEMATE"
            result = "DRAW"

        else:
            title = "GAME OVER"
            result = game_state.result.upper()

        # Render text
        title_surface = title_font.render(
            title,
            True,
            (255, 255, 255)
        )

        result_surface = result_font.render(
            result,
            True,
            (255, 255, 255)
        )

        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        title_rect = title_surface.get_rect(
            center=(center_x, center_y - 30)
        )

        result_rect = result_surface.get_rect(
            center=(center_x, center_y + 30)
        )

        screen.blit(title_surface, title_rect)

        screen.blit(result_surface, result_rect)


    def draw_coordinates(self, screen):

        font = pygame.font.SysFont("Arial", 18, bold=True)

        files = "abcdefgh"

        # Vẽ a, b, c, ..., h
        for col in range(COLS):

            text = files[col]

            text_surface = font.render(text,True,(40, 40, 40))

            x = col * SQSIZE + SQSIZE - 18

            y = ROWS * SQSIZE- 25

            screen.blit(text_surface, (x, y))

        # Vẽ 8, 7, 6, ..., 1
        for row in range(ROWS):

            text = str(ROWS - row)

            text_surface = font.render(text, True, (40, 40, 40))

            x = 5

            y = row * SQSIZE + 5

            screen.blit(text_surface,(x, y))


    def draw_promotion_menu(self, screen, color):

        promotion_pieces = [
            "queen",
            "rook",
            "bishop",
            "knight"
        ]

        menu_width = SQSIZE
        menu_height = SQSIZE * 4

        # Đặt menu ở giữa màn hình
        x = (
            screen.get_width() - menu_width
        ) // 2

        y = (
            screen.get_height() - menu_height
        ) // 2

        # Nền menu
        menu_rect = pygame.Rect(
            x,
            y,
            menu_width,
            menu_height
        )

        pygame.draw.rect(
            screen,
            (50, 50, 50),
            menu_rect
        )

        for index, piece_name in enumerate(
            promotion_pieces
        ):

            rect = pygame.Rect(
                x,
                y + index * SQSIZE,
                SQSIZE,
                SQSIZE
            )

            # Nền từng lựa chọn
            pygame.draw.rect(
                screen,
                (230, 230, 230),
                rect
            )

            key = f"{color}_{piece_name}"

            image = self.piece_images[key]

            image_x = (
                rect.x
                + (rect.width - image.get_width()) // 2
            )

            image_y = (
                rect.y
                + (rect.height - image.get_height()) // 2
            )

            screen.blit(image, (image_x, image_y))


    def get_promotion_choice(
        self,
        pos,
        screen
    ):

        promotion_pieces = [
            "queen",
            "rook",
            "bishop",
            "knight"
        ]

        menu_width = SQSIZE
        menu_height = SQSIZE * 4

        x = (
            screen.get_width() - menu_width
        ) // 2

        y = (
            screen.get_height() - menu_height
        ) // 2

        mouse_x, mouse_y = pos

        menu_rect = pygame.Rect(
            x,
            y,
            menu_width,
            menu_height
        )

        if not menu_rect.collidepoint(
            mouse_x,
            mouse_y
        ):
            return None

        index = (
            mouse_y - y
        ) // SQSIZE

        return promotion_pieces[index]