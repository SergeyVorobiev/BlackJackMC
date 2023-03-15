from montecarlo.sap.Action import Action
from montecarlo.sap.Policy import Policy
from montecarlo.StateInfoMap import StateInfoMap
from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerGame import black_jack_resources_path
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory
import pandas as pd


class BJLearnBrain(BJBrain):

    def __init__(self, policy: Policy, info_map: StateInfoMap):
        self.policy: Policy = policy
        self.info_map: StateInfoMap = info_map

    def make_decision(self, history: BJSinglePlayerHistory) -> BJAction:
        player_score = history.get_player_score()
        if player_score < 22:
            dealer_score = history.get_dealer_shown_card()
            state = self.info_map.get_state([player_score, dealer_score])
            action: Action = self.policy.pick_action(state)
            return BJAction(action.key)
        else:
            return BJAction.STICK

    def save_policy(self, file_name, file_path=None):
        if file_path is None:
            file_path = black_jack_resources_path
        path = file_path + "/" + file_name + ".csv"
        array = []
        for state in self.info_map.get_states():
            player_score = state.info[0]
            dealer_card = state.info[1]
            action = self.policy.get_optimal_action(state).key
            array.append([player_score, dealer_card, action])
            data = pd.DataFrame(data=array, columns=["PlayerScore", "DealerCard", "Action"])
            data.to_csv(path, index=False)

