from game import Position
from game.model.entity.character.character import Character
from .strategy import Strategy


class PassiveStrategy(Strategy):
    def make_move(self, character: Character) -> Position:
        return character.position