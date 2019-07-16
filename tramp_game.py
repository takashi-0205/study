#-*- coding:utf-8 -*-
import sys
import random
import time
from itertools import count
from master_deck import Dealer
from player_rule import Player

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
06/05 プレイヤー1のみ操作するように変更
06/05 hコマンドで自分の手札を確認できるように変更
06/06 プレイヤークラスを外部に切り出し
06/06 全自動と手動の選択を行えるように改修
07/16 ローカルに複数回コミットした際の挙動検証
"""

class BubbGame:

    def play(self, player_num,which_game,mode):
        self.players = [Player(f"Player#{i+1}",i) for i in range(player_num)]
        self.ranking = []

        print("###### Preparation ######")
        Dealer().deal(self.players,which_game)
        #コメントアウトを外すと全プレイヤーの手札公開
        #self._show_hands()
        self._drop_pairs()
        #self._show_hands()

        print("###### Game Start ######")
        self._show_heavenly_winner()
        turn = count(1)
        while len(self.players) > 1:
            print(f"===== Turn {next(turn)} ======")
            print(f"Playing {len(self.players)} players")
            self._turn(mode)
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

    def _turn(self,mode):
        for player, next_player in self._pair_players():
            print(player.name + " chooses the card to draw from " + next_player.name)
            pulled_card, dropped_cards = player.bubb_play(next_player,mode)
            #誰から何のカードを引いたか表示されるためコメントアウト
            #print(f"{player.name} pulled {pulled_card} from {next_player.name}")
            if next_player.win():
                print(f"{next_player.name} 引かれて上がり！")
                if next_player.id == 1:
                    time.sleep(2)
                self.players.remove(next_player)
                self.ranking.append(next_player)
            if dropped_cards:
                print(f"{player.name} dropped {dropped_cards}")
            if player.win():
                print(f"{player.name} 引いて上がり！")
                if player.id == 1:
                    time.sleep(2)
                self.players.remove(player)
                self.ranking.append(player)

    def _show_ranking(self):
        print("------ Ranking ------")
        for player in self.ranking + self.players:
            print(player.name)
            

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
12. ダブルダウンなし、スピリットなし、サレンダーなし。その他特殊そうなルールなし

開発ログ
05/17 オリジナル
05/17 終了コマンドを入力しない限りブラックジャックをプレイできるように
05/20 勝率の表示
06/03 カードクラスを外部に切り出し
06/06 プレイヤークラスを外部に切り出し
"""


#ブラックジャックのプレイヤーの動作と勝敗について定義
class BlackJackGame:
    def __init__(self):
        self._pcards = Dealer()
        self._player = Player("Player",None)
        self._dealer = Player("Dealer",None)
    #ゲームの流れの定義
    def play(self):
        print(" <<Let's play >>")
        print("<< First >>")
        self.first_player_draw()
        self.first_dealer_draw()
        print("")
        while True:
            if not self.is_continue():
                print("")
                break
            if not self.next_player_draw():
                break
        while self.next_dealer_draw():
            pass
        print("")
        return self.result()

    def _draw(self,name,pobj, is_print):
        card = self._pcards.draw()
        pobj.hold(card)
        if is_print:
            print('[{0}]=>[{1}]'.format(name,card.label))
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
            self._dealer.print_hold_card()
            print("")
            self._player.print_hold_card()
            print("")
            print("This game is a draw. ( ˘ω˘ )")
        elif judge(dealer_total):
            print("Dealer having a total over 21.")
            print("")
            self._dealer.print_hold_card()
            print("")
            self._player.print_hold_card()
            print("")
            print("You win. ٩( 'ω' )و")
            flag = True
        elif judge(dealer_total,player_total):
            print("The total value of the dealer is greater than your total.")
            print("Dealer:{0} > Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card()
            print("")
            self._player.print_hold_card()
            print("")
            print("You lose. (T^T)")
        elif judge(player_total):
            print("Your having a total over 21.")
            print("")
            self._dealer.print_hold_card()
            print("")
            self._player.print_hold_card()
            print("")
            print("You lose. (T^T)")
        elif judge(player_total,dealer_total):
            print("Your total is greater than the total value of the dealer.")
            print("Dealer:{0} < Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card()
            print("")
            self._player.print_hold_card()
            print("")
            print("You win. ٩( 'ω' )و")
            flag = True
        else:
            print("The total of your dealer and your total are the same.")
            print("Dealer:{0} = Your:{1}".format(dealer_total, player_total))
            print("")
            self._dealer.print_hold_card()
            print("")
            self._player.print_hold_card()
            print("")
            print("This game is a draw. ( ˘ω˘ )")
        return flag
    
    #カードを引くか否か
    def is_continue(self):
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

"""
開発する神経衰弱のルール
1. 初期カードは52枚
2. 揃ったペアをドロップする
3. 揃わなかったカードは末尾に再配置
4. ペアを揃えたプレイヤーは連続してターンを行える

開発ログ
06/05 作成開始
06/05 全自動神経衰弱の完成
06/06 人数指定を行えるように変更
06/06 プレイヤー1の時のみ選択できるように変更
06/06 全自動と手動の選択を行えるように改修
06/12 ターン制限の追加
06/12 ターン制限の有無を選択できるように改修
06/12 ターン制限数の設定を出来るように改修
"""

class NervousGame:
    def play(self,player_num,mode,limit_flg,limit_turn):
        self.players = [Player(f"Player#{i+1}",i) for i in range(player_num)]
        self.deck = Dealer()
        self.count = 1
        self.mode = mode
        self.limit_flg = limit_flg
        self.limit_turn = int(limit_turn)
        
        random.shuffle(self.deck.cards)
        
        print("###### Game Start ######")
        while len(self.deck.cards) > 1:
            for player in self.players:
                if self.deck.cards == []:
                    continue
                while self.turn(player):
                    if self.count > self.limit_turn and self.limit_flg == True:
                        break 
            if self.count > self.limit_turn and self.limit_flg == True:
                print(f"######{self.count -1} turns have passed.######\nThe remaining number of decks is " + str(len(self.deck.cards)))
                break
        print("###### Game End ######")
        self.result()

    def turn(self,player):
        if self.deck.cards == [] or (self.count > self.limit_turn and self.limit_flg == True):
            return False
        print(f"###### Turn {self.count} ######")
        print(f"{player.name} chooses the card.")
        player.nerv_play(self.deck,self.mode)
        player.nerv_play(self.deck,self.mode)
        flg = self.judge_pairs(player)
        return flg
    
    def judge_pairs(self,player):
        self.count += 1
        card1 = player.cards[-1]
        card2 = player.cards[-2]
        print(f"{card1}:{card2}")
        if card1.number == card2.number:
            print("I throw it out because it is a pair.")
            return True
        else:
            self.deck.release(card1)
            self.deck.release(card2)
            player.release(card1)
            player.release(card2)
            print("The card was not aligned.")
            return False
        
    def result(self):
        print("###### Game Result ######")
        for player in self.players:
            print(f"{player.name}'s result:{len(player.cards)}")

"""
ゲーム本編には関係のないメソッド
主に手動、自動の選択や連続してゲームを行うかの入力を行わせる
"""
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
    auto_mode = True
    while True:
        mode = input("Auto?Manual?[Auto/Manual]\n>>>")
        if mode.lower() in ["m","manual"]:
            auto_mode = False
            break
        elif mode.lower() in ["a","auto"]:
            pass
            break
        else:
            print("Please enter a mode.")
    while True:
        player_num = input("How many Players?\n>>>")
        if player_num.isdecimal():
            if int(player_num) in list(range(2,11)):
                return auto_mode, player_num
            print('Please select in the range of 2 to 10.')
        elif player_num.lower() in ["q", "quit"]:
            print("Good Bye")
            sys.exit()
        else:
            print('Please enter a number.')

def input_mode():
    while True:
        which_game = input("Which game do you play?[jiji/bubb]\n>>>")
        if which_game.lower() in ["j", "jiji", "b", "bubb"]:
            return which_game
        elif which_game.lower() in ["q", "quit"]:
            print("Good Bye.")
            sys.exit()
        else:
            print('Please enter a str.')

def input_limit_flg():
    while True:
        want_limit = input("Do you have a turn limit?[Yes/No]\n>>>")
        if want_limit.lower() in ["y", "yes"]:
            return True
        if want_limit.lower() in ["n", "no"]:
            return False
        print("Invalid value. Please input yes or no.")

def input_limit_turn(flg):
    while flg:
        turn = input("What turn do you play?\n>>>")
        if turn.isdecimal():
            if int(turn) > 1:
                return turn
            print('Please select 1 or more.')
        print('Please enter a number.')
    return 0
