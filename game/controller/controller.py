from enum import Enum

from game.elements import Artifact, Character, Object
from game.model import Model


class InputType(Enum):
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4


class Controller:

    def __init__(self, model):
        self.model = model

    def start_game(self, view):
        view.start(controller=self)

    def process_input(self, key_pressed):
        pass
