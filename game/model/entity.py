from abc import ABC
from game.model.position import Position


class Entity(ABC):
    """
    Entity base class.
    """

    def __init__(self, position: Position, symbol: str = '.'):
        """
        Initialises entity with given position in the world.

        :param position: Position
            Position of the entity
        :param symbol: str
            Symbol that identifies entity
        """
        self.position = position
        self.symbol = symbol
