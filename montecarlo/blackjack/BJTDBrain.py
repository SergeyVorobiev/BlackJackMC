from montecarlo.grid.Cell import Cell
from montecarlo.sap.EGreedyPolicy import EGreedyPolicy
from montecarlo.sap.Policy import Policy
from montecarlo.sap.State import State
from montecarlo.grid.GridWorldPolicy import update_policy_colors_cells
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJSinglePlayerGame import black_jack_resources_path
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory
from montecarlo.blackjack.BJStateInfoMap import BJStateInfoMap
#from temporaldifference.TD import TD
import pandas as pd


class BJTDBrain(BJBrain):

    def __init__(self, info_map: BJStateInfoMap):
        self.td: TD = TD()
        self.info_map: BJStateInfoMap = info_map
        episodes_count = 20000
        self.td.register_episodes_callback(self.__episodes_callback, episodes_count)
        self.td.register_update_policy_callback(self.__update_policy_callback, update_policy_after_steps_count=500)
        self.prev_last_step = None
        self.last_step = None
        self.policy: Policy = EGreedyPolicy(epsilon=0.96)
        Policy.build_uniform_policy(info_map.get_states())
        self.__value_getter = lambda c: c.v
        self.__cur_state = [0, 0]
        # self.__value_getter = lambda c: c.optimal_q

    def __episodes_callback(self):
        state: State
        visuals = self.info_map.get_visuals()
        for state in self.info_map.get_states():
            cell: Cell = state.visual
            cell.update_text()
        update_policy_colors_cells(visuals, self.__value_getter)

    def __update_policy_callback(self):
        Policy.make_actions_optimal_by_q(self.info_map.get_states())

    def see_state(self, state):
        termination = False
        self.last_step = state
        if self.prev_last_step is not None:
            prev_last_raw_action = self.prev_last_step[2]
            if prev_last_raw_action is None:  # The game is end without our choice (in case black jack for dealer)
                self.prev_last_step = None
                self.last_step = None
                return
            prev_last_state = self.info_map.get_state(self.prev_last_step[0])
            prev_last_action = prev_last_state.get_action_by_key(prev_last_raw_action)
            if prev_last_state is not None:
                reward = self.last_step[3]
                termination = self.last_step[4]
                if termination:
                    self.td.evaluate_v(prev_last_state, reward, termination=termination)
                    self.td.evaluate_q_sarsa(prev_last_state, prev_last_action, reward, termination=termination)
                    #self.nn.evaluate_q_Q_learning(prev_last_state, prev_last_action, reward, termination=termination)
                else:
                    last_state = self.info_map.get_state(self.last_step[0])
                    last_action = last_state.get_action_by_key(self.last_step[2])
                    self.td.evaluate_v(prev_last_state, reward, last_state)
                    self.td.evaluate_q_sarsa(prev_last_state, prev_last_action, reward, last_action)
                    #self.nn.evaluate_q_Q_learning(prev_last_state, prev_last_action, reward, last_state)
        if termination:
            self.prev_last_step = None
            self.last_step = None
        else:
            self.prev_last_step = self.last_step

    def make_decision(self, history: BJSinglePlayerHistory) -> BJAction:
        score = history.get_player_score()
        dealer_card = history.get_dealer_shown_card()
        if score < 11:
            return BJAction.HIT
        elif score > 19:
            return BJAction.STICK
        self.__cur_state[0] = score
        self.__cur_state[1] = dealer_card
        state = self.info_map.get_state(self.__cur_state)
        Policy.make_actions_optimal_by_q_in_state(state)
        raw_action = self.policy.pick_action(state).key
        return BJAction(raw_action)

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
