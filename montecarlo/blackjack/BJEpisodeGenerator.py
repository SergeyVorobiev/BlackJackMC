from montecarlo.blackjack.BJSinglePlayerGame import BJSinglePlayerGame


class BJEpisodeGenerator(object):

    def __init__(self, game: BJSinglePlayerGame, count: int):
        self.__game: BJSinglePlayerGame = game
        self.__count: int = count
        self.__episodes = 0

    def get_episode(self):
        episode = None
        if self.__episodes < self.__count:
            episode = self.__game.play().form_report()
        self.__episodes += 1
        return episode

    def reset(self):
        self.__episodes = 0
