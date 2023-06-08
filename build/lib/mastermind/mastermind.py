"""Module to run mastermind."""
from random import randint


def generate_code(cmp=6, ln=4):
    """Generate a random answer code."""
    return [randint(1, cmp) for i in range(0, ln)]


def check(guess, answer, ln=4):
    """Return G,Y,_ information for a given guess."""
    result = ["_" for i in range(0, ln)]
    temp_answer = answer.copy()
    # check for green and remove from answer
    for i in range(0, ln):
        if guess[i] == temp_answer[i]:
            result[i] = "G"
            temp_answer[i] = None
    # check for yellow and remove from answer
    for i in range(0, ln):
        if guess[i] in temp_answer and result[i] != "G":
            result[i] = "Y"
            temp_answer[temp_answer.index(guess[i])] = None
    return result


def user_guess_recursive(cmp=6, ln=4):
    """Recursive implementation to validate user guesses."""
    str = input(f"Guess {ln} numbers between 1 and {cmp}\n")
    guess = [int(c) for c in str]
    # validate
    for num in guess:
        if num < 1 or num > cmp:
            print(f"Use numbers between 1 and {cmp}")
            guess = user_guess_recursive(cmp, ln)
    if len(guess) != ln:
        print(f"Guess {ln} numbers")
        guess = user_guess_recursive(cmp, ln)
    return guess


def user_guess(cmp=6, ln=4):
    """Validate user guesses to be ln long and between 1 and cmp inclusive."""
    valid = False
    while not valid:
        valid = True
        guess_str = input(f"Guess {ln} numbers between 1 and {cmp}\n")
        guess = [int(c) for c in guess_str]
        # validate
        for num in guess:
            if num < 1 or num > cmp:
                valid = False
        if len(guess) != ln:
            valid = False
    return guess


def game(cmp=6, ln=4):
    """Code to play a mastermind game: accepting inputs and responding."""
    answer = generate_code(cmp, ln)
    play = True

    while play:
        guess = user_guess(cmp, ln)
        result = check(guess, answer, ln)
        if result == ["G" for i in range(0, ln)]:
            print("You win!")
            play = False
        else:
            print("".join(result))
