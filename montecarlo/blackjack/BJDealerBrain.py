from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory


class BJDealerBrain(BJBrain):

    def make_decision(self, history: BJSinglePlayerHistory) -> BJAction:
        score = history.get_dealer_score()
        if score >= 17:
            return BJAction.STICK
        return BJAction.HIT
