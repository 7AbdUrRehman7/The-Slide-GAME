"""Independent reimplementation of the slide game UI/logic.
(No course-provided text or docstrings are copied.)

Note for owner: Modified to avoid Copyright, origional implementation is still on the documents/CSCA08/[here]
"""
import sys
import slide_functions as sf

# Public constants (preserve original external API/values)
SQUARES = sf.RED_SQUARE + sf.YELLOW_SQUARE
PLAYER1_ID = 0
PLAYER2_ID = 1
NUM_MATCH = 3

SLIDE_RIGHT = 1
SLIDE_LEFT = 2


def is_valid_response(response: str, min_value: int, max_value: int) -> bool:
    """Return True iff response is an unsigned integer string within [min_value, max_value]."""
    return response.isdigit() and sf.between(response, min_value, max_value)


def get_valid_response(prompt_message: str, error_message: str,
                       min_value: int, max_value: int) -> int:
    """Prompt until a valid integer in [min_value, max_value] is entered (no +/-)."""
    while True:
        resp = input(prompt_message)
        if is_valid_response(resp, min_value, max_value):
            return int(resp)
        print(error_message)


def get_valid_move() -> int:
    """Ask for a move: 1 = right, 2 = left. Repeat until valid."""
    prompt = f'Enter a move ({SLIDE_RIGHT} for right, {SLIDE_LEFT} for left): '
    error = f'Invalid move: enter {SLIDE_RIGHT} or {SLIDE_LEFT}.'
    return get_valid_response(prompt, error, SLIDE_RIGHT, SLIDE_LEFT)


def get_valid_row_number(max_row_number: int) -> int:
    """Ask for a row number in [1, max_row_number]. Repeat until valid."""
    prompt = f'Enter a row number (1-{max_row_number}): '
    error = f'Invalid row: enter a number between 1 and {max_row_number}.'
    return get_valid_response(prompt, error, 1, max_row_number)


def calculate_last_diagonal_index(row: int, col: int, line_direction: str,
                                  max_row_number: int, max_col_number: int) -> int:
    """Return the last index for a diagonal starting at (row, col) in the given direction."""
    if line_direction == sf.DOWN_LEFT:
        steps = min(max_row_number - row, col - 1)
        r2, c2 = row + steps, col - steps
    else:  # sf.DOWN_RIGHT
        steps = min(max_row_number - row, max_col_number - col)
        r2, c2 = row + steps, col + steps
    return sf.calculate_str_index(r2, c2)


def _contains_win(sequence: str) -> bool:
    """Return True if sequence contains NUM_MATCH identical non-black squares consecutively."""
    target1 = SQUARES[PLAYER1_ID] * NUM_MATCH
    target2 = SQUARES[PLAYER2_ID] * NUM_MATCH
    return target1 in sequence or target2 in sequence


def check_win(game_board: str, max_row_number: int, max_col_number: int) -> bool:
    """Return True iff the board has a winning line horizontally, vertically, or diagonally."""
    # Horizontal
    for r in range(1, max_row_number + 1):
        if _contains_win(sf.get_row(r, game_board)):
            return True

    # Vertical
    for c in range(1, max_col_number + 1):
        if _contains_win(sf.get_column(c, game_board)):
            return True

    # Diagonals: down-right and down-left starting from top row
    step = sf.calculate_increment(sf.DOWN_RIGHT)
    for c in range(1, max_col_number + 1):
        start = sf.calculate_str_index(1, c)
        end = calculate_last_diagonal_index(1, c, sf.DOWN_RIGHT, max_row_number, max_col_number)
        if _contains_win(game_board[start:end+1:step]):
            return True

    step = sf.calculate_increment(sf.DOWN_LEFT)
    for c in range(1, max_col_number + 1):
        start = sf.calculate_str_index(1, c)
        end = calculate_last_diagonal_index(1, c, sf.DOWN_LEFT, max_row_number, max_col_number)
        if _contains_win(game_board[start:end+1:step]):
            return True

    return False


def format_game_board(game_board: str, max_row_number: int, max_col_number: int) -> str:
    """Return a string grid with header/row numbers, matching the original formatting exactly."""
    out = '  '
    for c in range(1, max_col_number + 1):
        out += f' {c}  '
    out += '\n'
    for r in range(1, max_row_number + 1):
        out += f'{r} '
        for c in range(1, max_col_number):
            idx = sf.calculate_str_index(r, c)
            out += f' {game_board[idx]} |'
        idx = sf.calculate_str_index(r, max_col_number)
        out += f' {game_board[idx]}\n'
    return out


def play_slide(max_row_number: int, max_col_number: int) -> str:
    """Run a two-player game session and return the final message + board."""
    board = sf.create_empty_board()
    is_p1 = True

    print('Player 1 is using square ' + SQUARES[PLAYER1_ID] +
          ' and Player 2 is using square ' + SQUARES[PLAYER2_ID] + '.')
    print('The first player to match ' + str(NUM_MATCH) + ' squares wins!')

    while True:
        print('The Game Board:\n\n' + format_game_board(board, max_row_number, max_col_number))

        player = 'Player 1' if is_p1 else 'Player 2'
        square = SQUARES[PLAYER1_ID] if is_p1 else SQUARES[PLAYER2_ID]

        print(player + "'s turn.")
        move = get_valid_move()
        row = get_valid_row_number(max_row_number)

        if move == SLIDE_LEFT:
            board = sf.slide_left(square, row, board)
        else:
            board = sf.slide_right(square, row, board)

        print('\n' + player + ' slid ' + square + ' onto row ' + str(row) + '.')

        if check_win(board, max_row_number, max_col_number):
            winner = 'Player 1 wins!\n\n' if is_p1 else 'Player 2 wins!\n\n'
            return winner + format_game_board(board, max_row_number, max_col_number)
        if sf.is_board_full(board):
            return 'It is a draw!\n\n' + format_game_board(board, max_row_number, max_col_number)

        is_p1 = not is_p1


if __name__ == '__main__':
    # Avoid running doctests; interactive session only.
    result = play_slide(sf.N_ROWS, sf.N_COLUMNS)
    print(result)
