import sys
import secrets
import hmac
import hashlib
from tabulate import tabulate
from colorama import init, Fore

class GameMove:
    def __init__(self, secret_key, available_dice):
        init()
        self.secret_key = secret_key
        self.available_dice = available_dice

    def calculate_win_probabilities(self, dice_list):
        size = len(dice_list)
        headers = [Fore.BLUE + "User dice v" + Fore.RESET] + [
            Fore.BLUE + ",".join(map(str, dice)) + Fore.RESET for dice in dice_list
        ]
        table = []
        for i in range(size):
            row = [",".join(map(str, dice_list[i]))]
            for j in range(size):
                if i == j:
                    row.append(".3333")
                    continue
                wins = 0
                total = 0
                for a in dice_list[i]:
                    for b in dice_list[j]:
                        total += 1
                        if a > b:
                            wins += 1
                probability = wins / total
                row.append(f"{probability:.4f}")
            table.append(row)

        print("\nProbability Table (A vs B):")
        print("This table shows the probability of one die beating another.")
        print(tabulate(table, headers=headers, tablefmt="grid"))
        print()

    def determine_first_move(self):
        computer_choice = secrets.randbelow(2)
        message = str(computer_choice).encode()
        hmac_value = hmac.new(self.secret_key, message, hashlib.sha3_256).hexdigest()
        print(f"I selected a random value in the range 0..1 (HMAC={hmac_value}).")

        while True:
            print("Try to guess my selection.")
            print("0 - 0\n1 - 1\nX - exit\n? - help")
            user_selection = input().strip().upper()

            if user_selection in ["0", "1", "X", "?"]:
                if user_selection == "?":
                    self.calculate_win_probabilities(self.available_dice)
                    continue
                if user_selection == "X":
                    print("Exiting the game. Bye!")
                    sys.exit()
                break
            print("Invalid selection. Please enter 0, 1, X, or ?.")

        print(f"Your selection: {user_selection}")
        print(f"My selection: {computer_choice} (KEY={self.secret_key.hex()})")

        return int(user_selection) == computer_choice

    def select_dice(self, user_first, computer_dice=None):
        if user_first:
            print("You guessed correctly! You make the first move.")
            dice_options = self.available_dice
        else:
            computer_index = secrets.randbelow(len(self.available_dice))
            computer_dice = self.available_dice[computer_index]
            print(f"I make the first move and choose the {computer_dice} dice.")
            dice_options = [dice for i, dice in enumerate(self.available_dice) if i != computer_index]

        while True:
            print("Choose your dice:")
            for idx, dice in enumerate(dice_options):
                print(f"{idx} - {','.join(map(str, dice))}")
            print("X - exit\n? - help")

            player_selection = input("Your selection: ").strip().upper()
            if player_selection == "X":
                print("Exiting the game. Bye!")
                sys.exit()
            elif player_selection == "?":
                self.calculate_win_probabilities(dice_options)
                continue
            elif player_selection.isdigit() and int(player_selection) in range(len(dice_options)):
                break
            print("Invalid selection. Please choose a valid index.")

        player_index = int(player_selection)
        player_dice = dice_options[player_index]

        if user_first:
            computer_choices = [dice for i, dice in enumerate(self.available_dice) if i != player_index]
            computer_dice = secrets.choice(computer_choices)

        print(f"You chose: {player_dice}")
        print(f"I choose: {computer_dice}")

        return player_dice, computer_dice