from collections import namedtuple
from enum import Enum

from game.elements import MapBlock
from game.model import Model
from game.model.character import Character


# TODO Refactor to Command pattern
class Action(Enum):
    """
    User action type
    """
    UNKNOWN = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4


Point = namedtuple("Point", ["x", "y"])


class Controller:
    """
    Controller of MVC architecture.
    """

    def __init__(self, model: Model):
        """
        Initialises controller with given model.

        :param model: Model
            A model to work with
        """
        self.model = model

    def start_game(self, view):
        """
        Starts the game loop.

        :param view: View
            View to work with
        """
        view.start(controller=self)

    # TODO Refactor to Command pattern
    def process_input(self, action: Action):
        """
        Processes user input.
        """
        if action == Action.MOVE_LEFT:
            self.move(self.model.get_hero(), Point(x=-1, y=0))
        if action == Action.MOVE_RIGHT:
            self.move(self.model.get_hero(), Point(x=1, y=0))
        if action == Action.MOVE_UP:
            self.move(self.model.get_hero(), Point(x=0, y=-1))
        if action == Action.MOVE_DOWN:
            self.move(self.model.get_hero(), Point(x=0, y=1))

    # TODO Refactor to Command pattern
    def move(self, character: Character, direction: Point):
        """
        Moves character according to given direction if it's possible.
        """
        y, x = character.position
        target_point = Point(x=direction.x + x, y=direction.y + y)

        if target_point.x < self.model.shape()[1] and target_point.y < self.model.shape()[0]:
            if self.model.labyrinth[target_point.y][target_point.x] == MapBlock.FLOOR:
                character.move(x=target_point.x, y=target_point.y)
            else:
                pass
