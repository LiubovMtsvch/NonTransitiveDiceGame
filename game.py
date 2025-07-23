import sys
import hmac
import hashlib
import secrets
from tabulate import tabulate
from colorama import init, Fore

def parse_arguments():
    secret_key = secrets.token_bytes(32)
    if len(sys.argv) < 4:
        print(f"Error: At least 3 dice configurations are required, got {len(sys.argv) - 1}.")
        print("Example: python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
        sys.exit(1)

    available_dice = []
    for arg in sys.argv[1:]:
        try:
            numbers = [int(n) for n in arg.split(',')]
            if len(numbers) < 1:
                print(f"Error: Each die must have at least 1 face, got {len(numbers)} for {arg}.")
                print("Example: python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
                sys.exit(1)
            available_dice.append(numbers)
        except ValueError:
            print(f"Error: All values in '{arg}' must be integers.")
            print("Example: python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
            sys.exit(1)

    return secret_key, available_dice

def calculate_win_probabilities(dice_list):
    size = len(dice_list)
    headers = [Fore.BLUE + "User dice v" + Fore.RESET] + [Fore.BLUE + ",".join(map(str, dice)) + Fore.RESET for dice in dice_list]
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

def determine_first_move(secret_key, available_dice):
    computer_choice = secrets.randbelow(2)
    message = str(computer_choice).encode()
    hmac_value = hmac.new(secret_key, message, hashlib.sha3_256).hexdigest()
    print(f"I selected a random value in the range 0..1 (HMAC={hmac_value}).")

    while True:
        print("Try to guess my selection.")
        print("0 - 0\n1 - 1\nX - exit\n? - help")
        user_selection = input().strip().upper()

        if user_selection in ["0", "1", "X", "?"]:
            if user_selection == "?":
                calculate_win_probabilities(available_dice)
                continue
            if user_selection == "X":
                print("Exiting the game. Bye!")
                sys.exit()
            break
        print("Invalid selection. Please enter 0, 1, X, or ?.")

    print(f"Your selection: {user_selection}")
    print(f"My selection: {computer_choice} (KEY={secret_key.hex()})")

    return int(user_selection) == computer_choice

def select_dice(available_dice, user_first, computer_dice=None):
    if user_first:
        print("You guessed correctly! You make the first move.")
        dice_options = available_dice
    else:
        computer_index = secrets.randbelow(len(available_dice))
        computer_dice = available_dice[computer_index]
        print(f"I make the first move and choose the {computer_dice} dice.")
        dice_options = [dice for i, dice in enumerate(available_dice) if i != computer_index]

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
            calculate_win_probabilities(dice_options)
            continue
        elif player_selection.isdigit() and int(player_selection) in range(len(dice_options)):
            break
        print("Invalid selection. Please choose a valid index.")

    player_index = int(player_selection)
    player_dice = dice_options[player_index]

    if user_first:
        computer_choices = [dice for i, dice in enumerate(available_dice) if i != player_index]
        computer_dice = secrets.choice(computer_choices)

    print(f"You chose: {player_dice}")
    print(f"I choose: {computer_dice}")

    return player_dice, computer_dice

def generate_roll(secret_key, dice_length, label, player_dice, computer_dice, other_user_number=None):
    computer_roll = secrets.randbelow(dice_length)
    message_roll = str(computer_roll).encode()
    hmac_value_roll = hmac.new(secret_key, message_roll, hashlib.sha3_256).hexdigest()
    print(f"It's time for {label}'s roll.\nI selected a random value in the range 0..{dice_length - 1} (HMAC={hmac_value_roll})")

    while True:
        user_input = input(f"Enter your number (0 to {dice_length - 1}) for {label}: ").strip()
        if user_input == "?":
            calculate_win_probabilities([player_dice, computer_dice])
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

def display_results(player_dice, computer_dice, player_roll, computer_roll):
    player_result = player_dice[player_roll]
    computer_result = computer_dice[computer_roll]

    print(f"\nResults:")
    print(f"Your roll result is {player_result}.")
    print(f"My roll result is {computer_result}.")

    if player_result > computer_result:
        print(f"You win ({player_result} > {computer_result})!")
    elif player_result < computer_result:
        print(f"I win ({computer_result} > {player_result})!")
    else:
        print("Result is a tie.")

def main():
    secret_key, available_dice = parse_arguments()
    user_first = determine_first_move(secret_key, available_dice)
    player_dice, computer_dice = select_dice(available_dice, user_first)
    dice_length = len(computer_dice)
    computer_roll_p, user_num_p, _ = generate_roll(secret_key, dice_length, "Player", player_dice, computer_dice)
    computer_roll_c, user_num_c, _ = generate_roll(secret_key, dice_length, "Computer", player_dice, computer_dice)
    player_roll = (computer_roll_p + user_num_c) % dice_length
    computer_roll = (computer_roll_c + user_num_p) % dice_length
    display_results(player_dice, computer_dice, player_roll, computer_roll)

if __name__ == "__main__":
    main()