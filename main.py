# the entrance of the game

from source import constants, tools, buttons
from source.states import main_menu, load_screen, level, choose_map, settings
import time


def main():
    # use  dictionary to control which window state to prescent in the screen

    state_dict = {

        'main_menu': main_menu.MainMenu(),
        'choose_map': choose_map.ChoseMap(),
        'load_screen': load_screen.LoadScreen(),
        'level': level.Level(),
        'settings': settings.Settings(),
        'game_over': load_screen.GameOver(),
    }
    game = tools.Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()
