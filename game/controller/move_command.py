from dataclasses import dataclass
from enum import Enum

from game.controller.status_manager import StatusManager
from game.controller.command import Command
from game.elements import MapBlock
from game.model import Character, Model, Position


class MoveDirection(Enum):
    """
    User action type
    """
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3


@dataclass
class MoveCommand(Command):
    """
    Move command.

    Moves character to given direction.
    """

    character: Character
    direction: int
    model: Model

    def __init__(self, status_manager: StatusManager, model: Model, character: Character, direction: MoveDirection):
        super().__init__(status_manager)
        self.model = model
        self.character = character
        self.direction = direction

    def execute(self):
        y, x = self.character.position

        if self.direction == MoveDirection.MOVE_LEFT:
            x -= 1
        if self.direction == MoveDirection.MOVE_RIGHT:
            x += 1
        if self.direction == MoveDirection.MOVE_UP:
            y -= 1
        if self.direction == MoveDirection.MOVE_DOWN:
            y += 1

        if self.is_correct_move_(y=y, x=x):
            self.character.move(Position.as_point(y=y, x=x))
        else:
            self.emit_message("Cannot move, obstacle ahead.")

    def is_correct_move_(self, y, x):
        """
        Check if given move is correct in current world.
        :param y:
            Row index
        :param x:
            Column index
        :return:
            True if move is correct,
            False otherwise
        """

        if x < self.model.shape()[1] and y < self.model.shape()[0]:
            if self.model.labyrinth[y][x] == MapBlock.FLOOR:
                return True

        return False
