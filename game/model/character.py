from abc import ABC
from dataclasses import dataclass
from typing import List

from game.elements import Artifact
from game.model.entity import Entity
from game.model.position import Position


@dataclass
class Character(Entity, ABC):
    """
    Base character class.
    """

    max_health: int
    health: int
    gold: int
    experience: int
    items: List[Artifact]
    items_limit: int

    def __init__(self, position: Position, max_health=5, items_limit=10):
        super().__init__(position)
        self.max_health = max_health
        self.health = max_health
        self.gold = 0
        self.experience = 0
        self.items = []

    def move(self, new_position: Position):
        """
        Moves character to given position on the map.
        :param new_position: Position
            New position of the character
        """
        self.position = new_position
