from montecarlo.blackjack.BJBrain import BJBrain
from montecarlo.blackjack.BJAction import BJAction
from montecarlo.blackjack.BJSinglePlayerHistory import BJSinglePlayerHistory


class BJPlayer(object):

    def __init__(self, brain: BJBrain):
        self.brain = brain
        self.hand = []
        self.prev_sum = 0

    def get_action(self, state: BJSinglePlayerHistory) -> BJAction:
        return self.brain.make_decision(state)

    def add_card(self, card_score):
        self.prev_sum = self.get_score()
        self.hand.append(card_score)

    def set_prev_sum_as_sum_on_hand(self):
        self.prev_sum = self.get_score()

    def get_prev_sum(self) -> int:
        return self.prev_sum

    def get_score(self) -> int:
        sum_ = sum(self.hand)
        if sum_ > 21:
            check = True
            while check:
                is_ace = False
                for i in range(len(self.hand)):
                    value = self.hand[i]
                    if value == 11:
                        is_ace = True
                        self.hand[i] = 1
                        break
                sum_ = sum(self.hand)
                check = sum_ > 21 and is_ace
        return sum_

    def discard(self):
        self.hand = []

if __name__ == '__main__':
    ...
    #player = BJPlayer(BJConstantBrain(20))
    #player.add_card(11)
    #player.add_card(9)
    #player.add_card(10)
    #player.add_card(11)
    #print(player.get_score())
    #print(player.get_prev_sum())
