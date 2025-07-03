import pickle
import random
import sys
import time

from hints import hints

choices = {1: ("Easy", 10), 2: ("Medium", 5), 3: ("Hard", 3)}


class HighScores:
    def __init__(self):
        try:
            with open("highScores.pkl", "rb") as f:
                readHighScoresInstance = pickle.load(f)
            self.highscoresData = readHighScoresInstance.highscoresData
            print(self.highscoresData)
        except:
            self.highscoresData = []

    def addScore(self, name: str, timer: int, attempts: int, category: int):
        self.highscoresData.append(
            {
                "name": name,
                "category": choices[category][0],
                "timeTaken": timer,
                "attempts": attempts,
            }
        )

        with open("highScores.pkl", "wb") as f:
            pickle.dump(self, f)


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

if __name__ == "__main__":
    while playAgain == "y":
        scores = HighScores()
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

                chances_left -= 1
                print(
                    f"You have {chances_left} chances left" if chances_left != 0 else ""
                )
            except ValueError:
                print("Plese enter a valid number")
                continue
            if number_guessed == number_to_guess:
                endTime = time.time()
                print(
                    f"Congratulations! You guessed the correct number in {int(endTime - startTime)} seconds and you still have {chances_left} chances left."
                )

                scores.addScore(
                    name=input("What is Your Leaderboard Name"),
                    timer=int(endTime - startTime),
                    attempts=chances_left,
                    category=difficulty_level,
                )
                break

            if number_guessed > number_to_guess:
                print(f"Incorrect! The number is less than {number_guessed}.")
            else:
                print(f"Incorrect! The number is greater than {number_guessed}.")
        if chances_left == 0:
            print("You lost the game.")

        if input("Do you want to see the leaderboard: ") == "y":
            for i in scores.highscoresData:
                print(
                    f'{i["name"]} taken  {i["timeTaken"]} seconds  with {i["attempts"]} left in {i["category"]} category'
                )

        playAgain = input("Do you want to play again? (y/N): ")
