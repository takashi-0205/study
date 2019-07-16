import random

class Card:
    SUITS = "♣♦♥♠"
    RANKS = "A23456789TJQK"

    def __init__(self, suit, rank=""):
        self.suit = suit
        self.rank = rank.replace("T", "10")
        self.number = rank and Card.RANKS.index(rank) + 1 or 0
        self.label = self.suit + self.rank

    def __repr__(self):
        return self.label
        
class Dealer:

    @staticmethod
    def deal(players,which_game):
        cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        
        if which_game.lower() in ["b","bubb"]:
            cards += [Card("Joker")]
        elif which_game.lower() in ["j","jiji"]:
            random.shuffle(cards)
            cards.pop(0)
        random.shuffle(cards)
        for i, card in enumerate(cards):
            players[i % len(players)].hold(card)