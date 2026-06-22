# A simple terminal-based Tic Tac Toe game starter.
#
# This version displays a 3x3 board, lets players take turns,
# checks for a winner, checks for a draw, and lets players play again.
#
# The goal is to keep the code easy to understand while adding one feature
# at a time.


def display_board(board):
    """Display the Tic Tac Toe board in the terminal.

    The board is a list that contains three smaller lists.
    Each smaller list represents one row of the Tic Tac Toe board.
    """

    # Print a blank line before the board so it is easier to read.
    print()

    # Print the first row of the board.
    print(f" {board[0][0]} | {board[0][1]} | {board[0][2]} ")

    # Print a separator line between the first and second rows.
    print("---+---+---")

    # Print the second row of the board.
    print(f" {board[1][0]} | {board[1][1]} | {board[1][2]} ")

    # Print a separator line between the second and third rows.
    print("---+---+---")

    # Print the third row of the board.
    print(f" {board[2][0]} | {board[2][1]} | {board[2][2]} ")

    # Print a blank line after the board.
    print()


def position_to_row_and_column(position):
    """Convert a position from 1 to 9 into a row and column.

    The player sees the board positions like this:

     1 | 2 | 3
    ---+---+---
     4 | 5 | 6
    ---+---+---
     7 | 8 | 9

    Python lists start counting at 0, so position 1 becomes row 0,
    column 0. Position 9 becomes row 2, column 2.
    """

    # Subtract 1 because humans count from 1, but Python counts from 0.
    position_index = position - 1

    # Dividing by 3 tells us which row the position is in.
    row = position_index // 3

    # The remainder tells us which column the position is in.
    column = position_index % 3

    return row, column


def get_player_move(board, current_player):
    """Ask the current player to choose an empty position from 1 to 9."""

    while True:
        # Ask the current player for a position.
        player_input = input(f"Player {current_player}, choose a position (1-9): ")

        # Make sure the player typed a number.
        if not player_input.isdigit():
            print("Please enter a number from 1 to 9.")
            continue

        # Convert the typed text into a number.
        position = int(player_input)

        # Make sure the number is inside the allowed range.
        if position < 1 or position > 9:
            print("That position is not on the board. Choose 1 to 9.")
            continue

        # Find the row and column for the chosen position.
        row, column = position_to_row_and_column(position)

        # Make sure the chosen square is empty.
        if board[row][column] != " ":
            print("That square is already taken. Choose another one.")
            continue

        # If we get here, the move is valid.
        return row, column


def check_winner(board, current_player):
    """Check whether the current player has won the game."""

    # Check each row for three matching marks.
    for row in board:
        if row[0] == current_player and row[1] == current_player and row[2] == current_player:
            return True

    # Check each column for three matching marks.
    for column in range(3):
        if (
            board[0][column] == current_player
            and board[1][column] == current_player
            and board[2][column] == current_player
        ):
            return True

    # Check the diagonal from top-left to bottom-right.
    if (
        board[0][0] == current_player
        and board[1][1] == current_player
        and board[2][2] == current_player
    ):
        return True

    # Check the diagonal from top-right to bottom-left.
    if (
        board[0][2] == current_player
        and board[1][1] == current_player
        and board[2][0] == current_player
    ):
        return True

    # If none of the checks found a winner, return False.
    return False


def ask_to_play_again():
    """Ask the players whether they want to play another game."""

    while True:
        # Ask for a simple yes or no answer.
        answer = input("Play again? (y/n): ").lower()

        # If the player says yes, start another game.
        if answer == "y" or answer == "yes":
            return True

        # If the player says no, end the program.
        if answer == "n" or answer == "no":
            return False

        # If the answer was not clear, ask again.
        print("Please enter y or n.")


def play_game():
    """Create an empty board and let players play one game."""

    # This is the starting board.
    #
    # There are 3 rows.
    # Each row has 3 spaces.
    # Each space means that the square is empty.
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "],
    ]

    # Show a simple title before the board.
    print("Tic Tac Toe")

    # Show the empty board before any moves are made.
    display_board(board)

    # X always goes first in this simple version.
    current_player = "X"

    # There are only 9 squares, so this loop allows up to 9 turns.
    for turn in range(9):
        # Ask the current player for a valid move.
        row, column = get_player_move(board, current_player)

        # Place the current player's mark on the board.
        board[row][column] = current_player

        # Show the updated board after the move.
        display_board(board)

        # Check whether the current player won with this move.
        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            return

        # If this was the ninth turn and nobody won, the game is a draw.
        if turn == 8:
            print("It's a draw!")
            return

        # Switch to the other player for the next turn.
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


def main():
    """Keep playing Tic Tac Toe until the players choose to stop."""

    while True:
        # Play one full game.
        play_game()

        # Stop the program if the players do not want another game.
        if not ask_to_play_again():
            print("Thanks for playing!")
            break


# This line checks whether this file is being run directly.
# If it is, Python will call the main function and start the program.
if __name__ == "__main__":
    main()
