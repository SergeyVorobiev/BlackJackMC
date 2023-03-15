from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerGame import black_jack_resources_path
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory
import pandas as pd


class BJOptimalBrain(BJBrain):

    def __init__(self, file_name, file_path=None):
        if file_path is None:
            file_path = black_jack_resources_path
        path = file_path + "/" + file_name + ".csv"
        data = pd.read_csv(path)
        self.table = []
        for score in range(4, 22):
            dealer_cards = []
            self.table.append(dealer_cards)
            for dealer_card in range(2, 12):
                dealer_cards.append(0)
        for i in range(len(data)):
            score = data["PlayerScore"][i]
            dealer_card = data["DealerCard"][i]
            action = data["Action"][i]
            self.table[score - 4][dealer_card - 2] = action

    def make_decision(self, history: BJSinglePlayerHistory) -> BJAction:
        score = history.get_player_score()
        dealer_card = history.get_dealer_shown_card()
        if score < 11:
            return BJAction.HIT
        if score < 22:
            action = self.table[score - 4][dealer_card - 2]
            return BJAction(action)
        return BJAction.STICK
