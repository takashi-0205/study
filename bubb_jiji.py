import tramp_game
def main():
    while True:
        game = tramp_game.BubbGame()
        which_game = tramp_game.input_mode()
        mode, player_num = tramp_game.input_data()
        game.play(int(player_num),which_game,mode)
        if not tramp_game.more_game():
            print("See you again.")
            break
        del game

if __name__ == "__main__":
    main()