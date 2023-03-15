
class BJSinglePlayerHistory(object):

    def __init__(self):
        self.__player_hand: [] = []
        self.__dealer_hand: [] = []
        self.dealer_shown_card: int = 0
        self.states = []
        self.__player_hand_sum = 0
        self.__dealer_hand_sum = 0
        self.__dealer_score = 0
        self.__new_state_callback = lambda state: 0
        self.reward = 0

    def reset(self):
        self.__player_hand: [] = []
        self.__dealer_hand: [] = []
        self.dealer_shown_card: int = 0
        self.states = []
        self.__player_hand_sum = 0
        self.__dealer_hand_sum = 0
        self.__player_prev_sum = 0

    def get_dealer_shown_card(self) -> int:
        return self.dealer_shown_card

    def set_dealer_shown_card(self, shown_card: int):
        self.dealer_shown_card = shown_card

    def set_reward(self, reward: int):
        self.reward = reward

    def set_player_score(self, sum_: int):
        self.__player_hand_sum = sum_

    def get_player_score(self) -> int:
        return self.__player_hand_sum

    def get_dealer_score(self) -> int:
        return self.__dealer_score

    def set_dealer_score(self, score: int):
        self.__dealer_score = score

    def add_state(self, player_prev_hand: [], player_hand: [], player_hand_sum: int, player_prev_sum: int, action: int):
        self.__player_hand_sum = player_hand_sum
        self.__player_prev_sum = player_prev_sum
        state = [player_prev_hand.copy(), self.__player_prev_sum, action, player_hand.copy(), self.__player_hand_sum]
        self.states.append(state)
        self.__new_state_callback(state)
        return self

    def register_new_state_callback(self, new_state_callback):
        self.__new_state_callback = new_state_callback

    def form_report(self) -> []:
        size = len(self.states)
        result = []
        for i in range(size):
            state = self.states[i]
            result.append([state[1], self.dealer_shown_card, state[2], 0])  # hand, show_card, action, reward
        last_state = self.states[size - 1]
        result.append([last_state[1], self.dealer_shown_card, -1, self.reward])
        return result

    def __str__(self):
        return "Player hand: " + str(self.__player_hand) + " score: " + str(self.__player_hand_sum) + "\n" + "Dealer hand: " + str(self.__dealer_hand) + " score: " + str(self.__dealer_hand_sum) + " shown card: " + str(self.dealer_shown_card)
