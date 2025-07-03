import random
import sys
import time

from hints import hints

choices = {1: ("Easy", 10), 2: ("Medium", 5), 3: ("Hard", 3)}


def welcome_statements():
    print("Welcome to number Guessing Game!")
    print("I am thinking of a number between 1 and 100.")


def input_difficulty():
    print("Please select the difficulty level:")
    for keys, values in choices.items():
        print(f"{keys}. {values[0]} ({values[1]} chances)")

    while True:
        try:
            difficulty_level = int(input("Enter your choice: "))
            if difficulty_level in choices:
                return difficulty_level
            else:
                raise ValueError()
        except ValueError:
            print("Please choose from the given option")


playAgain = "y"

# keyboard.add_hotkey('ctrl+h', my_function)


if __name__ == "__main__":
    while playAgain == "y":
        welcome_statements()

        difficulty_level = input_difficulty()

        chances_left = choices[difficulty_level][1]

        print(
            f"Great! You have selected the {choices[difficulty_level][0]} difficulty level."
        )

        number_to_guess = random.randint(1, 100)
        print("Let's start the game!")

        print(f"You have {chances_left} chances left, for hint type 'hint'")


        startTime = time.time()

        while chances_left != 0:
            try:
                number_guessed = input("Enter your guess: ")
                if number_guessed == "hint":
                    print("[Hint]: " + hints[number_to_guess])
                    continue
                number_guessed = int(number_guessed)
                if number_guessed > 100 or number_guessed < 1:
                    raise ValueError
                print(f"You have {chances_left} chances left")
            except ValueError:
                print("Plese enter a valid number")
                continue
            if number_guessed == number_to_guess:
                endTime = time.time()
                print(
                    f"Congratulations! You guessed the correct number in {int(endTime - startTime)} seconds and you still have {chances_left} chances left."
                )
                sys.exit()

            chances_left -= 1
            if number_guessed > number_to_guess:
                print(f"Incorrect! The number is less than {number_guessed}.")
            else:
                print(f"Incorrect! The number is greater than {number_guessed}.")
        print("You lost the game.")

        playAgain = input("Do you want to play again? (y/N): ")
