#class Board is a blueprint (model) for the entire checkers board.

from game_logic import Piece

ROWS, COLS = 8, 8

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS
'''This function returns the other player's color. 
     If the input is "red" → it returns "black"
     If the input is "black" → it returns "red"'''

class Board:
    '''This is the constructor of the Board class.
       It runs automatically when a new board is created.'''
    def __init__(self):#__init__ is a special function in Python that automatically runs whenever you create an object from a class.
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.setup()
    ''''''
    def setup(self):
          # Sets up the board at the start of the game by placing red and black pieces
    # in their standard positions on the dark squares.

        for r in range(ROWS):
            for c in range(COLS):
                if (r + c) % 2  ==1:
                    if r < 3:
                        self.grid[r][c] = Piece(r, c, "black")
                    elif r > 4:
                        self.grid[r][c] = Piece(r, c, "red")

    def get(self, r, c):
        # Sets up the board for a new game by placing red and black pieces
    # on the correct dark squares in the starting rows.

        return self.grid[r][c] if in_bounds(r, c) else None

    def set(self, r, c, piece):
          # Puts a piece on the board at row r and column c and updates its position.
        if in_bounds(r, c):
            self.grid[r][c] = piece
            if piece:
                piece.row = r
                piece.col = c

    def remove(self, r, c):
         # Clears the square at (r, c) by removing the piece there.
    # Used during captures or when a piece is moved.
        if in_bounds(r, c):
            self.grid[r][c] = None

    def move_piece(self, piece, r, c):
        # Moves the piece to the new location and checks if it should be promoted to a king.

        self.remove(piece.row, piece.col)
        self.set(r, c, piece)

        if piece.color  =="red" and r  ==0:
            piece.make_king()
        if piece.color  =="black" and r  ==ROWS - 1:
            piece.make_king()
