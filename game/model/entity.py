from abc import ABC
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Entity(ABC):
    """
    Entity base class.
    """

    position: Tuple[int, int]
    symbol: str

    def __init__(self, position: Tuple[int, int], symbol='.'):
        """
        Initialises entity with given position in the world.

        :param position:
            Position of the entity
        """
        self.position = position
        self.symbol = symbol

    def set_position(self, y, x):
        self.position = (y, x)
