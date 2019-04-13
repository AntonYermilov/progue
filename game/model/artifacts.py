import random
from abc import ABC, abstractmethod

from game.model.character import Character
from game.model.entity import Entity


class Artifact(Entity, ABC):
    """
    Artifact base class.
    """
    @abstractmethod
    def apply(self, character: Character):
        """
        Use artifact on a target.
        :param character: target to apply artifact effect to.
        """
        pass


class Gold(Artifact):
    """
    Gold artifact.

    Increases amount of gold by amount.
    """
    def __init__(self, position):
        super().__init__(position)
        self.amount = random.randint(1, 10)

    def apply(self, character):
        character.gold += self.amount


class HealingPotion(Artifact):
    """
    Healing potion.

    Increases amount of health.
    """
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.health = character.max_health


class AmnesiaPotion(Artifact):
    """
    Amnesia potion.

    Decreases character's XP by N points.
    """
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.experience = max(0, character.experience - 10)


class KnowledgeScroll(Artifact):
    """
    Knowledge scroll.

    Increases character's XP by N points.
    """
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.experience += 10


class CursedScroll(Artifact):
    """
    Cursed scroll.

    Decreases character's health.
    """
    def __init__(self, position):
        super().__init__(position)

    def apply(self, character):
        character.health -= 4
