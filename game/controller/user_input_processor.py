from enum import Enum

from game.controller.command import IdleCommand
from game.controller.command import MoveCommand

from game import Position
from game.controller.command import Command, AttackCommand
from game.controller.status_manager import StatusManager
from game.model import Model


class PlayerState(Enum):
    MOVING = 0
    FIGHTING = 1


class UserInput(Enum):
    """
    User action type
    """
    UNKNOWN = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class UserInputProcessor:
    """
    User input processing: creating corresponding command.
    """

    def __init__(self, model: Model, status_manager: StatusManager):
        self.state = PlayerState.MOVING
        self.model = model
        self.status_manager = status_manager

    def process_input(self, user_input: UserInput) -> Command:
        """
        Creates command corresponding to user input and current state.
        :param user_input:
            User input
        :return:
            Command by input
        """

        if user_input == UserInput.UP or user_input == UserInput.DOWN or user_input == UserInput.LEFT or user_input == UserInput.RIGHT:
            return self.process_move_(user_input)

    def process_move_(self, user_input: UserInput):
        hero = self.model.get_hero()
        y, x = hero.position

        if user_input == UserInput.LEFT:
            x -= 1
        if user_input == UserInput.RIGHT:
            x += 1
        if user_input == UserInput.UP:
            y -= 1
        if user_input == UserInput.DOWN:
            y += 1

        new_position = Position.as_point(y=y, x=x)

        target = self.get_mob_in_position_(new_position)
        if target is None:
            if self.is_correct_move_(new_position):
                return MoveCommand(self.model.get_hero(), new_position)
        else:
            return AttackCommand(attacker=hero, target=target, model=self.model)

        return IdleCommand()

    def get_mob_in_position_(self, position: Position):
        for mob in self.model.mobs:
            if mob.position == position:
                return mob

        return None

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
