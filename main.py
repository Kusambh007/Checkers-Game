#import pygames loads the Pygame library into my program.
#import sys loads the system module in Python.
import pygame
import sys

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
#this is for the colours 
WHITE = (245, 245, 245)
DARK_SQ = (102, 51, 0)
LIGHT_SQ = (230, 200, 160)
RED = (230, 40, 40)
BLACK = (10, 10, 10)

HIGHLIGHT = (255, 215, 0)
SELECT_COLOR = (0, 200, 200)
#pygame.init() starts (initializes) all the important modules of Pygame.
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))#This lines creates the game window.
pygame.display.set_caption("Checkers (capture = extra turn)")
FONT = pygame.font.SysFont("consolas", 24)
#These four variables represent movement directions on the board for a checker piece.
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DN_LEFT = (1, -1)
DN_RIGHT = (1, 1)
#This function checks whether a given row (r) and column (c) are inside the board.
def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS
'''This function returns the other player's color. 
     If the input is "red" → it returns "black"
     If the input is "black" → it returns "red"'''
def opponent(color):
    return "black" if color  =="red" else "red"
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
#class Board is a blueprint (model) for the entire checkers board.
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

def normal_moves(board, piece):
        # Calculates all regular moves for the piece (moving one diagonal square)
    # based on its color or king status.
    moves = []

    if piece.king:
        directions = [UP_LEFT, UP_RIGHT, DN_LEFT, DN_RIGHT]
    else:

        directions = [UP_LEFT, UP_RIGHT] if piece.color  =="red" else [DN_LEFT, DN_RIGHT]

    for dr, dc in directions:
        nr = piece.row + dr
        nc = piece.col + dc
        if in_bounds(nr, nc) and board.get(nr, nc) is None:
            moves.append((nr, nc))

    return moves

def capture_moves(board, piece):
     # Calculates all capture (jump) moves for the piece by checking if it can
    # jump over an opponent and land on an empty square.
    jumps = []

    if piece.king:
        directions = [UP_LEFT, UP_RIGHT, DN_LEFT, DN_RIGHT]
    else:
        directions = [UP_LEFT, UP_RIGHT] if piece.color  =="red" else [DN_LEFT, DN_RIGHT]

    for dr, dc in directions:
        mid_r = piece.row + dr
        mid_c = piece.col + dc
        land_r = piece.row + 2 * dr
        land_c = piece.col + 2 * dc

        if (
            in_bounds(mid_r, mid_c)
            and in_bounds(land_r, land_c)
            and board.get(mid_r, mid_c)
            and board.get(mid_r, mid_c).color  ==opponent(piece.color)
            and board.get(land_r, land_c) is None
        ):

            jumps.append((land_r, land_c, mid_r, mid_c))

    return jumps

def draw_board():
    # Draws the full checkers board, alternating light and dark squares
    # to create the standard board pattern.
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT_SQ if (r + c) % 2  ==0 else DARK_SQ
            pygame.draw.rect(
                WIN,
                color,
                (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

def draw_pieces(board, selected_piece=None, highlights=None):
     # Renders every piece on the board and displays visual markers
    # for selected pieces and possible moves.
     # Converts screen pixel coordinates into board coordinates by determining
    # which row and column the user clicked based on square size.
    item, output = pos
    row = output // SQUARE_SIZE
    col = item // SQUARE_SIZE
    return row, col


def main():
    # The core game loop that manages user input, piece selection, moves,
    # turn switching, board updates, and continuously redraws the game screen.
    clock = pygame.time.Clock()
    board = Board()
    turn = "red"
    selected = None
    highlights = []
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():# Loops through all events (mouse clicks, key presses, window close, etc.)
            if event.type  ==pygame.QUIT:
                running = False
                break

            if event.type  ==pygame.MOUSEBUTTONDOWN:# Checks if the player clicked the mouse.
                r, c = get_square(event.pos)
                piece = board.get(r, c)

                if selected:

                    if (r, c) in highlights:
                        capture_happened = False

                        for move in capture_moves(board, selected):
                            if move[0]  ==r and move[1]  ==c:
                                board.remove(move[2], move[3])
                                capture_happened = True
                                break

                        board.move_piece(selected, r, c)

                        if capture_happened:

                            selected = None
                            highlights = []
                        else:

                            selected = None
                            highlights = []
                            turn = opponent(turn)
                    else:

                        selected = None
                        highlights = []
                else:

                    if piece and piece.color  ==turn:
                        selected = piece
                        cap_moves = capture_moves(board, piece)
                        cap_lands = [(maximum[0], maximum[1]) for maximum in cap_moves]
                        highlights = normal_moves(board, piece) + cap_lands

        draw_board()
        draw_pieces(board, selected, highlights)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__  =="__main__":
    main()
