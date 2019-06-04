from enum import Enum
from bearlibterminal import terminal


class UserCommand(Enum):
    UP = terminal.TK_UP
    DOWN = terminal.TK_DOWN
    LEFT = terminal.TK_LEFT
    RIGHT = terminal.TK_RIGHT
    INVENTORY = terminal.TK_I
    DROP = terminal.TK_D
    USE = terminal.TK_U
    QUIT = terminal.TK_Q
    MENU = terminal.TK_M
    UNKNOWN = None
