import numpy as np
import itertools as it

# unrevealed
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# revealed
# 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
# bomb = -1
class Board:

    # https://www.reddit.com/r/Minesweeper/comments/mdbequ/what_is_a_good_mine_ratio/
    # mine percentages

    def __init__(self, x=10, y=10, mine_percentage=0.2):
        self.x = x
        self.y = y
        self.mine_percentage = mine_percentage
        self.grid = np.zeros((self.x, self.y), dtype=int)

    # prints raw info
    def print_grid(self):
        for row in self.grid:
            for cell in row:
                if 0 <= cell < 10:
                    print("   %d" % (cell), end="")
                elif 10 <= cell < 20:
                    print("  %d" % (cell), end="")
                else:
                    print("  %d" % (cell), end="")
            print("\n")

    # prints game board as if you were playing
    def print_board(self):
        for row in self.grid:
            for cell in row:
                # if it is bomb print it with a X
                # if cell == -1:
                #     print("   X", end="")
                #     continue
                if cell == 10:
                    print("   -", end="")
                    continue
                # If greater thatn 10, it has been revealed
                if cell > 10:
                    print("   %d" % (cell % 10), end="")
                else:
                    # \u2b1c
                    print("   #", end="")
            print("\n")
        print("\n")

    def place_mines(self, first_loc):
        mine_count = int(self.x * self.y * self.mine_percentage)

        g = np.linspace(0, self.x * self.y - 1, self.x * self.y, dtype=int)
        g = np.delete(g, first_loc)
        np.random.shuffle(g)

        # give the first mine_count elements a value of -10
        for i in range(mine_count):
            x = g[i] // self.y
            y = g[i] % self.y
            self.grid[x, y] = -1
            self.add_to_near(x, y)

    def add_to_near(self, x, y):
        d = [-1, 0, 1]

        for a, b in it.product(d, d):
            if self.check_bounds(x + a, y + b) and self.grid[x + a, y + b] != -1:
                self.grid[x + a, y + b] += 1

    def rl_return(self):
        return 0

    def check_bounds(self, x, y):
        if (0 <= x < self.x) and (0 <= y < self.y):
            return True
        else:
            return False

    def input_handler(self, x, y, flag, first):
        if first:
            return self.check_mound(x, y, True)
        elif flag:
            return self.set_flag(x, y)
        else:
            return self.check_mound(x, y, False)

    # I dont need to implement this for the rl
    def set_flag(self, x, y):
        pass

    def check_mound(self, x, y, first):
        # First choice - initalize everything else so the first location is never a bomb
        if first:
            loc = x * self.y + y
            self.place_mines(loc)

        if self.grid[x, y] == -1:
            return "LOSE"
        else:
            self.reveal(x, y)
            return "GRUH"

    def reveal(self, x, y):
        if self.grid[x, y] < 10:
            self.grid[x, y] += 10
            if self.grid[x, y] > 10:
                return
        else:
            return

        d = [-1, 0, 1]

        for a, b in it.product(d, d):
            if a == 0 and b == 0:
                continue
            if self.check_bounds(x + a, y + b) and -1 < self.grid[x + a, y + b] < 10:
                self.reveal(x + a, y + b)
