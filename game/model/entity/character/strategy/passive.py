from game import Position
from game.controller.command import Command, MoveCommand, IdleCommand
from game.model.entity.character.character import Character
from .strategy import Strategy


class PassiveStrategy(Strategy):
    def on_new_turn(self, character: Character) -> Command:
        return IdleCommand()
