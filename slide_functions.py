"""Independent reimplementation of the slide game helpers.
(No course-provided text or docstrings are copied.)
"""
# Public constants (same values to preserve external behavior)
N_COLUMNS = 5
N_ROWS = 4

BLACK_SQUARE = '#'
RED_SQUARE = 'R'
YELLOW_SQUARE = 'Y'

ACROSS = 'across'
DOWN = 'down'
DOWN_RIGHT = 'dright'
DOWN_LEFT = 'dleft'


def create_empty_board() -> str:
    """Return an N_ROWS x N_COLUMNS board encoded as a flat string of BLACK_SQUARE."""
    return BLACK_SQUARE * (N_ROWS * N_COLUMNS)


def is_board_full(game_board: str) -> bool:
    """Return True iff there is no BLACK_SQUARE on the board."""
    return BLACK_SQUARE not in game_board


def between(value: str, min_value: int, max_value: int) -> bool:
    """Return True iff int(value) lies in [min_value, max_value]."""
    return min_value <= int(value) <= max_value


def calculate_str_index(row: int, col: int) -> int:
    """Map 1-based (row, col) to a 0-based index in the flat board string."""
    return (row - 1) * N_COLUMNS + (col - 1)


def calculate_increment(direction: str) -> int:
    """Return step amount in the flat string for a given direction label."""
    if direction == DOWN:
        return N_COLUMNS
    if direction == ACROSS:
        return 1
    if direction == DOWN_RIGHT:
        return N_COLUMNS + 1
    # default: DOWN_LEFT
    return N_COLUMNS - 1


def _row_bounds(row_num: int) -> tuple[int, int]:
    """Return (start, end) slice bounds for a row (1-based), where end is exclusive."""
    start = (row_num - 1) * N_COLUMNS
    end = row_num * N_COLUMNS
    return start, end


def get_row(row_num: int, game_board: str) -> str:
    """Return the contents of row row_num from game_board."""
    start, end = _row_bounds(row_num)
    return game_board[start:end]


def get_column(col_num: int, game_board: str) -> str:
    """Return the contents of column col_num from game_board."""
    # slice end uses the full logical board extent so short strings work too
    return game_board[col_num - 1:N_ROWS * N_COLUMNS:N_COLUMNS]


def slide_right(square_added: str, row_num: int, game_board: str) -> str:
    """Insert square_added at the left of row row_num, dropping that row's rightmost square."""
    if square_added == '':
        return game_board
    start, end = _row_bounds(row_num)
    row = game_board[start:end]
    new_row = (square_added + row)[:N_COLUMNS]  # keep first N_COLUMNS
    return game_board[:start] + new_row + game_board[end:]


def slide_left(square_added: str, row_num: int, game_board: str) -> str:
    """Append square_added at the right of row row_num, dropping that row's leftmost square."""
    if square_added == '':
        return game_board
    start, end = _row_bounds(row_num)
    row = game_board[start:end]
    new_row = (row + square_added)[1:N_COLUMNS+1]  # drop first, keep N_COLUMNS
    return game_board[:start] + new_row + game_board[end:]
