from dataclasses import dataclass
from typing import Dict

import numpy as np

from game import Position
from game.model.entity.damage import Damageable, Damage, DamageType
from game.model.entity.inventory.inventory_keeper import InventoryKeeper
from game.model.entity.item.item import Item
from .character import Character, CharacterStats


@dataclass
class HeroStats(CharacterStats):
    max_experience: int
    experience: int
    confuse_ratio: float

    def __init__(self, max_experience: int, experience: int, confuse_ratio: float, confuse_turns: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_experience = max_experience
        self.experience = experience
        self.confuse_ratio = confuse_ratio
        self.confuse_turns = confuse_turns


class Hero(Character, InventoryKeeper):
    """
    Hero is the character controlled by the player.
    """

    def __init__(self, position: Position, description: Dict):
        stats = HeroStats(level=1,
                          max_health=description['initial_stats']['max_health'],
                          health=description['initial_stats']['health'],
                          attack_damage=description['initial_stats']['max_strength'],
                          max_experience=description['initial_stats']['max_experience'],
                          experience=description['initial_stats']['experience'],
                          confuse_ratio=description['initial_stats']['confuse_ratio'],
                          confuse_turns=description['initial_stats']['confuse_turns'])
        Character.__init__(self, position=position, stats=stats)
        InventoryKeeper.__init__(self, limit=description['initial_stats']['inventory_size'])

    def deal_damage(self, target: Damageable) -> Damage:
        confuse_turns = 0
        confuse = np.random.choice([True, False], p=[self.stats.confuse_ratio, 1 - self.stats.confuse_ratio])
        if confuse:
            confuse_turns = self.stats.confuse_turns
        return Damage(damage_type=DamageType.PHYSICAL,
                      damage_amount=self.stats.attack_damage,
                      confuse_turns=confuse_turns)

    def accept_damage(self, damage: Damage):
        self.stats.health -= damage.damage_amount

    def use_item(self, item: Item):
        item.apply(self)
        self.inventory.remove(item)

    def on_destroy(self, model):
        # print('Hero destroyed')
        pass

    def remove_item(self, item: Item):
        self.inventory.remove(item)

    def get_item_if_any(self):
        return self.inventory[0] if len(self.inventory) else None

    def get_prev_item_if_any(self, item: Item):
        idx = self.inventory.index(item)
        return self.inventory[idx - 1] if idx - 1 >= 0 else item

    def get_next_item_if_any(self, item: Item):
        idx = self.inventory.index(item)
        return self.inventory[idx + 1] if idx + 1 < len(self.inventory) else item

    def is_alive(self) -> bool:
        return self.stats.health > 0
