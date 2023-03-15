import random

from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory


class BJRandomBrain(BJBrain):

    def __init__(self, threshold):
        self.threshold = threshold

    def make_decision(self, history: BJSinglePlayerHistory) -> BJAction:
        score = history.get_player_score()
        if score < self.threshold:
            if score < 11:
                return BJAction.HIT
            return BJAction(random.randrange(0, 2))
        return BJAction.STICK

