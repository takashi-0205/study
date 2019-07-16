#-* coding:utf-8 -*-
import random

class EmptyError(Exception):
    pass

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

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
    
    def deal(self,players,which_game):
        if which_game.lower() in ["b","bubb"]:
            self.cards += [Card("Joker")]
        elif which_game.lower() in ["j","jiji"]:
            random.shuffle(self.cards)
            self.cards.pop(0)
        random.shuffle(self.cards)
        for i, card in enumerate(self.cards):
            players[i % len(players)].hold(card)
    
    def draw(self):
        #print(self.cards)
        card_size = len(self.cards)
        if card_size == 0:
            raise  EmptyError
        number = random.randint(1,card_size)
        return self.cards.pop(number - 1)
    
    def release(self,card):
        self.cards.append(card)