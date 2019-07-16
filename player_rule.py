#-* coding:utf-8 -*-
import random
import sys

"""
ババ(ジジ)抜きで使うものには☆
ブラックジャックで使うものには□
神経衰弱で使うものには△
07/16 ローカルに複数回コミットした際の挙動検証
"""

class Player:

    def __init__(self, name,id):
        if not id is None:
            self.id = id + 1
        self.name = name
        self.cards = []

    def hold(self, card):
        self.cards.append(card)

    def release(self, card):
        self.cards.remove(card)

    def input_number(self, number_of_cards):
        while True:
            pull_card = input("Please choose from the following numbers or [hand]\n"+ str(list(range(number_of_cards))) + "\n>>>")
            if not len(pull_card) == 0:
                if pull_card.isdecimal():
                    if int(pull_card) in list(range(number_of_cards)):
                        return pull_card
                if pull_card.lower() in ["h", "hand"]:
                    print(self.cards)
                elif pull_card.lower() in ["q", "quit"]:
                    print("Good Bye.")
                    sys.exit()
                else:
                    print("Invalid value. Please input correct number.")
            else:
                print("Please enter something.")

    #☆
    def drop_pairs(self):
        dropped_cards = []
        cards = sorted(self.cards, key=lambda card: card.number)
        for i in range(len(cards) - 1):
            if cards[i] and cards[i].rank == cards[i + 1].rank:
                dropped_cards += [cards[i], cards[i + 1]]
                cards[i] = cards[i + 1] = None
        self.cards = [card for card in self.cards if card not in dropped_cards]
        return dropped_cards

    #☆ 一部nerv_playと類似するから共通化したいけど抽象化としては早すぎるだろうか…
    def bubb_play(self, next_player,mode):
        if self.id == 1 and mode is False:
            hand = len(next_player.cards)
            pull_card = self.input_number(hand)
            card = next_player.cards[int(pull_card)]
        else:
            card = random.choice(next_player.cards)
        next_player.release(card)
        self.hold(card)
        return card, self.drop_pairs()

    #☆
    def win(self):
        return not self.cards

    #□
    def get_total_value(self):
        def adjust(number):
            return number if number <= 10 else 10
        if len(self.cards) ==0:
            return 0
        pre_total = sum([adjust(card.number) for card in self.cards])
        found = next( (card for card in self.cards if card.number == 1) ,None)
        if pre_total <= 11 and found:
            pre_total += 10
        return pre_total

    #□
    def print_hold_card(self):
        print("-- [{0}] --".format(self.name))
        for cards in self.cards:
            print("[{0}]".format(cards.label))
        print("--------------")
        print("Total: {0}".format(self.get_total_value()))

    #△ 一部bubb_playと類似するから共通化したいけど抽象化としては早すぎるだろうか…
    def nerv_play(self,deck,mode):
        if self.id == 1 and mode is False:
            hand = len(deck.cards)
            pull_card = self.input_number(hand)
            card = deck.cards[int(pull_card)]
        else:
            card = random.choice(deck.cards)
        print(card)
        deck.cards.remove(card)
        self.hold(card)
        