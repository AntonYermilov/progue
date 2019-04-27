from abc import ABC
from dataclasses import dataclass

from game.model.entity import Entity
from game import Position


@dataclass
class Character(Entity, ABC):
    """
    Base character class.
    """

    def __init__(self, position: Position):
        super().__init__(position)

    def move(self, new_position: Position):
        """
        Moves character to given position on the map.
        :param new_position: new position of the character
        """
        self.position = new_position
