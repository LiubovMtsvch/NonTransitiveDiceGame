from game_setup import GameSetup
from game_move import GameMove
from roll_generator import RollGenerator
from game_result import GameResult

def main():
    game_setup = GameSetup()
    secret_key, available_dice = game_setup.parse_arguments()
    game_move = GameMove(secret_key, available_dice)
    user_first = game_move.determine_first_move()
    player_dice, computer_dice = game_move.select_dice(user_first)
    dice_length = len(computer_dice)
    computer_roll_p, user_num_p, _ = RollGenerator.generate_roll(secret_key, dice_length, "Player", player_dice, computer_dice)
    computer_roll_c, user_num_c, _ = RollGenerator.generate_roll(secret_key, dice_length, "Computer", player_dice, computer_dice)
    player_roll = (computer_roll_p + user_num_c) % dice_length
    computer_roll = (computer_roll_c + user_num_p) % dice_length
    GameResult.display_results(player_dice, computer_dice, player_roll, computer_roll)

if __name__ == "__main__":
    main()