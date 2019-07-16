#-*- coding:utf-8 -*-
import sys
import random
#import master_deck

"""
開発するブラックジャックのルール
1. 初期カードは52枚
2. 引く際にカードの重複は無いようにする
3. プレイヤーとディーラーの2人対戦
4. プレーヤーは実行者、ディーラーは自動的に実行
5. 実行開始時、プレイヤーとディーラーはそれぞれ、カードを2枚引く。
   引いたカードは画面に表示する。ただし、ディーラーの2枚目のカードは分からないようにする
6. その後、先にプレイヤーがカードを引く。
   プレイヤーが21を超えていたらバースト、その時点でゲーム終了
7. プレーヤーはカードを引くたびに、次のカードを引くか選択できる
8. プレイヤーが引き終えたら、その後ディーラーは、自分の手札が17以上になるように引く
9. プレイヤーとディーラーが引き終えたら勝負。より21に近い方の勝ち
10. JとQとKは10として扱う
11. Aは手札の合計により「1」もしくは「11」として扱う。
12. ダブルダウンなし、すぴりっとなし、サレンダーなし。その他特殊そうなルールなし

開発ログ
05/17 オリジナル
05/17 終了コマンドを入力しない限りブラックジャックをプレイできるように
05/20 勝率の表示
06/03 カードクラスを外部に切り出し作業中(差異を吸収してはいない)
"""

class EmptyError(Exception):
    pass

class Card:
    def __init__(self,name,number):
        def convert(num):
            if num == 1:return 'A'
            if num == 11:return 'J'
            if num == 12:return 'Q'
            if num == 13:return 'K'
            return str(num)

        if not (1 <= number <= 13):
            raise ValueError

        self.name = name
        self.number = number
        #幅取りをしながら表示名を定義
        self.card_name = "{0}|{1:>2}".format(name,convert(number))

#デッキの中身と動作(引かれる)の定義
class PlayerCards:
    def __init__(self):
        self._initialize()

    def _initialize(self):
        names = ["♣", "♦", "♥", "♠"]
        #配列内の要素はCardオブジェクト
        self._cards = [Card(names[i % 4], i % 13 +1) for i in range(52)]

    def new(self):
            self._cards.clear()
            self._initialize()

    def draw(self):
        card_size = len(self._cards)
        if card_size == 0:
            raise  EmptyError
        number = random.randint(1,card_size)
        return self._cards.pop(number - 1)

#プレイヤーの手札の情報(得点など)について定義
class GamePlayer:
    def __init__(self):
        self._hold_cards = []

    def set_card(self, card):
        self._hold_cards.append(card)

    def get_total_value(self):
        def adjust(number):
            return number if number <= 10 else 10
        if len(self._hold_cards) ==0:
            return 0
        pre_total = sum([adjust(card.number) for card in self._hold_cards])
        found = next( (card for card in self._hold_cards if card.number == 1) ,None)
        if pre_total <= 11 and found:
            pre_total += 10
        return pre_total

    def print_hold_card(self, name=None):
        if not name is None:
            print("-- [{0}] --".format(name))
        for cards in self._hold_cards:
            print("[{0}]".format(cards.card_name))
        print("--------------")
        print("Total: {0}".format(self.get_total_value()))

#ブラックジャックのプレイヤーの動作と勝敗について定義
class BlackJackGame:
    def __init__(self):
        self._pcards = PlayerCards()
        self._player = GamePlayer()
        self._dealer = GamePlayer()

    def _draw(self,name,pobj, is_print):
        card = self._pcards.draw()
        pobj.set_card(card)
        if is_print:
            print('[{0}]=>[{1}]'.format(name,card.card_name))
        return pobj.get_total_value() <= 21

    def _print_total(self,name,pobj):
        print('[{0}] total: [{1}]'.format(name,pobj.get_total_value()))

    def _next_draw(self,name,pobj,is_print_draw_card,is_print_total):
        is_safe = self._draw(name,pobj,is_print_draw_card)
        if is_print_total:
            self._print_total(name,pobj)
        return is_safe

    def first_player_draw(self):
        self._draw("Player",self._player,True)
        self._draw("Player",self._player,True)
        self._print_total("Player",self._player)

    def first_dealer_draw(self):
        self._draw("Dealer",self._dealer,True)
        self._draw("Dealer",self._dealer,False)
        #self._print_total("Dealer",self._player)

    def next_player_draw(self):
        return self._next_draw("Player",self._player,True,True)

    def next_dealer_draw(self):
        is_safe = True
        if self._dealer.get_total_value() < 17:
            is_safe = self._next_draw("Dealer", self._dealer, True, True)
        return is_safe and self._dealer.get_total_value() < 17

    def result(self):
        def judge(total,border=21):
            return total > border

        dealer_total = self._dealer.get_total_value()
        player_total = self._player.get_total_value()
        flag = None
        if judge(dealer_total) and judge(player_total):
            print("The total of your dealer and your total are burst.")
            print("Dealer:{0} = Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card("Dealer")
            print("")
            self._player.print_hold_card("Player")
            print("")
            print("This game is a draw. ( ˘ω˘ )")
        elif judge(dealer_total):
            print("Dealer having a total over 21.")
            print("")
            self._dealer.print_hold_card("Dealer")
            print("")
            self._player.print_hold_card("Player")
            print("")
            print("You win. ٩( 'ω' )و")
            flag = True
        elif judge(dealer_total,player_total):
            print("The total value of the dealer is greater than your total.")
            print("Dealer:{0} > Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card("Dealer")
            print("")
            self._player.print_hold_card("Player")
            print("")
            print("You lose. (T^T)")
        elif judge(player_total):
            print("Your having a total over 21.")
            print("")
            self._dealer.print_hold_card("Dealer")
            print("")
            self._player.print_hold_card("Player")
            print("")
            print("You lose. (T^T)")
        elif judge(player_total,dealer_total):
            print("Your total is greater than the total value of the dealer.")
            print("Dealer:{0} < Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card("Dealer")
            print("")
            self._player.print_hold_card("Player")
            print("")
            print("You win. ٩( 'ω' )و")
            flag = True
        else:
            print("The total of your dealer and your total are the same.")
            print("Dealer:{0} = Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card("Dealer")
            print("")
            self._player.print_hold_card("Player")
            print("")
            print("This game is a draw. ( ˘ω˘ )")
        return flag

#カードを引くか否か
def is_continue():
    while True:
        flag = input ("continue? [Yes/No]\n>>>")
        #大文字を小文字に変換して比較
        if flag.lower() in ["y", "yes"]:
            return True
        if flag.lower() in ["n", "no"]:
            return False
        if flag.lower() in ["q", "quit"]:
            sys.exit()
        print("Invalid value. Please input yes or no.")

#ゲームの流れの定義
def run_game():
    game = BlackJackGame()
    print(" <<Let's play >>")
    print("<< First >>")
    game.first_player_draw()
    game.first_dealer_draw()
    print("")
    while True:
        if not is_continue():
            print("")
            break
        if not game.next_player_draw():
            break
    while game.next_dealer_draw():
        pass
    print("")
    return game.result()

#続けてゲームを行うか否かを定義
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
#本体
def blackJack():
    game_count = 0
    win_count = 0
    while True:
        game_count += 1
        if run_game():
            win_count += 1
        if not more_game():
            win_rate = (win_count / game_count) * 100
            print("Your winning rate is " + '{:.2f}'.format(win_rate) + '%')
            print("See you again.")
            break

if __name__ == '__main__':
    blackJack()