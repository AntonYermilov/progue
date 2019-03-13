from abc import ABC

from game.model.entity import Entity


class Character(Entity, ABC):
    def __init__(self, position):
        super().__init__(position)
        self.max_health = 5
        self.health = 5
        self.gold = 0
        self.experience = 0
        self.items = []
        self.items_limit = 10

    def move(self, x, y):
        self.position = (y, x)


class Hero(Character):
    def __init__(self, position):
        super().__init__(position)
        self.max_health = 7
        self.health = 7


class Snake(Character):
    def __init__(self, position):
        super().__init__(position)
        self.items_limit = 3


class Ghost(Character):
    def __init__(self, position):
        super().__init__(position)
        self.items_limit = 3
