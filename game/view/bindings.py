from game.controller import UserInput
from bearlibterminal import terminal

import curses

KEY_BINDINGS = {
    terminal.TK_UP: UserInput.UP,
    terminal.TK_DOWN: UserInput.DOWN,
    terminal.TK_RIGHT: UserInput.RIGHT,
    terminal.TK_LEFT: UserInput.LEFT,
    terminal.TK_I: UserInput.TOGGLE_INVENTORY,
    terminal.TK_U: UserInput.USE_ITEM,
    terminal.TK_D: UserInput.DROP_ITEM,
    terminal.TK_P: UserInput.PICK_ITEM,
}

LEGEND = 'q - exit\n' \
         'i - switch between inventory and map\n' \
         'u - use selected item from inventory\n' \
         'd - drop selected item from inventory\n'


GAME_OVER = ' GGG   AAA  M   M EEEEE    OOO  V   V EEEEE RRRR \n' \
            'G     A   A MM MM E       O   O V   V E     R   R\n' \
            'G  GG A   A M M M EEEEE   O   O V   V EEEEE RRRR \n' \
            'G   G AAAAA M   M E       O   O  V V  E     R  R \n' \
            ' GGG  A   A M   M EEEEE    OOO    V   EEEEE R   R\n' \
            '=================================================\n' \
            '              q - exit, r - restart              \n'