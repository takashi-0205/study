import tramp_game
def main():
    while True:
        game = tramp_game.NervousGame()
        auto_mode, player_num = tramp_game.input_data()
        flg = tramp_game.input_limit_flg()
        game.play(int(player_num),auto_mode,flg,input_limit_turn(flg))
        if not tramp_game.more_game():
            print("See you again.")
            break
        del game

if __name__ == "__main__":
    main()
