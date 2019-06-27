from abc import ABC, abstractmethod

from .damage import Damage


class Damageable(ABC):
    """
    Interface for anything that can be damaged.
    """

    @abstractmethod
    def accept_damage(self, damage: Damage):
        """
        Deal damage to this Damageable.
        :param damage: damage
        """
        pass

    @abstractmethod
    def is_destroyed(self) -> bool:
        pass

    @abstractmethod
    def on_destroy(self, model):
        pass
