import numpy as np

from .character import Character
from .position import Position
from .strategy.strategy import Strategy



class Mob(Character):
    """
    Mob, the enemy to the player.
    """

    def __init__(self, position: Position, strategy: Strategy):
        super().__init__(position, items_limit=3)
        self.strategy = strategy

    def get_move(self) -> Position:
        return self.strategy.make_move(self)
