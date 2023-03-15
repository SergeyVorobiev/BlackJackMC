from montecarlo.cardgames.Card import Card

card_names36 = [["6" "C", "6 Club"], "6 diamond", "6 heart", "6 spade",
                "7 club", "7 diamond", "7 heart", "7 spade",
                "8 club", "8 diamond", "8 heart", "8 spade",
                "9 club", "9 diamond", "9 heart", "9 spade",
                "10 club", "10 diamond", "10 heart", "10 spade",
                "J club", "J diamond", "J heart", "J spade",
                "Q club", "Q diamond", "Q heart", "Q spade",
                "K club", "K diamond", "K heart", "K spade",
                "A club", "A diamond", "A heart", "A spade", ]

card_names52 = ["2 club", "2 diamond", "2 heart", "2 spade",
                "3 club", "3 diamond", "3 heart", "3 spade",
                "4 club", "4 diamond", "4 heart", "4 spade",
                "5 club", "5 diamond", "5 heart", "5 spade"] + card_names36

card_names54 = card_names52 + ["Black Joker", "Red Joker"]


def create_52() -> [Card]:
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    suits = ["C", "D", "H", "S"]
    names = ["Club", "Diamond", "Heart", "Spade"]
    cards = []
    for v in values:
        for i in range(len(suits)):
            score = 0
            value = str(v)
            suit = suits[i]
            name = names[i]
            full_name = value + " " + name
            cards.append(Card(value, suit, full_name, score))
    return cards


def black_jack_scores(cards: [Card]):
    scores = {"2": 2,
              "3": 3,
              "4": 4,
              "5": 5,
              "6": 6,
              "7": 7,
              "8": 8,
              "9": 9,
              "10": 10,
              "J": 10,
              "Q": 10,
              "K": 10,
              "A": 11}
    for c in cards:
        c: Card = c
        value = c.get_value()
        score = scores[value]
        c.set_score(score)
