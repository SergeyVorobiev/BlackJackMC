from abc import abstractmethod

from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory


class BJBrain(object):

    @abstractmethod
    def make_decision(self, state: BJSinglePlayerHistory) -> BJAction:
        ...
