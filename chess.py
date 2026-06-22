# A beginner-friendly terminal-based Chess game starter.
#
# This first version only displays an 8x8 chessboard.
# It places all chess pieces in their normal starting positions.
# It also alternates turns between White and Black.
# It allows pawns, rooks, queens, and kings to move.
# It can detect basic check and checkmate for the pieces that can move.
# Other pieces cannot move yet.


def create_starting_board():
    """Create and return a chessboard with all pieces in starting positions."""

    # We will use short text labels for each piece.
    #
    # The first letter shows the color:
    # W = White
    # B = Black
    #
    # The second letter shows the piece:
    # R = Rook
    # N = Knight
    # B = Bishop
    # Q = Queen
    # K = King
    # P = Pawn
    #
    # Empty squares are written as two spaces: "  "
    board = [
        ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
        ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
        ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"],
    ]

    return board


def display_board(board):
    """Display the chessboard in the terminal."""

    # Print the column labels above the board.
    print()
    print("     A    B    C    D    E    F    G    H")
    print("  +----+----+----+----+----+----+----+----+")

    # Go through each row in the board.
    for row_number in range(8):
        # Chess rows are usually numbered from 8 down to 1.
        chess_rank = 8 - row_number

        # Start the row with the chess rank.
        print(f"{chess_rank} |", end="")

        # Print each square in this row.
        for column_number in range(8):
            print(f" {board[row_number][column_number]} |", end="")

        # End the row with the same chess rank.
        print(f" {chess_rank}")

        # Print a separator line after each row.
        print("  +----+----+----+----+----+----+----+----+")

    # Print the column labels below the board too.
    print("     A    B    C    D    E    F    G    H")
    print()


def switch_player(current_player):
    """Switch from White to Black, or from Black to White."""

    # If White just had a turn, Black goes next.
    if current_player == "White":
        return "Black"

    # Otherwise, White goes next.
    return "White"


def square_to_row_and_column(square):
    """Convert a chess square like E2 into a board row and column.

    The board uses columns A through H and rows 1 through 8.
    Python lists use row and column numbers that start at 0.
    This function translates from chess notation into Python list indexes.
    """

    # A valid square must have exactly two characters, such as E2.
    if len(square) != 2:
        return None

    # Split the square into its letter and number parts.
    file_letter = square[0].upper()
    rank_number = square[1]

    # Make sure the file and rank are both on the board.
    if file_letter < "A" or file_letter > "H":
        return None

    if rank_number < "1" or rank_number > "8":
        return None

    # Convert A-H into 0-7.
    column = ord(file_letter) - ord("A")

    # Convert chess rank 8 to row 0, rank 7 to row 1, and so on.
    row = 8 - int(rank_number)

    return row, column


def is_players_piece(piece, current_player):
    """Check whether a piece belongs to the current player."""

    # Empty squares do not belong to either player.
    if piece == "  ":
        return False

    # White pieces start with W, and Black pieces start with B.
    if current_player == "White":
        return piece[0] == "W"

    return piece[0] == "B"


def is_opponents_piece(piece, current_player):
    """Check whether a piece belongs to the other player."""

    # Empty squares are not opponent pieces.
    if piece == "  ":
        return False

    # If it is not the current player's piece, it is the opponent's piece.
    return not is_players_piece(piece, current_player)


def is_clear_path_for_rook(board, start_row, start_column, end_row, end_column):
    """Check whether a rook has a clear path to its destination."""

    # A rook must move in a straight line.
    if start_row != end_row and start_column != end_column:
        return False

    # Work out which direction the rook is moving.
    row_step = 0
    column_step = 0

    if end_row > start_row:
        row_step = 1
    elif end_row < start_row:
        row_step = -1

    if end_column > start_column:
        column_step = 1
    elif end_column < start_column:
        column_step = -1

    # Start checking one square after the rook's starting square.
    current_row = start_row + row_step
    current_column = start_column + column_step

    # Stop before the destination square.
    while current_row != end_row or current_column != end_column:
        if board[current_row][current_column] != "  ":
            return False

        current_row = current_row + row_step
        current_column = current_column + column_step

    return True


def is_clear_path_for_bishop(board, start_row, start_column, end_row, end_column):
    """Check whether a diagonal path is clear.

    Bishops move diagonally, and queens can also move diagonally.
    We are not adding bishop movement yet, but this helper is useful
    for the queen.
    """

    row_change = end_row - start_row
    column_change = end_column - start_column

    # A diagonal move changes rows and columns by the same amount.
    if abs(row_change) != abs(column_change):
        return False

    # Work out which diagonal direction the piece is moving.
    if row_change > 0:
        row_step = 1
    else:
        row_step = -1

    if column_change > 0:
        column_step = 1
    else:
        column_step = -1

    # Start checking one square after the starting square.
    current_row = start_row + row_step
    current_column = start_column + column_step

    # Stop before the destination square.
    while current_row != end_row or current_column != end_column:
        if board[current_row][current_column] != "  ":
            return False

        current_row = current_row + row_step
        current_column = current_column + column_step

    return True


def is_valid_pawn_move(board, piece, start_row, start_column, end_row, end_column):
    """Check whether a pawn move is legal in this simple version."""

    # White pawns move up the printed board, which means row numbers decrease.
    if piece[0] == "W":
        direction = -1
        starting_row = 6
    else:
        # Black pawns move down the printed board, which means row numbers increase.
        direction = 1
        starting_row = 1

    row_change = end_row - start_row
    column_change = end_column - start_column
    destination_piece = board[end_row][end_column]

    # Move forward one square if the destination is empty.
    if column_change == 0 and row_change == direction and destination_piece == "  ":
        return True

    # Move forward two squares from the pawn's starting row.
    if (
        column_change == 0
        and start_row == starting_row
        and row_change == direction * 2
        and destination_piece == "  "
    ):
        middle_row = start_row + direction

        # The square between the start and destination must also be empty.
        if board[middle_row][start_column] == "  ":
            return True

    # Capture one square diagonally if an opponent's piece is there.
    if abs(column_change) == 1 and row_change == direction:
        if is_opponents_piece(destination_piece, "White" if piece[0] == "W" else "Black"):
            return True

    return False


def is_valid_rook_move(board, start_row, start_column, end_row, end_column):
    """Check whether a rook move is legal in this simple version."""

    return is_clear_path_for_rook(board, start_row, start_column, end_row, end_column)


def is_valid_queen_move(board, start_row, start_column, end_row, end_column):
    """Check whether a queen move is legal in this simple version."""

    # Queens can move like rooks: straight across rows or columns.
    if is_clear_path_for_rook(board, start_row, start_column, end_row, end_column):
        return True

    # Queens can also move diagonally.
    if is_clear_path_for_bishop(board, start_row, start_column, end_row, end_column):
        return True

    return False


def is_valid_king_move(start_row, start_column, end_row, end_column):
    """Check whether a king move is legal in this simple version."""

    row_change = abs(end_row - start_row)
    column_change = abs(end_column - start_column)

    # A king can move one square in any direction.
    return row_change <= 1 and column_change <= 1


def find_king(board, player):
    """Find the row and column of a player's king."""

    # White's king is WK. Black's king is BK.
    if player == "White":
        king = "WK"
    else:
        king = "BK"

    # Search every square until we find the king.
    for row in range(8):
        for column in range(8):
            if board[row][column] == king:
                return row, column

    # This should not happen in a normal game.
    return None


def can_piece_attack_square(board, piece, start_row, start_column, end_row, end_column):
    """Check whether a piece attacks a specific square.

    This is used for check detection.
    For now, it only uses the pieces that this beginner version can move:
    pawns, rooks, queens, and kings.
    """

    piece_type = piece[1]

    # Pawns attack diagonally, even though they move forward.
    if piece_type == "P":
        if piece[0] == "W":
            direction = -1
        else:
            direction = 1

        row_change = end_row - start_row
        column_change = abs(end_column - start_column)

        return row_change == direction and column_change == 1

    # Rooks attack in straight lines if the path is clear.
    if piece_type == "R":
        return is_clear_path_for_rook(board, start_row, start_column, end_row, end_column)

    # Queens attack in straight lines or diagonals if the path is clear.
    if piece_type == "Q":
        return is_valid_queen_move(board, start_row, start_column, end_row, end_column)

    # Kings attack one square in any direction.
    if piece_type == "K":
        return is_valid_king_move(start_row, start_column, end_row, end_column)

    # Bishops and knights are not active in this version yet.
    return False


def is_in_check(board, player):
    """Check whether the given player's king is under attack."""

    king_position = find_king(board, player)

    # If the king is missing, treat that as check to avoid unsafe moves.
    if king_position is None:
        return True

    king_row, king_column = king_position
    opponent = switch_player(player)

    # Look at every opponent piece and ask whether it attacks the king.
    for row in range(8):
        for column in range(8):
            piece = board[row][column]

            if is_players_piece(piece, opponent):
                if can_piece_attack_square(
                    board, piece, row, column, king_row, king_column
                ):
                    return True

    return False


def is_valid_move_for_piece(board, piece, start_row, start_column, end_row, end_column):
    """Check a piece's movement rule without changing the board."""

    piece_type = piece[1]

    if piece_type == "P":
        return is_valid_pawn_move(
            board, piece, start_row, start_column, end_row, end_column
        )

    if piece_type == "R":
        return is_valid_rook_move(board, start_row, start_column, end_row, end_column)

    if piece_type == "Q":
        return is_valid_queen_move(board, start_row, start_column, end_row, end_column)

    if piece_type == "K":
        return is_valid_king_move(start_row, start_column, end_row, end_column)

    return False


def make_temporary_move(board, start_row, start_column, end_row, end_column):
    """Move a piece, but return the captured piece so the move can be undone."""

    moving_piece = board[start_row][start_column]
    captured_piece = board[end_row][end_column]

    board[end_row][end_column] = moving_piece
    board[start_row][start_column] = "  "

    return captured_piece


def undo_temporary_move(
    board, start_row, start_column, end_row, end_column, captured_piece
):
    """Undo a temporary move."""

    moving_piece = board[end_row][end_column]

    board[start_row][start_column] = moving_piece
    board[end_row][end_column] = captured_piece


def has_any_legal_move(board, player):
    """Check whether a player has at least one legal move available."""

    # Try every square as a starting square.
    for start_row in range(8):
        for start_column in range(8):
            piece = board[start_row][start_column]

            # Skip empty squares and opponent pieces.
            if not is_players_piece(piece, player):
                continue

            # Try every square as a possible destination.
            for end_row in range(8):
                for end_column in range(8):
                    destination_piece = board[end_row][end_column]

                    # A player cannot move onto one of their own pieces.
                    if is_players_piece(destination_piece, player):
                        continue

                    # The king is never captured in chess.
                    if destination_piece.endswith("K"):
                        continue

                    # Skip moves that do not match the piece's movement rule.
                    if not is_valid_move_for_piece(
                        board, piece, start_row, start_column, end_row, end_column
                    ):
                        continue

                    # Try the move.
                    captured_piece = make_temporary_move(
                        board, start_row, start_column, end_row, end_column
                    )

                    # If the player is not in check after this move,
                    # then at least one legal move exists.
                    move_is_safe = not is_in_check(board, player)

                    # Put the board back exactly how it was.
                    undo_temporary_move(
                        board,
                        start_row,
                        start_column,
                        end_row,
                        end_column,
                        captured_piece,
                    )

                    if move_is_safe:
                        return True

    return False


def is_checkmate(board, player):
    """Check for basic checkmate."""

    # A player is checkmated only if they are in check
    # and have no legal move that gets out of check.
    return is_in_check(board, player) and not has_any_legal_move(board, player)


def move_piece(board, current_player, start_square, end_square):
    """Try to move a piece and return True if the move worked."""

    # Convert squares like E2 and E4 into board indexes.
    start_position = square_to_row_and_column(start_square)
    end_position = square_to_row_and_column(end_square)

    # Stop if either square was typed incorrectly.
    if start_position is None or end_position is None:
        print("Please use squares like E2 or A7.")
        return False

    start_row, start_column = start_position
    end_row, end_column = end_position

    # Get the piece from the starting square.
    piece = board[start_row][start_column]

    # Empty squares cannot be moved.
    if piece == "  ":
        print("There is no piece on that starting square.")
        return False

    # Make sure the player chose one of their own pieces.
    if not is_players_piece(piece, current_player):
        print(f"Please choose one of {current_player}'s pieces.")
        return False

    # Do not allow a player to capture their own piece.
    destination_piece = board[end_row][end_column]
    if is_players_piece(destination_piece, current_player):
        print("You cannot move onto one of your own pieces.")
        return False

    # The king is never captured. Checkmate ends the game instead.
    if destination_piece.endswith("K"):
        print("You cannot capture the king. Try to give checkmate instead.")
        return False

    # For now, only pawns, rooks, queens, and kings can move.
    if piece[1] not in ["P", "R", "Q", "K"]:
        print("Only pawns, rooks, queens, and kings can move right now.")
        return False

    valid_move = is_valid_move_for_piece(
        board, piece, start_row, start_column, end_row, end_column
    )

    # If the movement rule failed, do not change the board.
    if not valid_move:
        print("That move is not allowed for that piece.")
        return False

    # Try the move on the board.
    captured_piece = make_temporary_move(
        board, start_row, start_column, end_row, end_column
    )

    # A player is not allowed to leave their own king in check.
    if is_in_check(board, current_player):
        undo_temporary_move(
            board, start_row, start_column, end_row, end_column, captured_piece
        )
        print("That move would leave your king in check.")
        return False

    return True


def main():
    """Create the starting chessboard and alternate player turns."""

    # Create a board with all pieces in their starting positions.
    board = create_starting_board()

    # Show a simple title before the board.
    print("Chess")

    # Display the board in the terminal.
    display_board(board)

    # White always goes first in chess.
    current_player = "White"

    # This simple loop gives each player a turn.
    while True:
        print(f"{current_player}'s turn")
        player_input = input("Enter a move like E2 E4, or type q to quit: ")

        # Let the players stop the program when they are done.
        if player_input.lower() == "q":
            print("Thanks for playing!")
            break

        # Split the input into words.
        move_parts = player_input.split()

        # A move needs two squares: the start square and the end square.
        if len(move_parts) != 2:
            print("Please enter a move with a start square and an end square.")
            continue

        start_square = move_parts[0]
        end_square = move_parts[1]

        # Try to move the piece.
        move_was_successful = move_piece(
            board, current_player, start_square, end_square
        )

        # Only switch turns after a successful move.
        if move_was_successful:
            # Show the updated board.
            display_board(board)

            opponent = switch_player(current_player)

            # After a successful move, check whether the opponent is in check.
            if is_checkmate(board, opponent):
                print(f"Checkmate! {current_player} wins!")
                break

            if is_in_check(board, opponent):
                print(f"{opponent} is in check.")

            current_player = opponent


# This line checks whether this file is being run directly.
# If it is, Python will call the main function and start the program.
if __name__ == "__main__":
    main()
