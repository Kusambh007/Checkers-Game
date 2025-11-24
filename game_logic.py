#class Piece is a blueprint (model) for a single checker piece on the board.
class Piece:
    '''This is the constructor of the Piece class.
       Whenever I create a new piece, this function runs automatically.'''
    def __init__(self, r, c, color, king=False):
        self.row = r
        self.col = c
        self.color = color
        self.king = king
    '''This function promotes a normal checker piece into a king.
       When a piece reaches the opposite side of the board, this function is called.'''
    def make_king(self):
        self.king = True