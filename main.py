#import pygames loads the Pygame library into my program.
#import sys loads the system module in Python.
import pygame
import sys

from board import Board
from game_logic import Piece
import board
in_bounds = board.in_bounds

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



def opponent(color):
    return "black" if color  =="red" else "red"


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

    if highlights:
        for r, c in highlights:
            pygame.draw.circle(
                WIN,
                HIGHLIGHT,
                (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                 r * SQUARE_SIZE + SQUARE_SIZE // 2),
                SQUARE_SIZE // 6,
            )

    for r in range(ROWS):
        for c in range(COLS):
            piece = board.get(r, c)
            if piece:
                color = RED if piece.color  =="red" else BLACK
                pygame.draw.circle(
                    WIN,
                    color,
                    (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                     r * SQUARE_SIZE + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 2 - 8,
                )

                if piece.king:
                    k_text = FONT.render("K", True, WHITE)
                    WIN.blit(
                        k_text,
                        (
                            c * SQUARE_SIZE + SQUARE_SIZE // 2 - 8,
                            r * SQUARE_SIZE + SQUARE_SIZE // 2 - 14,
                        ),
                    )

    if selected_piece:
        pygame.draw.rect(
            WIN,
            SELECT_COLOR,
            (
                selected_piece.col * SQUARE_SIZE,
                selected_piece.row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            ),
            4,
        )

def get_square(pos):
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
