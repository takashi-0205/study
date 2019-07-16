import tramp_game
#本体
def blackJack():
    game_count = 0
    win_count = 0
    while True:
        game = tramp_game.BlackJackGame()
        game_count += 1
        if game.play():
            win_count += 1
        if not tramp_game.more_game():
            win_rate = (win_count / game_count) * 100
            print("Your winning rate is " + '{:.2f}'.format(win_rate) + '%')
            print("See you again.")
            break
        del game

if __name__ == '__main__':
    blackJack()