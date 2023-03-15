import random

from montecarlo.math.RMath import RMath
from montecarlo.sap.Action import Action
from montecarlo.sap.Policy import Policy
from montecarlo.sap.State import State


class EGreedyPolicy(Policy):

    def __init__(self, epsilon):
        super().__init__()
        self.epsilon = round(epsilon, 2)

    def pick_action(self, state: State) -> Action:
        value = RMath.get_value(self.epsilon, 0, 1)
        count = state.optimal_actions_count
        size = state.action_size
        if value == 0 or state.optimal_actions_count == size: # All
            index = random.randrange(0, count, 1)
        else:
            index = random.randrange(count, size, 1)
        return state.optimal_actions[index]

    def get_optimal_action(self, state: State) -> Action:
        return state.optimal_actions[0]

    def pick_actions(self, state: State) -> {object: Action}:
        return state.get_optimal_actions()

