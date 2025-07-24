import sys
import hmac
import hashlib
import secrets
from tabulate import tabulate
from colorama import init, Fore

class RollGenerator:
    @staticmethod
    def calculate_win_probabilities(dice_list):
        init()
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

    @staticmethod
    def generate_roll(secret_key, dice_length, label, player_dice, computer_dice, other_user_number=None):
        computer_roll = secrets.randbelow(dice_length)
        message_roll = str(computer_roll).encode()
        hmac_value_roll = hmac.new(secret_key, message_roll, hashlib.sha3_256).hexdigest()
        print(f"It's time for {label}'s roll.\nI selected a random value in the range 0..{dice_length - 1} (HMAC={hmac_value_roll})")

        while True:
            user_input = input(f"Enter your number (0 to {dice_length - 1}) for {label}: ").strip()
            if user_input == "?":
                RollGenerator.calculate_win_probabilities([player_dice, computer_dice])
                continue
            if not user_input.isdigit() or int(user_input) not in range(dice_length):
                print("Invalid input. Try again.")
                continue
            user_number = int(user_input)
            break

        print(f"My roll for {label} was: {computer_roll}")
        print(f"HMAC KEY: {secret_key.hex()}")
        expected_hmac = hmac.new(secret_key, str(computer_roll).encode(), hashlib.sha3_256).hexdigest()
        if expected_hmac != hmac_value_roll:
            print("MAC verification failed! Data might have been tampered.")
            sys.exit()
        else:
            print("HMAC verified successfully.")

        final_index = (computer_roll + (user_number if other_user_number is None else other_user_number)) % dice_length
        return computer_roll, user_number, final_index