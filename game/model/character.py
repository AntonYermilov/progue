from abc import ABC
from typing import List, Tuple

from game.elements import Artifact
from game.model.entity import Entity
from dataclasses import dataclass


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

    def __init__(self, position: Tuple[int, int], max_health=5, items_limit=10):
        super().__init__(position)
        self.max_health = max_health
        self.health = max_health
        self.gold = 0
        self.experience = 0
        self.items = []

    def move(self, x, y):
        """
        Moves character to given position on the map.
        :param x:
            X coordinate
        :param y:
            Y coordinate
        """
        self.position = (y, x)


class Hero(Character):
    """
    Hero is the character controlled by the player.
    """

    def __init__(self, position):
        super().__init__(position, max_health=7)


class Mob(Character):
    """
    Mob, the enemy to the player.
    """

    def __init__(self, position):
        super().__init__(position, items_limit=3)
