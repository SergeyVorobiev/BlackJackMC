import random

from montecarlo.cardgames import DeckSuitBuilder
from montecarlo.cardgames.Card import Card


class Deck(object):

    def __init__(self, deck_suit_builder=DeckSuitBuilder.create_52, copy_card_deck=None, card_scores_builder_function=None):
        self.__card_suits = deck_suit_builder()
        if card_scores_builder_function is not None:
            card_scores_builder_function(self.__card_suits)
        self.__card_deck = []
        if copy_card_deck is not None:
            self.__card_deck = list(copy_card_deck)
        else:
            self.new_deck()

    def new_deck(self) -> __qualname__:
        self.__card_deck = list(range(self.__card_suits.__len__()))
        return self

    def get_card_deck(self):
        return list(self.__card_deck)

    def shuffle(self):
        random.shuffle(self.__card_deck)
        return self

    def show_deck(self) -> [Card]:
        deck = []
        for i in self.__card_deck:
            deck.append(self.__card_suits[i])
        return deck

    def show_first_card(self) -> Card:
        return self.show_card_with_number(1)

    def remove_first_card(self) -> Card:
        return self.remove_card_with_number(1)

    def show_last_card(self) -> Card:
        return self.show_card_with_number(self.size())

    def remove_last_card(self) -> Card:
        return self.remove_card_with_number(self.size())

    def show_card_with_number(self, number) -> Card:
        index = self.__card_deck[number - 1]
        return self.__card_suits[index]

    def remove_card_with_number(self, number) -> Card:
        index = self.__card_deck.pop(number - 1)
        return self.__card_suits[index]

    def size(self):
        return len(self.__card_deck)

    def __str__(self):
        result = []
        for card in self.show_deck():
            result.append(card.__str__())
        return str(result)


# if __name__ == '__main__':





