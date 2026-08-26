class Dragger:

    def __init__(self):

        self.dragging = False

        self.initial_row = None
        self.initial_col = None

        self.piece = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.legal_moves = []


    def start_drag(self, row, col, piece, 
                   mouse_x, mouse_y, legal_moves):

        self.dragging = True

        self.initial_row = row
        self.initial_col = col

        self.piece = piece

        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        self.legal_moves = legal_moves


    def update_mouse(self, mouse_x, mouse_y):

        if not self.dragging:
            return

        self.mouse_x = mouse_x
        self.mouse_y = mouse_y


    def stop_drag(self):

        self.dragging = False

        self.initial_row = None
        self.initial_col = None

        self.piece = None

        self.legal_moves = []