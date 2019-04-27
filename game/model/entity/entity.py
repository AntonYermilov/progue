from abc import ABC
from game import Position


class Entity(ABC):
    """
    Entity base class.
    """

    def __init__(self, position: Position):
        """
        Initialises entity with given position in the world.

        :param position: Position
            Position of the entity
        """
        self.position = position
