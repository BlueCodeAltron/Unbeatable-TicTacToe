import time
import math
from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer


class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    # UI
    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]  # we will use a single list to represent 3x3 board

    def print_board(self):
        # getting rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc. (tells us what number corresponds  to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    # Game Logic
    def make_move(self, square, letter):
        # if valid move, then make the move (assign square to letter) then return true
        # if invalid, return false

        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # winner if 3 in a row anywhere... we have to check all of it
        # first, check rows
        row_ind = math.floor(square / 3)
        row = self.board[row_ind * 3: (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # check columns
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # check diagonals
        # but only if the square is an even number (0, 2, 4, 6, 8)
        # diagonal1 =  0, 4, 8; diagonal2 = 2, 4, 6
        # these are the only moves possible to win a diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # left to right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # right to left diagonal
            if all([spot == letter for spot in diagonal2]):
                return True

        # if all of these fail ---> we lost
        return False

    def available_move(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]
        # SAME THING (Long Form) ----->
        # moves = []
        # for [i, spot] in enumerate(self.board):
        #
        #     # ['x', 'x', 'o'] ---> [(0, x), (1, x), (2, o)]
        #     if spot == ' ':
        #         moves.append(i)
        #     return moves

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')


def play(game, x_player, o_player, print_game=True):
    # returns the winner of the game(the letter)! or None for a tie
    if print_game:
        game.print_board_nums()

    letter = "X"  # Starting Letter
    # iterate while the game still has empty squares
    # don't have to worry about winner because we'll return that
    # which breaks the loop
    while game.empty_squares():
        if letter == "O":
            # get appropriate players to get move
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # A function to make a move
        if game.make_move(square, letter):
            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print("")  # empty line! nothing else...

            if game.current_winner:
                if print_game:
                    print(letter + " won!!!")
                return letter

            # after we made a move, we need to alternate letters
            # switching players
            letter = "O" if letter == "X" else "X"
            # shortform of the following
            # if letter == "X":
            #     letter = "O"
            # else:
            #     letter = "X"

        # tiny pause
        time.sleep(0)

    if print_game:
        print('It\'s a tie!!!')


# if __name__ == '__main__':
#     x_player = SmartComputerPlayer('X')
#     o_player = RandomComputerPlayer('O')
#     t = TicTacToe()
#     play(t, x_player, o_player, print_game=True)

if __name__ == '__main__':
    x_wins = 0
    o_wins = 0
    tie = 0
    for _ in range(10):
        x_player = GeniusComputerPlayer('X')
        o_player = RandomComputerPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)
        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            tie += 1

    print(f" X_player wins: {x_wins}; O_player wins {o_wins}; Tie: {tie}")
