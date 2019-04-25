from .strategy import Strategy
from game.model.character import Character
from game.model.model import Model
from game.model.position import Position


class AggressiveStrategy(Strategy):
    def make_move(self, character: Character) -> Position:
        pass