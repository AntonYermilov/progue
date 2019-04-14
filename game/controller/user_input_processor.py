from enum import Enum

from game.controller.status_manager import StatusManager
from game.controller.command import Command
from game.controller.idle_command import IdleCommand
from game.controller.move_command import MoveCommand, MoveDirection
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
    User input processing: creating corresponding commands.
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

        if user_input == UserInput.UP:
            return self.process_up_()
        if user_input == UserInput.DOWN:
            return self.process_down_()
        if user_input == UserInput.LEFT:
            return self.process_left_()
        if user_input == UserInput.RIGHT:
            return self.process_right_()

    def process_up_(self) -> Command:
        if self.state == PlayerState.MOVING:
            return MoveCommand(self.status_manager, self.model, self.model.get_hero(), MoveDirection.MOVE_UP)

        return IdleCommand(status_manager=self.status_manager)

    def process_down_(self) -> Command:
        if self.state == PlayerState.MOVING:
            return MoveCommand(self.status_manager, self.model, self.model.get_hero(), MoveDirection.MOVE_DOWN)

        return IdleCommand(status_manager=self.status_manager)

    def process_left_(self) -> Command:
        if self.state == PlayerState.MOVING:
            return MoveCommand(self.status_manager, self.model, self.model.get_hero(), MoveDirection.MOVE_LEFT)

        return IdleCommand(status_manager=self.status_manager)

    def process_right_(self) -> Command:
        if self.state == PlayerState.MOVING:
            return MoveCommand(self.status_manager, self.model, self.model.get_hero(), MoveDirection.MOVE_RIGHT)

        return IdleCommand(status_manager=self.status_manager)
