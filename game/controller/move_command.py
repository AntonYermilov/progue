from dataclasses import dataclass
from enum import Enum

from game import Position
from game.controller.status_manager import StatusManager
from game.controller.command import Command
from game.model import Model
from game.model.entity.character import Character


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

        new_position = Position.as_point(y=y, x=x)
        if self.is_correct_move_(new_position):
            cell_is_free = True
            for mob in self.model.mobs:
                cell_is_free &= mob.position != new_position
            if cell_is_free:
                self.character.move(new_position)

            for mob in self.model.mobs:
                new_mob_position = mob.get_move()
                if new_mob_position == self.character.position:
                    continue
                mob.move(new_mob_position)
        else:
            self.emit_message("Cannot move, obstacle ahead.")

    def is_correct_move_(self, position: Position):
        """
        Check if given move is correct in current world.
        :param position:
            New position of character
        :return:
            True if move is correct,
            False otherwise
        """
        return self.model.labyrinth.is_floor(position)
