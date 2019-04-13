from abc import ABC

from game.model.entity import Entity


class Character(Entity, ABC):
    """
    Base character class.
    """

    def __init__(self, position):
        super().__init__(position)
        self.max_health = 5
        self.health = 5
        self.gold = 0
        self.experience = 0
        self.items = []
        self.items_limit = 10

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
        super().__init__(position)
        self.max_health = 7
        self.health = 7


class Mob(Character):
    """
    Mob, the enemy to the player.
    """
    def __init__(self, position):
        super().__init__(position)
        self.items_limit = 3
