import random
from abc import ABC, abstractmethod

from game.model.character import Character
from game.model.entity import Entity


class Artifact(Entity, ABC):
    @abstractmethod
    def apply(self, character: Character):
        pass


class Gold(Artifact):
    def __init__(self, position):
        super().__init__(position)
        self.amount = random.randint(1, 10)

    def apply(self, character):
        character.gold += self.amount


class HealingPotion(Artifact):
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.health = character.max_health


class AmnesiaPotion(Artifact):
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.experience = max(0, character.experience - 10)


class KnowledgeScroll(Artifact):
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.experience += 10


class CursedScroll(Artifact):
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.health -= 4
