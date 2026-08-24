


class Move:

    def __init__(self, initial, final, 
                 promotion=None, is_en_passant=False):
        self.initial = initial
        self.final = final
        self.promotion = promotion
        self.is_en_passant = is_en_passant
 

    def __eq__(self, other):
        return (
            isinstance(other, Move)
            and self.initial == other.initial
            and self.final == other.final
            and self.promotion == other.promotion
            and self.is_en_passant == other.is_en_passant
        )