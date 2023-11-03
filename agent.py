from abc import ABC, abstractmethod
from dice_game import DiceGame
import numpy as np

GAMMA, THETA = 0.9, 0.1


class DiceGameAgent(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def play(self, state):
        pass


class AlwaysHoldAgent(DiceGameAgent):
    def play(self, state):
        return (0, 1, 2)


class PerfectionistAgent(DiceGameAgent):
    def play(self, state):
        if state == (1, 1, 1) or state == (1, 1, 6):
            return (0, 1, 2)
        else:
            return ()


class Node:
    def __init__(self, action, value):
        self.value = value
        self.action = action


class MyAgent(DiceGameAgent):
    def __init__(self, game):
        """
        if your code does any pre-processing on the game, you can do it here

        e.g. you could do the value iteration algorithm here once, store the policy,
        and then use it in the play method

        you can always access the game with self.game
        """
        # this calls the superclass constructor (does self.game = game)
        super().__init__(game)

        self.memoization_table = {}
        self.state_dict = {state: Node((), 0) for state in self.game.states}

        delta = 1 + THETA

        while delta >= THETA:
            delta = 0

            for state in self.game.states:
                temp = self.state_dict[state].value
                self.state_dict[state].action, self.state_dict[state].value = self.get_max_value(state)
                delta = max(delta, abs(temp - self.state_dict[state].value))

    def play(self, state):
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice

        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions

        read the code in dicegame.py to learn more
        """
        return self.state_dict[state].action

    def memoization(self, action, _state):
        if (action, _state) not in self.memoization_table:
            self.memoization_table[(action, _state)] = self.game.get_next_states(action, _state)
        return self.memoization_table[(action, _state)]

    def get_max_value(self, _state):

        chosen_action, max_value = None, -10000

        for action in self.game.actions:
            temp_value = 0
            states, game_over, reward, probabilities = self.memoization(action, _state)

            for state, probability in zip(states, probabilities):
                if not game_over:
                    temp_value += probability * (reward + GAMMA * self.state_dict[state].value)
                else:
                    temp_value += probability * (reward + GAMMA * self.game.final_score(_state))

            if temp_value > max_value:
                max_value = temp_value
                chosen_action = action

        return chosen_action, max_value

    @staticmethod
    def set_parameters(gamma, theta):
        global GAMMA, THETA
        GAMMA = gamma
        THETA = theta
