from game import Position
from game.controller.command import Command


class MoveCommand(Command):
    """
    Move command.

    Moves character to given direction.
    """

    def __init__(self, character, position: Position):
        self.character = character
        self.target_position = position

    def execute(self):
        self.character.move(self.target_position)
