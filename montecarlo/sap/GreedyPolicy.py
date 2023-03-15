import random

from montecarlo.sap.Action import Action
from montecarlo.sap.Policy import Policy
from montecarlo.sap.State import State


class GreedyPolicy(Policy):

    def __init__(self):
        super().__init__()

    def pick_action(self, state: State) -> Action:
        optimal_actions = state.get_optimal_actions()
        optimal_keys: [] = state.get_optimal_action_keys()
        key = optimal_keys[random.randrange(0, optimal_keys.__len__(), 1)]
        return optimal_actions[key]

    def pick_actions(self, state: State) -> {object: Action}:
        return state.get_optimal_actions()
