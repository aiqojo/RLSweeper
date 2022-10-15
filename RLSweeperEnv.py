import gym
from gym import spaces
import numpy as np
import Board


class RLSweeperEnv(gym.Env):
    metadata = {"render.modes": {"human"}}

    def __init__(self):
        
        self.reward = 0
        x = 10
        y = 10
        perc = 0.2
        self.board = Board.Board(x, y, perc)
        self.prev_revealed = 0

        self.first = True
        self.done = False
        
        # so we can cut agent off and it doesn't go on forever
        self.moves = 0
        self.max_moves = self.board.x * self.board.y

        self.action_space = spaces.Box(shape=(2,), low=0, high=1, dtype=np.float32)
        self.observation_space = spaces.Box(shape=(x, y), low=-1, high=8, dtype=np.float32)

    # agent will give 2d np array with x in [0] and y in [1]
    # agent wont have ability to flag

    ## reward
    # +1 for each cell revealed
    # -2 if it doesn't reveal a cell with a move
    # -5 for an invalid move
    # -(x*y)/2 for losing
    # +(x*y)/2 for winning
    # -(x*y)/4 for running out of moves
    def step(self, loc):
        # print("LOC: ", loc)
        x = loc[0].astype(int)
        y = loc[1].astype(int)

        valid_move = self.board.check_bounds(x, y)

        if valid_move:
            game_state = self.board.input_handler(x, y, False, self.first)
        else:
            # not a valid move, penalize
            self.reward += -5

        # finds the amount that was revealed from the previous move
        rev_count = self.board.revealed - self.prev_revealed
        # print("prev: ", self.prev_revealed, "revealed: ", self.board.revealed, "rev_count: ", rev_count)
        if rev_count > 0:
            # if it is greater than 0, the agent revealed rev_count cells
            # give it a reward for that
            self.reward += rev_count
            self.prev_revealed = self.board.revealed
        else:
            # if it is 0, the agent did not reveal any new cells
            # penalize it for that
            self.reward += -2


        self.moves += 1
        
        self.first = False
        if game_state == "LOST":
            self.reward += -(self.board.x * self.board.y) // 2
            self.done = True
        elif game_state == "WON":
            self.reward += (self.board.x * self.board.y) // 2
            self.done = True
        elif self.moves >= self.max_moves:
            self.reward += -(self.board.x * self.board.y) // 4
            self.done = True

        return self.board.rl_return(), self.reward, self.done, {}

    def reset(self):
        self.reward = 0

        self.board = Board.Board(self.board.x, self.board.y, self.board.mine_percentage)
        self.first = True
        self.done = False

        self.moves = 0
        self.max_moves = self.board.x * self.board.y

        return self.board.rl_return()

    def render(self, mode="human"):
        if mode == "human":
            self.board.print_board()
        elif mode == "rl":
            rl_print = self.board.rl_return()
            for row in self.rl_print:
                for cell in row:
                    if cell == 10:
                        print("   #", end="")
                    elif cell == -1:
                        print("   -", end="")
                    elif cell == -2:
                        print("   X", end="")
                    else:
                        print("   %d" % cell, end="")
                print("\n")
            print("\n")
