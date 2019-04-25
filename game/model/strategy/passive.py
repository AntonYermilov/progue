from .strategy import Strategy
from game.model.character import Character
from game.model.model import Model
from game.model.position import Position


class PassiveStrategy(Strategy):
    def make_move(self, character: Character) -> Position:
        return character.position