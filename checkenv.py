from RLSweeperEnv import RLSweeperEnv
import numpy as np
import time

env = RLSweeperEnv()
env.reset()

episodes = 10

for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        n_state, reward, done = env.step(action)
        print("LOC: ", action)
        print("Reward: ", reward)
        score += reward
        # env.board.print_grid()
        print("\n")
        env.board.print_board()
        time.sleep(2)

    print("Episode: {} Score: {}".format(episode, score))
