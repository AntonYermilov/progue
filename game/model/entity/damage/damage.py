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
    confuse_turns: int = 0
