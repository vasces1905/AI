from dice_game import DiceGame
from agent import MyAgent
import numpy as np
import matplotlib.pyplot as plt

dict_gamma = {}
dict_theta = {}


def play_game_with_agent(agent, game, verbose=False):
    state = game.reset()

    if verbose:
        print(f"Testing agent: \n\t{type(agent).__name__}")
    if verbose:
        print(f"Starting dice: \n\t{state}\n")

    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1

        if verbose: print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if verbose and not game_over:
            print(f"Dice: \t\t{state}")

    if verbose:
        print(f"\nFinal dice: {state}, score: {game.score}")

    return game.score


def tests(_gamma, _theta, test_parameter):
    import time

    total_score = 0
    total_time = 0
    n = 10000

    np.random.seed()

    if test_parameter == "gamma":
        print(f"Testing gamma value: {_gamma}")
    elif test_parameter == "theta":
        print(f"Testing theta value: {_theta}")

    game = DiceGame()

    start_time = time.process_time()
    test_agent = MyAgent(game)
    test_agent.set_parameters(_gamma, _theta)
    total_time += time.process_time() - start_time

    for i in range(n):
        start_time = time.process_time()
        score = play_game_with_agent(test_agent, game)
        total_time += time.process_time() - start_time
        total_score += score

    return total_score / n


if __name__ == "__main__":
    def_gamma = 0.9
    def_theta = 0.01
    # Test gamma values
    for gamma in np.arange(def_gamma, 1.01, 0.01):
        dict_gamma[gamma] = tests(gamma, def_theta, "gamma")

    # Test theta values
    for theta in np.arange(def_theta, 1.1, 0.01):
        dict_theta[theta] = tests(def_gamma, theta, "theta")

    # Plot WSS Graph
    plt.plot(dict_gamma.keys(), dict_gamma.values(), 'bx-')
    plt.xlabel('Gamma')
    plt.ylabel('Avg. Score')
    plt.title('Avg. Score vs Gamma')
    plt.show()

    # Plot Silhouette Scores
    plt.plot(dict_theta.keys(), dict_theta.values(), 'bx-')
    plt.xlabel('Theta')
    plt.ylabel('Avg. Score')
    plt.title('Avg. Score vs Theta')
    plt.show()
