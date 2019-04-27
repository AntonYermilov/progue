from dataclasses import dataclass
from enum import Enum


class DamageType(Enum):
    PHYSICAL = 0
    MAGIC = 1
    HEALING = 2


@dataclass
class Damage:
    """
    Damage class.
    """

    damage_type: DamageType
    damage_amount: int

    def get_damage_type(self) -> DamageType:
        """
        Type of damage.
        :return:
            damage type
        """
        return self.damage_type

    def get_damage_amount(self) -> int:
        """
        Amount of damage.
        :return:
            amount of damage
        """
        return self.damage_amount
