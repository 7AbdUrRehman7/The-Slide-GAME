"""CSCA08H: The main program for the Slide game.

Instructions (READ THIS FIRST!)
===============================

Make sure that the files slide_functions.py and a1_checker.py, and the
directory pyta, are in the same directory as this file.

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students
taking the CSCA08 course at the University of Toronto Scarborough. Copying for
purposes other than this use is expressly prohibited. All forms of distribution
of this code, whether as given or with any changes, are expressly prohibited.

"""

import slide_functions as sf

# All the possible squares in the game
SQUARES = sf.RED_SQUARE + sf.YELLOW_SQUARE
PLAYER1_ID = 0
PLAYER2_ID = 1
NUM_MATCH = 3  # Number of spaces to be connected by a player

# The two moves that can2 be done in a game of slide, represented as integers
SLIDE_RIGHT = 1
SLIDE_LEFT = 2


def is_valid_response(response: str, min_value: int, max_value: int) -> bool:
    """Return True if and only if response contains the representation of
    an integer without a +/- sign that is between min_value and max_value,
    inclusive.

    >>> is_valid_response('4', 1, 9)
    True
    >>> is_valid_response('abc', 1, 3)
    False
    """

    return response.isdigit() and sf.between(response, min_value, max_value)


def get_valid_response(prompt_message: str, error_message: str,
                       min_value: int, max_value: int) -> int:
    """Return the user's response to prompt_message. Repeatedly prompt the
    user for input with prompt_message until the user enters a valid
    response. Display error_message for each invalid response entered
    by the user.

    A response is valid if it is a str representation of an integer,
    without a +/- sign, between min_value and max_value, inclusive.

    (No docstring example given since function depends on user input.)
    """

    response = input(prompt_message)
    while not is_valid_response(response, min_value, max_value):
        print(error_message)
        response = input(prompt_message)

    return int(response)


def get_valid_move() -> int:
    """Return the valid move entered by the user. The int 1 represents slide
    right and the int 2 represents slide left. Display an error message for
    each invalid response entered by the user. The user's input is valid if
    it is a string representation of an integer, without a +/- sign that is
    between 1 and 2.

    (No docstring example given since the function depends on user input.)
    """

    print('Which move, slide right or slide left, would you like to do?')
    move = get_valid_response('Enter 1 for slide right and 2 for slide left: ',
                              'That is not a valid move. Try again!', 1, 2)

    return move


def get_valid_row_number(max_row_number: int) -> int:
    """Return a valid row number that is less than or equal to max_row_number.

    (No docstring example given since the function depends on user input.)
    """

    print('Enter a row number between 1 and ' + str(max_row_number) + '.')

    error_message = 'Your suggested row number is not valid. Try again!'
    row = get_valid_response('Enter row number: ', error_message, 1,
                             max_row_number)

    return row


def calculate_last_diagonal_index(row: int, col: int, line_direction: str,
                                  max_row_number: int, max_col_number: int) \
                                  -> int:
    """Return the index of the last character from a line that starts at row
    row and column col and goes in direction line_direction on a game board
    with max_row_number rows and max_col_number columns.

    Preconditions:
        - row and col are valid row numbers and column numbers, respectively.
        - line_direction is one of sf.DOWN_RIGHT, sf.DOWN_LEFT

    >>> calculate_last_diagonal_index(1, 2, sf.DOWN_LEFT, 4, 5)
    5
    >>> calculate_last_diagonal_index(2, 5, sf.DOWN_LEFT, 4, 5)
    17
    >>> calculate_last_diagonal_index(1, 2, sf.DOWN_RIGHT, 4, 5)
    19
    >>> calculate_last_diagonal_index(2, 1, sf.DOWN_RIGHT, 4, 5)
    17
    """

    last_row = row
    last_col = col

    if line_direction == sf.DOWN_LEFT:
        while last_row < max_row_number and last_col > 1:
            last_row = last_row + 1
            last_col = last_col - 1
    else:
        while last_row < max_row_number and last_col < max_col_number:
            last_row = last_row + 1
            last_col = last_col + 1

    return sf.calculate_str_index(last_row, last_col)


def check_win(game_board: str, max_row_number: int, max_col_number: int) \
              -> bool:
    """Return True if and only if the game_board with max_row_number rows and
    max_col_number columns contains a winner.

    The game has been won when a square appears consecutively NUM_MATCH times
    in the horizontal, vertical, or diagonal directions.

    >>> check_win('RYRYRYRYRYYRYRYRYRYR', 4, 5)
    False
    >>> check_win('YRRRYRYRYRYYRYYRYRYR', 4, 5)
    True
    """

    winning_p1 = SQUARES[PLAYER1_ID] * NUM_MATCH
    winning_p2 = SQUARES[PLAYER2_ID] * NUM_MATCH

    # Horizontal wins
    for row in range(1, max_row_number + 1):
        squares = sf.get_row(row, game_board)
        if winning_p1 in squares or winning_p2 in squares:
            return True

    # Vertical wins
    for col in range(1, max_col_number + 1):
        squares = sf.get_column(col, game_board)
        if winning_p1 in squares or winning_p2 in squares:
            return True

    # Diagonal wins: downward rightward
    increment = sf.calculate_increment(sf.DOWN_RIGHT)
    for col in range(1, max_col_number + 1):
        first_index = sf.calculate_str_index(1, col)
        last_index = calculate_last_diagonal_index(1, col, sf.DOWN_RIGHT,
                                                   max_row_number,
                                                   max_col_number)
        squares = game_board[first_index:last_index + 1:increment]

        if winning_p1 in squares or winning_p2 in squares:
            return True

    # Diagonal wins: downward leftward
    increment = sf.calculate_increment(sf.DOWN_LEFT)
    for col in range(1, max_col_number + 1):
        first_index = sf.calculate_str_index(1, col)
        last_index = calculate_last_diagonal_index(1, col, sf.DOWN_LEFT,
                                                   max_row_number,
                                                   max_col_number)
        squares = game_board[first_index:last_index + 1:increment]

        if winning_p1 in squares or winning_p2 in squares:
            return True

    return False


# Interested in why this docstring starts with an r?
# See section 2.4.1: https://docs.python.org/3.11/reference/lexical_analysis.html
def format_game_board(game_board: str, max_row_number: int,
                      max_col_number: int) -> str:
    r"""Return a string representation of game_board with max_row_number rows
    and max_col_number columns.

    >>> format_game_board('Y', 1, 1)
    '   1  \n1  Y\n'
    >>> expected = '   1   2   3   4   5  \n1  R | Y | R | Y | R\n' + \
    ... '2  Y | R | Y | R | Y\n3  Y | R | Y | R | Y\n4  R | Y | R | Y | R\n'
    >>> expected == format_game_board('RYRYRYRYRYYRYRYRYRYR', 4, 5)
    True
    """

    # Add in the column numbers.
    formatted_board = '  '
    for col in range(1, max_col_number + 1):
        formatted_board += ' ' + str(col) + '  '
    formatted_board += '\n'

    # Add in the row numbers, board contents, and grid markers.
    for row in range(1, max_row_number + 1):
        # Row numbers
        formatted_board += str(row) + ' '

        for col in range(1, max_col_number):
            index = sf.calculate_str_index(row, col)
            # Board contents and grid markers
            formatted_board += ' ' + game_board[index] + ' |'

        index = sf.calculate_str_index(row, max_col_number)
        formatted_board += ' ' + game_board[index] + '\n'

    return formatted_board


def play_slide(max_row_number: int, max_col_number: int) -> str:
    """Play a single game of Slide with two human users with a game board
    that has max_row_number rows and max_col_number columns.

    (No docstring example given since the function indirectly depends on user
    input)
    """
    game_board = sf.create_empty_board()

    is_game_over = False
    is_player1_turn = True

    print('Player 1 is using square ' + SQUARES[PLAYER1_ID] + ' and Player 2'
          + ' is using square ' + SQUARES[PLAYER2_ID] + '.')
    print('The first player to match ' + str(NUM_MATCH) + ' squares wins!')

    while not is_game_over:
        print('The Game Board:\n\n' + format_game_board(game_board,
                                                        max_row_number,
                                                        max_col_number))

        if is_player1_turn:
            player = 'Player 1'
            square = SQUARES[PLAYER1_ID]
        else:
            player = 'Player 2'
            square = SQUARES[PLAYER2_ID]

        print(player + "'s turn.")
        move = get_valid_move()
        row = get_valid_row_number(max_row_number)

        if move == SLIDE_LEFT:
            game_board = sf.slide_left(square, row, game_board)
        elif move == SLIDE_RIGHT:
            game_board = sf.slide_right(square, row, game_board)

        print('\n' + player + ' slid ' + square + ' onto row ' + str(row) +
              '.')

        have_winner = check_win(game_board, max_row_number, max_col_number)
        if have_winner:
            if is_player1_turn:
                winner = 'Player 1 wins!\n\n'
            else:
                winner = 'Player 2 wins!\n\n'
            return winner + format_game_board(game_board, max_row_number,
                                              max_col_number)
        if sf.is_board_full(game_board):
            return 'It is a draw!\n\n' + format_game_board(game_board,
                                                           max_row_number,
                                                           max_col_number)
        else:
            is_player1_turn = not is_player1_turn


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    result = play_slide(sf.N_ROWS, sf.N_COLUMNS)
    print(result)
