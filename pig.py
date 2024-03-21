import time
import random
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

    def get_score(self):
        return self.score

    def decide_roll(self):
        return True

class HumanPlayer(Player):
    def decide_roll(self):
        while True:
            decision = input(f"{self.name}, do you want to roll (r) or hold (h)? ").lower().strip()
            if decision == 'r' or decision == 'h':
                return decision == 'r'
            else:
                print("Please enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    def decide_roll(self, turn_total):
        if self.score + turn_total < 100:
            if turn_total < min(25, 100 - self.score):
                return True
            else:
                return False
        else:
            return False

class Factory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type. Must be 'human' or 'computer'.")

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()
        self.winner = None

    def check_time(self):
        if time.time() - self.start_time > 60:
            self.winner = "None"
            return True
        return False

    def play(self):
        while not self.check_time() and not self.game.get_winner():
            self.game.play_turn()

    def get_winner(self):
        if self.winner == "None":
            return None
        elif self.winner:
            return self.winner
        return self.game.get_winner()

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.turn_total = 0

    def play_turn(self):
        print(f"\n{self.current_player.name}'s turn")
        print(f"TOTAL SCORE: {self.current_player.get_score()}")
        self.turn_total = 0
        roll = True
        while roll:
            points = random.randint(1, 6)
            print(f"{self.current_player.name} rolled a {points}")
            if points == 1:
                print(f"{self.current_player.name} got a 1 and lost their turn.")
                self.turn_total = 0
                self.switch_player()
                break
            else:
                self.turn_total += points
                print(f"{self.current_player.name}'s turn total is {self.turn_total}")
                if isinstance(self.current_player, HumanPlayer):
                    roll = self.current_player.decide_roll()
                else:
                    roll = self.current_player.decide_roll(self.turn_total)

        if roll is False or points == 1:
            if points != 1:
                self.current_player.add_score(self.turn_total)
                print(f"{self.current_player.name} holds. {self.current_player.name}'s score is now {self.current_player.get_score()}")
            self.switch_player()

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def get_winner(self):
        if self.player1.get_score() >= 100:
            return self.player1.name
        elif self.player2.get_score() >= 100:
            return self.player2.name
        else:
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pig Game')
    parser.add_argument('--player1', choices=['human', 'computer'], default='human')
    parser.add_argument('--player2', choices=['human', 'computer'], default='human')
    parser.add_argument('--timed', action='store_true')
    args = parser.parse_args()

    player1 = Factory.create_player(args.player1, 'Player 1')
    player2 = Factory.create_player(args.player2, 'Player 2')

    if args.timed:
        game_proxy = TimedGameProxy(Game(player1, player2))
        game_proxy.play()
        winner = game_proxy.get_winner()
    else:
        game = Game(player1, player2)
        while not game.get_winner():
            game.play_turn()
        winner = game.get_winner()

    if winner is None:
        print("Time's up! Game is tied.")
    else:
        print(f"\nThe winner is {winner}!")
