from abc import ABC, abstractmethod
from dataclasses import dataclass

from game import Position
from game.model.entity import Entity
from game.model.entity.damage import Damageable, Damage, DamageType


@dataclass
class CharacterStats:
    level: int
    attack_damage: int
    max_health: int
    health: int


@dataclass
class Character(Entity, Damageable, ABC):
    """
    Base character class.
    """

    def __init__(self, position: Position, stats: CharacterStats):
        super().__init__(position)
        self.stats = stats

    def move(self, new_position: Position):
        """
        Moves character to given position on the map.
        :param new_position: new position of the character
        """
        self.position = new_position

    @abstractmethod
    def deal_damage(self, target: Damageable) -> Damage:
        """
        Get attack damage for given target.
        :param target: target
        :return: damage
        """
        pass

    @abstractmethod
    def accept_damage(self, damage: Damage):
        """
        Receive specified damage
        :param damage: incoming damage
        """
        pass

    def is_destroyed(self) -> bool:
        return self.stats.health <= 0
