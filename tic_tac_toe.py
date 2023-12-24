from pyfiglet import Figlet
from collections import deque
from colorama import init, Fore

init()  # Initialize Colorama

players = deque()  # Define an empty deque for players
turns = 0  # Define 'turns' as a global variable
player_one_wins = 0  # Counter for Player 1 wins
player_two_wins = 0  # Counter for Player 2 wins
draws = 0  # Counter for draws

# Define color codes for players
player_colors = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]


def print_start():
    f = Figlet(font='slant')
    title = f.renderText("Tic-Tac-Toe")
    print(title)
    print("Welcome to Tic-Tac-Toe game!")
    print("Let's get started!\n")


def check_for_win():
    global player_one_wins, player_two_wins, draws

    player_name, player_symbol = players[0]
    opponent_name, opponent_symbol = players[1]

    # Check for diagonal wins
    first_diagonal_win = all([board[i][i] == player_symbol for i in range(SIZE)])
    second_diagonal_win = all([board[i][SIZE - i - 1] == player_symbol for i in range(SIZE)])

    # Check for row wins
    row_win = any([all(player_symbol == pos for pos in row) for row in board])

    # Check for column wins
    col_win = any([all(board[r][c] == player_symbol for r in range(SIZE)) for c in range(SIZE)])

    if any([first_diagonal_win, second_diagonal_win, row_win, col_win]):
        if all([first_diagonal_win, second_diagonal_win, row_win, col_win]):
            print_board(winning_path=[(i, i) for i in range(SIZE)])
            print(Fore.GREEN + f"{player_name} won!" + Fore.RESET)
            print(Fore.RED + f"{opponent_name} lost!" + Fore.RESET)
            if player_name == players[0][0]:
                player_one_wins += 1
            else:
                player_two_wins += 1
        else:
            winning_path = []
            if first_diagonal_win:
                winning_path = [(i, i) for i in range(SIZE)]
            elif second_diagonal_win:
                winning_path = [(i, SIZE - i - 1) for i in range(SIZE)]
            elif row_win:
                for r in range(SIZE):
                    if all(board[r][c] == player_symbol for c in range(SIZE)):
                        winning_path = [(r, c) for c in range(SIZE)]
                        break
            elif col_win:
                for c in range(SIZE):
                    if all(board[r][c] == player_symbol for r in range(SIZE)):
                        winning_path = [(r, c) for r in range(SIZE)]
                        break

            print_board(winning_path=winning_path)
            player_idx = next(
                idx for idx, player in enumerate(players) if player[0] == player_name and player[1] == player_symbol
            )
            print(Fore.GREEN + f"{player_name} won!" + Fore.RESET)
            print(Fore.RED + f"{opponent_name} lost!" + Fore.RESET)
            if player_name == players[0][0]:
                player_one_wins += 1
            else:
                player_two_wins += 1
        raise SystemExit

    if turns == SIZE * SIZE and not any([first_diagonal_win, second_diagonal_win, row_win, col_win]):
        print_board()
        print("Draw!")
        draws += 1
        raise SystemExit


def place_symbol(row, col):
    global last_move

    board[row][col] = players[0][1]
    last_move = (row, col)

    check_for_win()

    if turns == SIZE * SIZE:
        print_board()
        print("Draw!")
        update_game_stats(None)  # Update game stats for a draw
        raise SystemExit

    players.append(players.popleft())  # Rotate players manually


def choose_position():
    global turns

    while True:
        try:
            position = int(input(f"{players[0][0]} choose a free position in the range [1-{SIZE * SIZE}]: "))
            row, col = (position - 1) // SIZE, (position - 1) % SIZE
        except ValueError:
            print(f"{players[0][0]}, please select a valid position!")
            continue

        if 1 <= position <= SIZE * SIZE and board[row][col] == ' ':
            turns += 1
            place_symbol(row, col)
            break
        else:
            print(f"{players[0][0]}, please select a valid position!")


def print_board(begin=False, winning_path=None):
    if begin:
        print("This is the numeration of the board:")
        numeration_board = [[str(i + 1 + SIZE * j).rjust(len(str(SIZE * SIZE))) for i in range(SIZE)] for j in range(SIZE)]
        [print(f"| {' | '.join(row)} |") for row in numeration_board]
        print("\n")

    if not begin:
        for row_idx, row in enumerate(board):
            line = "| "
            for col_idx, pos in enumerate(row):
                if winning_path and (row_idx, col_idx) in winning_path:
                    line += Fore.GREEN + pos + Fore.RESET + " | "
                else:
                    line += pos + " | "
            print(line)

        print("\n")




def play_game():
    player_one_name = input("Player 1, please enter your name: ")
    player_two_name = input("Player 2, please enter your name: ")

    while True:
        player_one_symbol = input(f"{player_one_name} would you like to play with 'X' or 'O'? ").upper()

        if player_one_symbol not in ["X", "O"]:
            print(f"{player_one_name}, please select a valid option!")
        else:
            break

    player_two_symbol = "O" if player_one_symbol == "X" else "X"

    players.append([player_one_name, player_one_symbol])
    players.append([player_two_name, player_two_symbol])

    print_board(begin=True)  # Print the board with numeration

    try:
        choose_position()
    except SystemExit:
        return False

    while True:
        try:
            print_board()  # Print the board after each player's turn
            choose_position()
        except SystemExit:
            return False


def play_again():
    global turns
    while True:
        replay_choice = input("Do you want to play again? (Y/N): ").upper()
        if replay_choice == "Y":
            turns = 0
            return True
        elif replay_choice == "N":
            return False
        else:
            print("Please enter a valid option (Y/N).")


def get_board_size():
    while True:
        try:
            size = int(input("Enter the board size (3 or greater): "))
            if size >= 3:
                return size
            else:
                print("Invalid board size. Please enter a value of 3 or greater.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def update_game_stats(winner):
    print("-------- Game Stats --------")
    print(f"Player 1 wins: {player_one_wins}")
    print(f"Player 2 wins: {player_two_wins}")
    print(f"Draws: {draws}")
    print("-----------------------------")
    if winner:
        print(f"Congratulations, {winner[0]}!")


if __name__ == "__main__":
    print_start()
    SIZE = get_board_size()
    board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
    while True:
        play_game()
        update_game_stats(players[0])  # Update game stats for the winner
        board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]  # Reset the board for a new game
        if not play_again():
            break


def print_stats():
    print("\nGame Statistics:")
    print(f"{players[0][0]} wins: {player_one_wins}")
    print(f"{players[1][0]} wins: {player_two_wins}")
    print(f"Draws: {draws}")


print_start()