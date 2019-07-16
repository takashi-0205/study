#-*- coding:utf-8 -*-
import sys
from itertools import count
import master_deck

"""
開発するババ抜き、ジジ抜きのルール
1. 初期カードは52枚
2. プレイヤーに分配する前にジョーカーの追加ないし、ランダムでカードを1枚抜く
3. 揃ったペアをドロップする
4. ドロップしたカードしか確認できない
5. 2～10人で行うかをスクリプトの実行者が決定する
6. 引くカードはスクリプトの実行者が選択する
7. プレイヤーが最後の1人になるまで行う

開発ログ
05/27 オリジナル
05/28 全自動ババ抜きからスクリプトの実行者が引くカードを選ぶ形式に変更
05/29 終了コマンドを入力しない限りババ抜きをプレイできるように
05/30 ジジ抜きの実装
05/30 ジジ抜きとババ抜きを人数決定後に選択できるように変更
06/03 カードクラスを外部に切り出し
"""

class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []

    def hold(self, card):
        self.cards.append(card)

    def release(self, card):
        self.cards.remove(card)

    def drop_pairs(self):
        dropped_cards = []
        cards = sorted(self.cards, key=lambda card: card.number)
        for i in range(len(cards) - 1):
            if cards[i] and cards[i].rank == cards[i + 1].rank:
                dropped_cards += [cards[i], cards[i + 1]]
                cards[i] = cards[i + 1] = None
        self.cards = [card for card in self.cards if card not in dropped_cards]
        return dropped_cards

    def input_number(self, number_of_cards):
        while True:
            pull_card = input("Please choose from the following numbers\n"+ str(list(range(number_of_cards))) + "\n>>>")
            if not len(pull_card) == 0:
                if pull_card.isdecimal():
                    if int(pull_card) in list(range(number_of_cards)):
                        return pull_card
                if pull_card.lower() in ["q", "quit"]:
                    print("Good Bye.")
                    sys.exit()
            print("Invalid value. Please input correct number.")

    def play(self, next_player):
        hand = len(next_player.cards)
        pull_card = self.input_number(hand)
        #card = random.choice(next_player.cards)
        card = next_player.cards[int(pull_card)]
        next_player.release(card)
        self.hold(card)
        return card, self.drop_pairs()

    def win(self):
        return not self.cards

            

class AutoPlay:

    def play(self, player_num,which_game):
        self.players = [Player(f"Player#{i+1}") for i in range(player_num)]
        self.ranking = []

        print("###### Preparation ######")
        master_deck.Dealer.deal(self.players,which_game)
        #self._show_hands()
        self._drop_pairs()
        #self._show_hands()

        print("###### Game Start ######")
        self._show_heavenly_winner()
        turn = count(1)
        while len(self.players) > 1:
            print(f"===== Turn {next(turn)} ======")
            print(f"Playing {len(self.players)} players")
            self._turn()
            #self._show_hands()

        print("###### Game Over ######")
        self._show_ranking()

    def _show_hands(self):
        print("------ Players Hand ------")
        for player in self.players:
            print(f"{player.name} holds {player.cards}")

    def _drop_pairs(self):
        print("------ Drop Pairs ------")
        for player in self.players:
            dropped_cards = player.drop_pairs()
            if dropped_cards:
                print(f"{player.name} dropped {dropped_cards}")

    def _show_heavenly_winner(self):
        for player in self.players[:]:
            if player.win():
                print(f"{player.name} いきなり上がり！")
                self.players.remove(player)
                self.ranking.append(player)

    def _pair_players(self):
        players = self.players[:]
        for i, player in enumerate(players):
            if player.win():
                continue
            for next_player in players[i+1:] + players[:i]:
                if not next_player.win():
                    yield player, next_player
                    break

    def _turn(self):
        for player, next_player in self._pair_players():
            print(player.name + " chooses the card to draw from " + next_player.name)
            pulled_card, dropped_cards = player.play(next_player)
            print(f"{player.name} pulled {pulled_card} from {next_player.name}")
            if next_player.win():
                print(f"{next_player.name} 引かれて上がり！")
                self.players.remove(next_player)
                self.ranking.append(next_player)
            if dropped_cards:
                print(f"{player.name} dropped {dropped_cards}")
            if player.win():
                print(f"{player.name} 引いて上がり！")
                self.players.remove(player)
                self.ranking.append(player)

    def _show_ranking(self):
        print("------ Ranking ------")
        for player in self.ranking + self.players:
            print(player.name)
            

def more_game():
    while True:
        flag = input ("Do you want to continue the game? [Yes/No]\n>>>")
        if flag.lower() in ["y", "yes"]:
            print("☆★☆★☆★☆★")
            return True
        if flag.lower() in ["n", "no"]:
            return False
        if flag.lower() in ["q", "quit"]:
            sys.exit()
        print("Invalid value. Please input yes or no.")


def input_data():
    while True:
        player_num = input("How many Players?\n>>>")
        if player_num.isdecimal():
            if int(player_num) in list(range(2,11)):
                break
            print('Please select in the range of 2 to 10.')
        elif player_num.lower() in ["q", "quit"]:
            print("Good Bye")
            sys.exit()
        else:
            print('Please enter a number.')
    while True:
        which_game = input("Which game do you play?[jiji/bubb]\n>>>")
        if which_game.lower() in ["j", "jiji", "b", "bubb"]:
            AutoPlay().play(int(player_num),which_game)
            break
        elif which_game.lower() in ["q", "quit"]:
            print("Good Bye.")
            sys.exit()
        else:
            print('Please enter a str.')

def main():
    while True:
        input_data()
        if not more_game():
            print("see you again.")
            break

if __name__ == "__main__":
    main()