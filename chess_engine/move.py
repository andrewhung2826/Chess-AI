


class Move:

    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
 

    def __eq__(self, other):
        return (
            self.initial.row == other.initial.row
            and self.initial.col == other.initial.col
            and self.final.row == other.final.row
            and self.final.col == other.final.col
        )