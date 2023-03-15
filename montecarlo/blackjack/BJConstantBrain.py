from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory


class BJConstantBrain(BJBrain):

    def __init__(self, threshold):
        self.threshold = threshold

    def make_decision(self, history: BJSinglePlayerHistory) -> BJAction:
        if history.get_player_score() < self.threshold:
            return BJAction.HIT
        return BJAction.STICK
