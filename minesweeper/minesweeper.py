"""Implements the game minesweeper."""
import numpy as np
import pandas as pd


def count_mines(i, j, grid):
    """Count number of surrounding mines to a point."""
    count = 0
    for pos in [(i + 1, j), (i + 1, j + 1), (i, j + 1), (i - 1, j + 1),
                (i - 1, j), (i - 1, j - 1), (i, j - 1), (i + 1, j - 1)]:
        count += grid[pos]
    return -count


def create_reference(m, n, mines):
    """Create a grid containing mines and counts."""
    # mines number of mines, and the rest empty
    arr = np.array([-1] * mines + [0] * (m * n - mines))
    # randomise locations
    np.random.shuffle(arr)
    # reshape into m x n grid
    ref_grid = np.reshape(arr, (m, n))
    # copy with zero border to avoid indexing issues
    ref_copy = np.pad(ref_grid, [(1, 1), (1, 1)])
    # count on ref_copy, add counts to ref_grid
    for i in range(0, m):
        for j in range(0, n):
            # only count if not a mine
            if ref_grid[i, j] != -1:
                # (i, j) on grid is (i + 1, j + 1) on copy, as prepended row
                # and col
                ref_grid[i, j] = count_mines(i + 1, j + 1, ref_copy)
    return ref_grid


def player_move(ref_grid, player_grid, flags, mines_flagged, gamestate):
    # take input of position and flag/not
    i = int(input("Row: "))
    j = int(input("Col: "))
    type = input("Flag (f)? ")
    # add flag to player view
    if type == "f":
        player_grid[i, j] = "F"
        # record flag and if it is correct
        flags += 1
        if ref_grid[i, j] == -1:
            mines_flagged += 1
    # check normal move: explode mine or record info on player grid
    else:
        # if mine: explode
        if ref_grid[i, j] == -1:
            print("You lose!")
            player_grid[i, j] = "*"
            gamestate = False
        # if not mine: display value
        else:
            player_grid[i, j] = ref_grid[i, j]

            """
            def check_neighbours(x, y):
                Look at neighbouring squares for 0s.
                for pos in [(x + 1, y), (x + 1, y + 1), (x, y + 1),
                            (x - 1, y + 1), (x - 1, y), (x - 1, y - 1),
                            (x, y - 1), (x + 1, y - 1)]:
                    # if initial square is 0, reveal all neighbours
                    if ref_grid[x, y] == 0 and pos[0] >= 0 and pos[1] >= 0:
                        try:
                            player_grid[pos] = ref_grid[pos]
                        except IndexError:
                            None
                    else:
                        # otherwise: check all possible neigbours for zeroes
                        try:
                            if ref_grid[pos] == 0 and (pos[0] >= 0
                                                       and pos[1] >= 0):
                                player_grid[pos] = ref_grid[pos]
                        except IndexError:
                            None
            #check_neighbours(i, j)

            def show_neighbours(x, y, ref_grid, player_grid):
                Show all neighbours of square.
                for pos in [(x + 1, y), (x + 1, y + 1), (x, y + 1),
                            (x - 1, y + 1), (x - 1, y), (x - 1, y - 1),
                            (x, y - 1), (x + 1, y - 1)]:
                    try:
                        player_grid[pos] = ref_grid[pos]
                    except IndexError:
                        None
                return ref_grid, player_grid
            
            # if zero square, show all neighbours to player
            if ref_grid[i, j] == 0:
                ref_grid, player_grid = show_neighbours(i, j, ref_grid, player_grid)
            """


            def neighbours(x,  y):
                """List of indices of neigbours of (x,y)."""
                # list of all possible neigbours
                idx = [(x + 1, y), (x + 1, y + 1), (x, y + 1),
                            (x - 1, y + 1), (x - 1, y), (x - 1, y - 1),
                            (x, y - 1), (x + 1, y - 1)]
                # list of neighbours
                n_idx = []
                # add those within the grid
                for pos in idx:
                    try:
                        ref_grid[pos]
                        n_idx.append(pos)
                    except IndexError:
                        None
                return n_idx


            def zero_method(x, y, ref_grid, player_grid):
                """Call on zero squares to find all connected zeroes and border."""
                # list of connected zeros
                zero_list = []
                # list of border
                border_list = []
                
                def f(x,y):
                    # loop over all neighbours
                    for pos in neighbours(x,y):
                        # if zero and not in list, add to list and call f
                        if ref_grid[pos] == 0 and not pos in zero_list:
                            zero_list.append(pos)
                            f(pos[0],pos[1])
                        # if not zero and not in border list, add
                        elif not pos in border_list:
                            border_list.append(pos)
                
                f(x,y)

                # now add all zeros and borders found to player view
                for pos in zero_list:
                    player_grid[pos] = ref_grid[pos]
                for pos in border_list:
                    player_grid[pos] = ref_grid[pos]
                
                return ref_grid, player_grid
            

            # if move is a zero, call method
            if ref_grid[i, j] == 0:
                ref_grid, player_grid = zero_method(i, j, ref_grid, player_grid)
            # if not, call on any neighbouring zeros
            else:
                nbs = neighbours(i, j)
                for pos in nbs:
                    if ref_grid[pos] == 0:
                        ref_grid, player_grid = zero_method(pos[0], pos[1], ref_grid, player_grid)






            
                    
                    
                    

    return ref_grid, player_grid, flags, mines_flagged, gamestate


def display_grid(grid):
    """Pretty print player grid."""
    df = pd.DataFrame(grid)
    print(df.to_string(header=True, index=True))


def game(m, n, mines):
    """Run the game."""
    # create reference grid: mine locations and counts
    ref_grid = create_reference(m, n, mines)

    # create a player grid
    player_grid = np.array(["-"] * m * n).reshape((m, n))

    gamestate = True
    flags = 0
    mines_flagged = 0

    # start game
    while gamestate:
        # allow player move
        ref_grid, player_grid, flags, mines_flagged, gamestate = player_move(
            ref_grid, player_grid, flags, mines_flagged, gamestate)

        # display player grid
        display_grid(player_grid)

        # check if all mines flagged
        if mines == flags and mines == mines_flagged:
            print("You win!")
            gamestate = False
