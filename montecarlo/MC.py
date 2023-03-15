from graphics import GraphWin

from montecarlo.grid import VisualGrid
from montecarlo.grid.DrawGrid import DrawGrid
from montecarlo.sap.Action import Action
from montecarlo.sap.EGreedyPolicy import EGreedyPolicy
from montecarlo.sap.Policy import Policy
from montecarlo.sap.State import State
from montecarlo.grid import Cell
from montecarlo.grid.GridWorldPolicy import update_policy_colors_grid
from montecarlo.StateInfoMap import StateInfoMap
from montecarlo.blackjack.BJDealerBrain import BJDealerBrain
from montecarlo.blackjack.BJEpisodeGenerator import BJEpisodeGenerator
from montecarlo.blackjack.BJLearnBrain import BJLearnBrain
from montecarlo.blackjack.BJPlayer import BJPlayer
from montecarlo.blackjack.BJSinglePlayerGame import BJSinglePlayerGame
from montecarlo.blackjack.BJStateInfoMap import BJStateInfoMap
from montecarlo.cardgames import DeckSuitBuilder
from montecarlo.cardgames.Deck import Deck

win = GraphWin('BlackJack', 1800, 1100)


class MC(object):

    def __init__(self, state_info_map: StateInfoMap):
        self.state_info_map: StateInfoMap = state_info_map
        self.__sample_callback = lambda state: 0
        self.__episodes_callback = lambda count: 0
        self.callback_episodes_count = 0
        self.discount = 1
        self.__episode_getter = self.__default_episode_getter
        self.all_count = 0

    def register_sample_callback(self, sample_callback):
        self.__sample_callback = sample_callback

    def register_episodes_callback(self, episodes_callback, episodes_count):
        self.__episodes_callback = episodes_callback
        self.callback_episodes_count = episodes_count

    def __default_episode_getter(self) -> [] or None:
        return None

    def register_episode_getter(self, episode_getter):
        self.__episode_getter = episode_getter

    @staticmethod
    def __update_q(action: Action, g):
        q = action.q
        action.visit_count += 1
        alpha = 1 / action.visit_count
        next_q = q + alpha * (g - q)
        action.q = next_q

    # On policy control soft meaning (all actions have p > 0)
    def evaluate_v(self):
        k = 0
        callback_episodes = 0
        episode: [] or None = self.__episode_getter()
        update_policy_count = 100
        update_policy = 0
        while episode is not None:
            update_policy += 1
            k += 1
            callback_episodes += 1
            last = episode.__len__() - 1
            g = 0
            for i in range(last - 1, -1, -1):
                step = episode[i]
                next_step = episode[i + 1]
                info = [step[0], step[1]]
                #if info[0] < 11:
                #    continue
                raw_action = step[2]
                next_reward = next_step[3]
                g = next_reward + self.discount * g
                state: State = self.state_info_map.get_state(info)
                if raw_action is None:
                    break
                #state.g += g
                #state.visit_count += 1
                #state.v = state.g / state.visit_count
                MC.__update_q(state.get_action_by_key(raw_action), g)
                #Policy.make_actions_optimal_by_q_in_state(state)
                self.__sample_callback(state)
            if update_policy > update_policy_count:
                update_policy = 0
                Policy.make_actions_optimal_by_q(self.state_info_map.get_states())
            if self.callback_episodes_count > 0 and self.callback_episodes_count == callback_episodes:
                callback_episodes = 0
                self.all_count += self.callback_episodes_count
                self.__episodes_callback(self.all_count)
            episode = self.__episode_getter()


dealer = BJPlayer(brain=BJDealerBrain())
deck = Deck(card_scores_builder_function=DeckSuitBuilder.black_jack_scores)

i = 0


def episodes_callback1(count):
    print(str(count))
    for state in info_map.get_states():
        state.update_visual()
    cell: Cell
    for x in grid:
        for cell in x:
            cell.update_text()
    update_policy_colors_grid(grid, lambda c: c.optimal_q)


if __name__ == '__main__':
    game_count1 = 1000000
    greedy_factor = 0.9
    episodes_count_update = 1000
    file_name = "million_games"
    grid = VisualGrid.build_grid(win, width=18, height=10, start_rect_x=10, start_rect_y=10, cell_size_x=95, cell_size_y=70)
    draw_grid = DrawGrid(grid)
    draw_grid.draw()
    win.getMouse()
    print("Start to generate episodes")
    info_map = BJStateInfoMap(grid)
    policy = EGreedyPolicy(greedy_factor)
    brain = BJLearnBrain(policy, info_map)
    player1 = BJPlayer(brain=BJLearnBrain(policy, info_map))
    game: BJSinglePlayerGame = BJSinglePlayerGame(player1, dealer, deck)
    generator: BJEpisodeGenerator = BJEpisodeGenerator(game, game_count1)
    #episodes1 = game.generate_episodes(game_count1)
    #game.generate_episode()
    #BJSinglePlayerGame.save_episodes(episodes1, "ten_millions_episodes")
    print("Episodes generated")
    mc = MC(info_map)
    #mc.register_sample_callback(callback)
    mc.register_episodes_callback(episodes_callback1, episodes_count_update)
    mc.register_episode_getter(generator.get_episode)
    mc.evaluate_v()
    brain.save_policy(file_name)
    win.getMouse()
