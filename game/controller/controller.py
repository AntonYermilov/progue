from enum import Enum

from game.elements import MapBlock
from game.model import Model
from game.model.position import Position
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


Direction = Position


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
            self.move(self.model.get_hero(), Direction.as_point(x=-1, y=0))
        if action == Action.MOVE_RIGHT:
            self.move(self.model.get_hero(), Direction.as_point(x=1, y=0))
        if action == Action.MOVE_UP:
            self.move(self.model.get_hero(), Direction.as_point(x=0, y=-1))
        if action == Action.MOVE_DOWN:
            self.move(self.model.get_hero(), Direction.as_point(x=0, y=1))

    # TODO Refactor to Command pattern
    def move(self, character: Character, direction: Direction):
        """
        Moves character according to given direction if it's possible.
        """
        target_position = character.position + direction

        if target_position.get_x() < self.model.shape()[1] and target_position.get_y() < self.model.shape()[0]:
            if self.model.labyrinth[target_position.get_row()][target_position.get_col()] == MapBlock.FLOOR:
                character.move(target_position)
            else:
                pass
