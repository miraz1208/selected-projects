"""
This program/game-
*** Prompts the user for a level, 'n',
If the user does not input 1, 2, or 3, the program prompts again.

*** Randomly generates ten (10) math problems formatted as X + Y = ,
wherein each of X and Y is a non-negative integer with 'n' digits.

*** Prompts the user to solve each of those problem.
If an answer is not correct (or not even a number),
the program outputs 'Wrong!' and prompt the user again,
allowing the user up to three tries in total.
If the user has still not answered correctly after three tries,
the program outputs the correct answer.

    Raises:
        ValueError:
            while choosing level-
            If user doesn't input any numbers among 1/2/3,
            raises 'ValuerError' with message

    Returns:
        int: The program ultimately outputs the user's score out of 10.
"""


import sys
import random


class Professor():
    '''Main game class'''
    def __init__(self):
        self.main_game()

    def get_level(self):
        '''Decides level from input'''
        levels = [1, 2, 3]
        while True:
            try:
                level = int(input("Choose your level: "))
                if level in levels:
                    return level
                raise ValueError
            except ValueError:
                print("Please choose a number among 1, 2, and 3!")
                continue

    def generate_integer(self, level: int):
        '''Generates integers from level'''
        if level == 1:
            num1 = random.randint(0, 9)
            num2 = random.randint(0, 9)
            return (num1, num2)
        if level == 2:
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
            return (num1, num2)
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        return (num1, num2)

    def simulate_tries(self, num1: int, num2: int):
        '''Checks attempts, returns True of False depending on condition'''
        attempts = 1
        while attempts <= 3:
            try:
                math = int(input(f"{num1} + {num2} = "))
                if math == (num1 + num2):
                    print("Correct!")
                    return True
                attempts += 1
                print("Wrong!")
            except ValueError:
                attempts += 1
                print("Wrong!")
            except EOFError:
                sys.exit()
        print(f"{num1} + {num2} = {num1+num2}")
        return False

    def game(self, level: int):
        '''Takes level(int) as input, returns score(int)'''
        rounds = 0
        score = 0
        while rounds <= 9:
            num1, num2 = self.generate_integer(level)
            response = self.simulate_tries(num1, num2)
            if response is True:
                score += 1
            rounds += 1
        return score

    def main_game(self):
        '''Main game function'''
        level = self.get_level()
        score = self.game(level)
        print(f"You scored: {score}/10 ")


Professor()
