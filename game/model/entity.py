from abc import ABC


class Entity(ABC):
    """
    Entity base class.
    """

    def __init__(self, position):
        """
        Initialises entity with given position in the world.

        :param position:
            Position of the entity
        """
        self.position = position
        self.symbol = '.'
