import logging
from collections import namedtuple
from enum import Enum

from game.elements import MapBlock
from game.model import Model
from game.model.character import Character


class Action(Enum):
    UNKNOWN = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4


Point = namedtuple("Point", ["x", "y"])


class Controller:

    def __init__(self, model: Model):
        self.model = model

    def start_game(self, view):
        view.start(controller=self)

    def process_input(self, action: Action):
        if action == Action.MOVE_LEFT:
            self.move(self.model.get_hero(), Point(x=-1, y=0))
        if action == Action.MOVE_RIGHT:
            self.move(self.model.get_hero(), Point(x=1, y=0))
        if action == Action.MOVE_UP:
            self.move(self.model.get_hero(), Point(x=0, y=-1))
        if action == Action.MOVE_DOWN:
            self.move(self.model.get_hero(), Point(x=0, y=1))

    def move(self, character: Character, direction: Point):
        y, x = character.position
        target_point = Point(x=direction.x + x, y=direction.y + y)

        print(self.model.shape())
        if target_point.x < self.model.shape()[1] and target_point.y < self.model.shape()[0]:
            if self.model.labyrinth[target_point.y][target_point.x] == MapBlock.FLOOR:
                character.move(x=target_point.x, y=target_point.y)
            else:
                pass
        else:
            pass
