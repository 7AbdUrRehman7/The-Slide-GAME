"""CSCA08H: Functions for the Slide single-player game.

Instructions (READ THIS FIRST!)
===============================

Make sure that the file slide_game.py is in the same directory as this file.

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students
taking the CSCA08 course at the University of Toronto Scarborough. Copying for
purposes other than this use is expressly prohibited. All forms of distribution
of this code, whether as given or with any changes, are expressly prohibited.

"""

# The next several lines contain constants for you to use in your code.
# You must use these constants instead of the values they refer to.
# For example, use BLACK_SQUARE instead of '#'.
# You may not need to use all of the constants provided.
# Do not change the values these constants refer to.

N_COLUMNS = 5             # Number of columns in the game board
N_ROWS = 4                 # Number of rows in the game board

BLACK_SQUARE = '#'         # The character that represents a black square
RED_SQUARE = 'R'           # The character that represents a red square
YELLOW_SQUARE = 'Y'        # The character that represents a blue square

ACROSS = 'across'          # The horizontal direction
DOWN = 'down'              # The vertical direction
DOWN_RIGHT = 'dright'      # The diagonal direction: downward and rightward
DOWN_LEFT = 'dleft'        # The diagonal direction: downward and leftward


# This function is completed for you as an example and you must not change it.
def create_empty_board() -> str:
    """Return a string representation of a game board of all empty symbols with
    N_ROWS rows and N_COLUMNS columns.
    """
    return BLACK_SQUARE * N_ROWS * N_COLUMNS


def is_board_full(game_board: str) -> bool:
    """Return True if and only if the game_board is full.

    A game_board is full when it does not contain any BLACK_SQUARE characters.

    >>> is_board_full('R########YR####Y####')
    False
    >>> is_board_full('RYYRYYRYYRYYRYYRYYRY')
    True
    """
    return BLACK_SQUARE not in game_board


def between(value: str, min_value: int, max_value: int) -> bool:
    """Return True if and only if value is between min_value and max_value,
    inclusive.

    Preconditions:
        - value can be converted to an integer without error
        - min_value <= max_value

    >>> between('2', 0, 2)
    True
    >>> between('0', 2, 3)
    False
    """
    return min_value <= int(value) <= max_value


def calculate_str_index(row: int, col: int) -> int:
    """Return an index of integer type that corresponts to the location of
    the given row as spesified by row and column as spesified by col.

    >>> calculate_str_index(3, 2)
    11
    >>> calculate_str_index(1, 5)
    4
    """
    return (row - 1) * N_COLUMNS + (col - 1)


def calculate_increment(direction: str) -> int:
    """Return an integer that represents difference between the string
    indices of two adjacent squares on a line that goes in  spesefied
    direction.

    Preconditions:
        - string value should be either DOWN, ACROSS, DOWN_RIGHT, or DWON_LEFT.
        - Grid specified by number of rows by number of columns.

    >>> calculate_increment('down')
    5
    >>> calculate_increment('across')
    1
    >>> calculate_increment('down_right')
    6
    >>> calculate_increment('down_left')
    4
    """
    if direction == DOWN:
        return N_COLUMNS
    elif direction == ACROSS:
        return 1
    elif direction == DOWN_RIGHT:
        return N_COLUMNS + 1
    return N_COLUMNS - 1


def get_row(row_num: int, game_board: str) -> str:
    """Return a string of the row_num row from the game_board game board.

    precondition:
        - row number and game board must be valid.

    >>> get_row(1, 'ABCDEFGHIJKLMNOPQRST')
    'ABCDE'
    >>> get_row(2, 'ABCDEFGHIJKLMNOPQRST')
    'FGHIJ'
    >>> get_row(3, 'ABCDEFGHIJKLMNOPQRST')
    'KLMNO'
    >>> get_row(2, 'HIJKLMNOPQRST')
    'MNOPQ'
    >>> get_row(5, 'ABCDEFGHIJKLMNOPQRST')
    ''
    """
    return game_board[(row_num - 1) * N_COLUMNS:row_num * N_COLUMNS]


def get_column(col_num: int, game_board: str) -> str:
    """Return a string of the col_num column from the game_board game board.

    precondition:
        - column number and game board must be valid.

    >>> get_column(3, 'ABCDEFGHIJKLMNOPQRST')
    'CHMR'
    >>> get_column(4, 'ABCDEFGHIJKLMNOPQRST')
    'DINS'
    >>> get_column(5, 'ABCDEFGHIJKLMNOPQRST')
    'EJOT'
    >>> get_column(99, 'ABCDEFGHIJKLMNOPQRST')
    ''
    """
    return game_board[col_num - 1:N_ROWS * N_COLUMNS:N_COLUMNS]


def slide_right(square_added: str, row_num: int, game_board: str) -> str:
    """Return a string of the game_board game board diagram, where
    square_added square slids in the biggining of the assigned row_num row
    and the square at the end slids off the game_board game board.

    preconditions:
        - Square, row number and game board must be valid.

    >>> slide_right('@', 1, 'ABCDEFGHIJKLMNOPQRST')
    '@ABCDFGHIJKLMNOPQRST'
    >>> slide_right('', 4, 'ABCDEFGHIJKLMNOPQRST')
    'ABCDEFGHIJKLMNOPQRST'
    >>> slide_right('$', 2, 'ABCDEFGHIJKLMNO')
    'ABCDE$FGHIKLMNO'
    """
    if square_added != '':
        return (game_board[0:(row_num - 1) * N_COLUMNS] + square_added +
                game_board[(row_num - 1) * N_COLUMNS:
                           (row_num * N_COLUMNS) - 1] +
                game_board[(row_num * N_COLUMNS):])
    return game_board


def slide_left(square_added: str, row_num: int, game_board: str) -> str:
    """Return a string of the game_board game board diagram, where
    square_added square slids in the end of the assigned row_num row
    and the square at the biggining slids off the game_board game board.

    preconditions:
        - Square, row number and game board must be valid.

     >>> slide_left('@', 1, 'ABCDEFGHIJKLMNOPQRST')
    'BCDE@FGHIJKLMNOPQRST'
    >>> slide_left('', 4, 'ABCDEFGHIJKLMNOPQRST')
    'ABCDEFGHIJKLMNOPQRST'
    >>> slide_left('$', 2, 'ABCDEFGHIJKLMNO')
    'ABCDEGHIJ$KLMNO'
    """
    if square_added != '':
        return (game_board[0:(row_num - 1) * N_COLUMNS] +
                game_board[((row_num - 1) * N_COLUMNS) + 1:
                           row_num * N_COLUMNS] + square_added +
                game_board[row_num * N_COLUMNS:])
    return game_board