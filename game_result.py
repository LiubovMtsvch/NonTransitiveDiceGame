class GameResult:
    @staticmethod
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