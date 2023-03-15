class Card(object):

    def __init__(self, value, suit, name, score):
        self.__value = value
        self.__suit = suit
        self.__name = name
        self.__score = score
        self.__view = [value, suit, name, score]

    def __str__(self):
        return str(self.__view)

    def get_value(self):
        return self.__value

    def get_score(self):
        return self.__score

    def get_suit(self):
        return self.__suit

    def get_name(self):
        return self.__name

    def set_score(self, score):
        self.__score = score
        self.__view[3] = score
