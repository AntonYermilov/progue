from game.controller import UserInput

import curses

KEY_BINDINGS = {
    curses.KEY_UP: UserInput.UP,
    curses.KEY_DOWN: UserInput.DOWN,
    curses.KEY_RIGHT: UserInput.RIGHT,
    curses.KEY_LEFT: UserInput.LEFT,
    ord('i'): UserInput.TOGGLE_INVENTORY,
    ord('u'): UserInput.USE_ITEM,
    ord('d'): UserInput.DROP_ITEM,
    ord('p'): UserInput.PICK_ITEM,
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