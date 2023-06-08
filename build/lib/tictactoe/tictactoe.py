"""Play tic tac toe / noughts and crosses."""


def printstate(state, format=True):
    """Print a grid to display the state of the game."""
    if format:
        state = ["X" if x == 1 else "O" if x == -1 else " " for x in state]
    print(f"{state[0]} | {state[1]} | {state[2]}")
    print("---------")
    print(f"{state[3]} | {state[4]} | {state[5]}")
    print("---------")
    print(f"{state[6]} | {state[7]} | {state[8]}")


def check(state):
    """Check the state of the game for winning positions."""
    solves = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
              [0, 3, 6], [1, 4, 7], [2, 5, 8],
              [0, 4, 8], [2, 4, 6]]
    scores = [sum([state[j] for j in solves[i]]) for i in range(0, 8)]
    if 3 in scores:
        print("p1 wins")
        return False
    elif -3 in scores:
        print("p2 wins")
        return False
    else:
        return True


def game():
    """Play a game of tictactoe via user input."""
    gamestate = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    game = True

    printstate([0, 1, 2, 3, 4, 5, 6, 7, 8], format=False)
    print("Select squares using the above labels")

    while game:

        # p1 move
        pos = int(input("p1 enter a square to play: "))
        gamestate[pos] = 1
        printstate(gamestate)

        game = check(gamestate)

        if game:
            # p2 move
            pos = int(input("p2 enter a square to play: "))
            gamestate[pos] = -1
            printstate(gamestate)

            game = check(gamestate)
