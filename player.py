"""Implementation of command-line TicTacToe by Abdul Basit Tonmoy
Spacial Thanks to Kylie Ying"""


import math
import random


class Player():
    def __init__(self, letter):
        # letter is x or 0
        self.letter = letter

    # we want all players to get their move given a game
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for next move
        square = random.choice(game.available_move())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        value = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            # So we checked that if the value is correct or not
            # by casting it to an integer, and if it's not,
            # we say --> Invalid.
            # If the spot isn't available on the board, we also say invalid.
            try:
                value = int(square)
                if value not in game.available_move():
                    raise ValueError
                valid_square = True  # if value is in game.available_move(), it's valid. So  no error. Yay...
            except ValueError:
                print("Invalid Square Input. Try Again.")
        return value


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_move()) == 9:
            square = random.choice(game.available_move())  # randomly choose a spot

        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # Me/ You
        other_player = "O" if player == "X" else "X"  # the other player who is not you or me

        # first, we want to check if the previous move is a winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return position AND score because we need to keep track of score for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player
                    else -1 * (state.num_empty_squares() + 1)}

        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        # Initialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize (be large)
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize

        for possible_move in state.available_move():
            # step 1: make a move and try that spot
            state.make_move(possible_move, player)

            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)  # now, we alternate the player

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # otherwise this will get messed up from the recurse

            # step 4: update the dictionary if necessary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score  # replace the best
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score  # replace the best

        return best
