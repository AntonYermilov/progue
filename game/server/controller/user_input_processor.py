from enum import Enum

from game.server.controller.command import IdleCommand
from game.server.controller.command import MoveCommand

from game import Position
from game.server.controller.command import Command, AttackCommand
from game.server.controller.command import DropItemCommand
from game.server.controller.command import PickCommand
from game.server.controller.command import ToggleInventoryCommand
from game.server.controller.command import UseItemCommand
from game.server.controller import StatusManager
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
    PICK_ITEM = 5
    DROP_ITEM = 6
    USE_ITEM = 7
    TOGGLE_INVENTORY = 8


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

        if self.model.current_item and \
                (user_input == UserInput.UP
                 or user_input == UserInput.DOWN
                 or user_input == UserInput.LEFT
                 or user_input == UserInput.RIGHT):
            return self.process_inventory_shift_(user_input)
        if user_input == UserInput.UP \
                or user_input == UserInput.DOWN \
                or user_input == UserInput.LEFT \
                or user_input == UserInput.RIGHT:
            return self.process_move_(user_input)
        if self.model.current_item and user_input == UserInput.DROP_ITEM:
            return DropItemCommand(self.model)
        if self.model.current_item and user_input == UserInput.USE_ITEM:
            return UseItemCommand(self.model)
        if user_input == UserInput.TOGGLE_INVENTORY:
            return ToggleInventoryCommand(self.model)

        return IdleCommand()

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
        artifact = self.get_artifact_in_position_(new_position)
        if target:
            return AttackCommand(attacker=hero, target=target, model=self.model)
        elif artifact:
            return PickCommand(picker=hero, target=artifact, model=self.model, new_position=new_position)
        else:
            if self.is_correct_move_(new_position):
                return MoveCommand(self.model.get_hero(), new_position)

        return IdleCommand()

    def get_mob_in_position_(self, position: Position):
        for mob in self.model.mobs:
            if mob.position == position:
                return mob

        return None

    def get_artifact_in_position_(self, position: Position):
        for artifact in self.model.items:
            if artifact.position == position:
                return artifact

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

    def process_inventory_shift_(self, user_input):
        hero = self.model.hero
        current_item = self.model.current_item
        if user_input == UserInput.UP:
            self.model.current_item = hero.get_prev_item_if_any(current_item)
        if user_input == UserInput.DOWN:
            self.model.current_item = hero.get_next_item_if_any(current_item)

        return IdleCommand()
