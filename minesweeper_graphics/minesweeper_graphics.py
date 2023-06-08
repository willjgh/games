"""Graphical display for minesweeper."""
import numpy as np
import os
import pygame

#os.environ['SDL_VIDEO_CENTERED'] = '1'

"""
window_height = 900
window_width = 900

pygame.init()
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()

def display_grid(m, n):
    Draw an m x n (row x col) grid of squares.
    # width of grid cells
    cell_size = int(window_width / n)
    # for each corner in grid, draw rectangle
    for x in range(0, cell_size * n, cell_size):
        for y in range(0, cell_size * m, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, (200,200,200), rect, 1)


x = 250
y = 160
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_RIGHT:
                x += 8
            elif event.key == pygame.K_LEFT:
                x -= 8
            elif event.key == pygame.K_DOWN:
                y += 8
            elif event.key == pygame.K_UP:
                y -= 8

    display_grid(20,10)  
    pygame.display.update()  

    clock.tick(60)

pygame.quit()
"""

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

"""
def player_move(i, j, type, ref_grid, player_grid, flags, mines_flagged, running):
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
            running = False
        # if not mine: display value
        else:
            player_grid[i, j] = ref_grid[i, j]

            def neighbours(x,  y):
                List of indices of neigbours of (x,y).
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
                Call on zero squares to find all connected zeroes and border.
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

    return ref_grid, player_grid, flags, mines_flagged, running
    
def display_grid(m, n, player_grid, window):
    # width of grid cells
    cell_size = min([int(1000 / n), int(1000 / m)])
    # for each corner in grid, draw rectangle
    for x in range(0, cell_size * n, cell_size):
        for y in range(0, cell_size * m, cell_size):
            #rect = pygame.Rect(x, y, cell_size, cell_size)
            #pygame.draw.rect(window, (200,200,200), rect, 1)
            #location = pygame.math.Vector2(x * cell_size, y * cell_size)
            #window.blit(sprite2, rect, rect)
            sprite2 = pygame.transform.scale(pygame.image.load("two.png"), (cell_size, cell_size))
            window.blit(sprite2, (x,y))
"""


class Game():
    def __init__(self, m, n, mines):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # setup game
        pygame.init()
        self.window = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("Minesweeper")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.clock = pygame.time.Clock()
        self.running = True
        # store values
        self.m = m
        self.n = n
        self.mines = mines
        self.flags = 0
        self.mines_flagged = 0
        # create reference grid
        self.ref_grid = create_reference(m, n, mines)
        # create a player grid
        self.player_grid = np.array(["-"] * m * n).reshape((m, n))
        # store current move
        self.x = 0
        self.y = 0
        self.type = ""
        # load sprites
        self.cell_size = min([int(1000 / n), int(1000 / m)])
        self.sprite1 = pygame.transform.scale(pygame.image.load("one.png"), (self.cell_size, self.cell_size))
        self.sprite2 = pygame.transform.scale(pygame.image.load("two.png"), (self.cell_size, self.cell_size))
        self.sprite3 = pygame.transform.scale(pygame.image.load("three.png"), (self.cell_size, self.cell_size))
        self.sprite4 = pygame.transform.scale(pygame.image.load("four.png"), (self.cell_size, self.cell_size))
        self.sprite5 = pygame.transform.scale(pygame.image.load("five.png"), (self.cell_size, self.cell_size))
        self.sprite6 = pygame.transform.scale(pygame.image.load("six.png"), (self.cell_size, self.cell_size))
        self.sprite7 = pygame.transform.scale(pygame.image.load("seven.png"), (self.cell_size, self.cell_size))
        self.sprite8 = pygame.transform.scale(pygame.image.load("eight.png"), (self.cell_size, self.cell_size))
        self.spritef = pygame.transform.scale(pygame.image.load("flag.png"), (self.cell_size, self.cell_size))
        self.spriterevealed = pygame.transform.scale(pygame.image.load("revealed.png"), (self.cell_size, self.cell_size))
        self.spriteunrevealed = pygame.transform.scale(pygame.image.load("unrevealed.png"), (self.cell_size, self.cell_size))

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
            # listen for mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if right click, set type to flag
                if pygame.mouse.get_pressed()[2]:
                    self.type = "f"
                elif pygame.mouse.get_pressed()[0]:
                    self.type = "click"
                # get mouse position and calculate grid square
                cell_size = min([int(1000 / self.n), int(1000 / self.m)])
                mouse_pos = pygame.mouse.get_pos()
                # row of click
                self.x = round(mouse_pos[1] / cell_size - 0.5)
                # column of click
                self.y = round(mouse_pos[0] / cell_size - 0.5)
                print(f"x: {self.x}, y:{self.y}, type:{self.type}")
                print(f"Mines: {self.mines}, Flags: {self.flags}, Flagged Mines: {self.mines_flagged}")
                
    def update(self):
        i = self.x
        j = self.y
        # add flag to player view
        if self.type == "f":
            self.player_grid[i, j] = "F"
            # record flag and if it is correct
            self.flags += 1
            if self.ref_grid[i, j] == -1:
                self.mines_flagged += 1
        # check normal move: explode mine or record info on player grid
        elif self.type == "click":
            # if mine: explode
            if self.ref_grid[i, j] == -1:
                print("You lose!")
                self.player_grid[i, j] = "*"
                self.running = False
            # if not mine: display value
            else:
                self.player_grid[i, j] = self.ref_grid[i, j]

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
                            self.ref_grid[pos]
                            # NEW TRIAL CONDITION
                            if pos[0] >= 0 and pos[1] >= 0:
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
                if self.ref_grid[i, j] == 0:
                    self.ref_grid, self.player_grid = zero_method(i, j, self.ref_grid, self.player_grid)
                # if not, call on any neighbouring zeros
                else:
                    nbs = neighbours(i, j)
                    for pos in nbs:
                        if self.ref_grid[pos] == 0:
                            self.ref_grid, self.player_grid = zero_method(pos[0], pos[1], self.ref_grid, self.player_grid)

        # check if all mines flagged
        #if self.mines == self.flags and self.mines == self.mines_flagged:
        #    print("You win!")
        #    self.running = False

        # check if flags match up with mines
        mine_x = list(np.where(self.ref_grid == -1)[0])
        mine_y = list(np.where(self.ref_grid == -1)[1])
        flag_x = list(np.where(self.player_grid == "F")[0])
        flag_y = list(np.where(self.player_grid == "F")[1])
        if (mine_x == flag_x) and (mine_y == flag_y):
            print("You win! location")
            self.running = False

    def render(self):
        """Draw an m x n (row x col) grid of squares, with numbers and flags."""
        # for each corner in grid, draw rectangle
        #for x in range(0, cell_size * n, cell_size):
        for j in range(0, self.n):
            #for y in range(0, cell_size * m, cell_size):
            for i in range(0, self.m):
                # coordinates
                x = j * self.cell_size
                y = i * self.cell_size
                # grid entry
                entry = self.player_grid[i,j]
                if entry == "-":
                    self.window.blit(self.spriteunrevealed, (x,y))
                elif entry == "F":
                    self.window.blit(self.spritef, (x,y))
                elif entry == "0":
                    self.window.blit(self.spriterevealed, (x,y))
                elif entry == "1":
                    self.window.blit(self.sprite1, (x,y))
                elif entry == "2":
                    self.window.blit(self.sprite2, (x,y))
                elif entry == "3":
                    self.window.blit(self.sprite3, (x,y))
                elif entry == "4":
                    self.window.blit(self.sprite4, (x,y))
                elif entry == "5":
                    self.window.blit(self.sprite5, (x,y))
                elif entry == "6":
                    self.window.blit(self.sprite6, (x,y))
                elif entry == "7":
                    self.window.blit(self.sprite7, (x,y))
                elif entry == "8":
                    self.window.blit(self.sprite8, (x,y))

                #rect = pygame.Rect(x, y, cell_size, cell_size)
                #pygame.draw.rect(window, (200,200,200), rect, 1)
                #location = pygame.math.Vector2(x * cell_size, y * cell_size)
                #window.blit(sprite2, rect, rect)
                #sprite2 = pygame.transform.scale(pygame.image.load("two.png"), (cell_size, cell_size))
                #self.window.blit(sprite2, (x,y))
        pygame.display.update()    

    def run(self):    
        while self.running:
            self.processInput()
            self.update()
            self.render()      
            self.clock.tick(60)
        pygame.quit()
