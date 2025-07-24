import sys
import secrets

class GameSetup:
    def parse_arguments(self):
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