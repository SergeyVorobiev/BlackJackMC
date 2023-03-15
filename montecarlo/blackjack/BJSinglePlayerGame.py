import os

from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJPlayer import BJPlayer
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory
from montecarlo.cardgames.Deck import Deck
import pandas as pd

black_jack_resources_path = os.path.join(os.path.dirname(__file__), "resources")


class BJSinglePlayerGame(object):

    def __init__(self, player: BJPlayer, dealer: BJPlayer, deck: Deck, allow_two_aces_on_start=True):
        self.allow_two_aces_on_start = allow_two_aces_on_start
        self.player: BJPlayer = player
        self.dealer: BJPlayer = dealer
        self.deck: Deck = deck
        self.history = BJSinglePlayerHistory()

    def __get_started_distribution(self):
        self.history.reset()
        if self.allow_two_aces_on_start:
            self.deck.shuffle()
        else:
            score = 22
            while score > 21:
                score = 0
                self.deck.shuffle()
                score += self.deck.show_first_card().get_score()
                score += self.deck.show_card_with_number(3).get_score()
        self.player.add_card(self.__take_card_from_deck())
        self.dealer.add_card(self.__take_card_from_deck())
        self.player.add_card(self.__take_card_from_deck())
        self.dealer.add_card(self.__take_card_from_deck())

        # At start prev sum should be equal to sum on hand in case if we will decide to not take the card
        self.player.set_prev_sum_as_sum_on_hand()
        self.history.set_player_score(self.player.get_score())
        self.history.set_dealer_score(self.dealer.get_score())
        self.history.dealer_shown_card = self.dealer.hand[0]

    def __take_card_from_deck(self):
        return self.deck.remove_first_card().get_score()

    def __cards_taking(self, player: BJPlayer, is_player: bool):
        continue_ = True
        while continue_:
            action = player.get_action(self.history)
            player_prev_hand = player.hand.copy()
            prev_score = player.get_score()
            if action == BJAction.HIT:
                player.add_card(self.__take_card_from_deck())
            else:
                continue_ = False
            if is_player:
                if prev_score < 22:
                    self.history.add_state(player_prev_hand, player.hand, player.get_score(), prev_score, action.value)
            else:
                self.history.set_dealer_score(player.get_score())

    def __game_result(self):
        player_score = self.player.get_score()
        dealer_score = self.dealer.get_score()
        reward = 0
        if player_score > 21:
            reward = -1
        elif dealer_score > 21 or player_score > dealer_score:
            reward = 1
        elif player_score < dealer_score:
            reward = -1
        self.history.set_reward(reward)
        return self.history

    def play(self) -> BJSinglePlayerHistory:
        self.player.discard()
        self.dealer.discard()
        self.deck.new_deck()
        self.__get_started_distribution()
        self.__cards_taking(self.player, is_player=True)
        self.__cards_taking(self.dealer, is_player=False)
        return self.__game_result()

    def register_new_state_callback(self, new_state_callback):
        self.history.register_new_state_callback(new_state_callback)

    # deprecated
    @staticmethod
    def save_episodes(episodes, file_name, folder_path=None):
        if folder_path is None:
            folder_path = black_jack_resources_path
        file_path = folder_path + "/" + file_name + ".csv"
        array = []
        for episode in episodes:
            episode_size = len(episode)
            last_step = episode_size - 1
            for i in range(episode_size):
                episode_step = episode[i]
                scores = episode_step[0]
                player_score = scores[0]
                dealer_card = scores[1]
                action = episode_step[1]
                reward = episode_step[2]
                if i == last_step:
                    end_episode_signal = 1
                else:
                    end_episode_signal = 0
                array.append([player_score, dealer_card, action, reward, end_episode_signal])
        data = pd.DataFrame(data=array, columns=["PlayerScore", "DealerCard", "Action", "Reward", "EndEpisodeSignal"])
        data.to_csv(file_path, index=False)

    # not done yet
    @staticmethod
    def load_episodes(path):
        df = pd.read_csv(path)
