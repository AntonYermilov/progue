from game import Position
from game.controller.command import Command, MoveCommand
from game.model.entity.character.character import Character
from .strategy import Strategy


class PassiveStrategy(Strategy):
    def on_new_turn(self, character: Character) -> Command:
        return MoveCommand(character, self.make_move(character))

    def make_move(self, character: Character) -> Position:
        return character.position
