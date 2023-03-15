from montecarlo.blackjack.BJConstantBrain import BJConstantBrain
from montecarlo.blackjack.BJDealerBrain import BJDealerBrain
from montecarlo.blackjack.BJOptimalBrain import BJOptimalBrain
from montecarlo.blackjack.BJPlayer import BJPlayer
from montecarlo.blackjack.BJSinglePlayerGame import BJSinglePlayerGame
from montecarlo.cardgames import DeckSuitBuilder
from montecarlo.cardgames.Deck import Deck

dealer = BJPlayer(brain=BJDealerBrain())
deck = Deck(card_scores_builder_function=DeckSuitBuilder.black_jack_scores)


def stand():
    games_count = 1000000
    players = {
                "constant17": BJPlayer(brain=BJConstantBrain(17)),
                "constant16": BJPlayer(brain=BJConstantBrain(16)),
                "constant15": BJPlayer(brain=BJConstantBrain(15)),
                "constant14": BJPlayer(brain=BJConstantBrain(14)),
                "constant13": BJPlayer(brain=BJConstantBrain(13)),
                "constant12": BJPlayer(brain=BJConstantBrain(12)),
                "constant11": BJPlayer(brain=BJConstantBrain(11)),
                "millionGames": BJPlayer(brain=BJOptimalBrain("million_games")),
               }
    track_results1 = {}
    for player_prop in players.items():
        name = player_prop[0]
        player1 = player_prop[1]
        cumulative_reward1, track_rewards1 = play_stand(player1, games_count)
        track_results1[name] = cumulative_reward1
        print(name + ": " + str(cumulative_reward1) + " " + str(round(cumulative_reward1 / games_count, 4)))
    show_info(track_results1)


def play_stand(player: BJPlayer, game_count) -> (int, []):
    cumulative_reward = 0
    track_rewards = []
    game = BJSinglePlayerGame(player, dealer, deck, allow_two_aces_on_start=True)
    for i in range(game_count):
        history = game.play()
        cumulative_reward += history.reward
        track_rewards.append(cumulative_reward)
    return cumulative_reward, track_rewards


def show_info(results):
    # graph should be here
    pass


if __name__ == '__main__':
    stand()
