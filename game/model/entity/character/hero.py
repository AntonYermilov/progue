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

@dataclass
class LevelUpStats:
    health_inc_value: int
    strength_inc_value: int
    experience_inc_ratio: float

class Hero(Character, InventoryKeeper):
    """
    Hero is the character controlled by the player.
    """

    def __init__(self, name: str, id: str, position: Position, description: Dict):
        stats = HeroStats(level=1,
                          max_health=description['initial_stats']['max_health'],
                          health=description['initial_stats']['health'],
                          attack_damage=description['initial_stats']['max_strength'],
                          max_experience=description['initial_stats']['max_experience'],
                          experience=description['initial_stats']['experience'],
                          confuse_ratio=description['initial_stats']['confuse_ratio'],
                          confuse_turns=description['initial_stats']['confuse_turns'],
                          reward=description['reward'])
        Character.__init__(self, position=position, stats=stats)
        InventoryKeeper.__init__(self, limit=description['initial_stats']['inventory_size'])
        self.level_up_stats = LevelUpStats(health_inc_value=description['on_new_level']['max_health_increase_value'],
                                           strength_inc_value=description['on_new_level']['max_strength_increase_value'],
                                           experience_inc_ratio=description['on_new_level']['max_experience_increase_ratio'])
        self.name = name
        self.id = id

    def deal_damage(self, target: Damageable) -> Damage:
        confuse_turns = 0
        confuse = np.random.choice([True, False], p=[self.stats.confuse_ratio, 1 - self.stats.confuse_ratio])
        if confuse:
            confuse_turns = self.stats.confuse_turns
        return Damage(damage_type=DamageType.PHYSICAL,
                      damage_amount=self.stats.attack_damage,
                      confuse_turns=confuse_turns)

    def accept_damage(self, damage: Damage):
        self.update_health(-damage.damage_amount)

    def use_item(self, item: Item):
        item.apply(self)
        self.inventory.remove(item)

    def on_destroy(self, model):
        model.players.pop(self.id)

    def remove_item(self, item: Item):
        self.inventory.remove(item)

    def is_alive(self) -> bool:
        return self.stats.health > 0

    def update_health(self, health):
        self.stats.health += health
        if self.stats.health > self.stats.max_health:
            self.stats.health = self.stats.max_health
        if self.stats.health < 0:
            self.stats.health = 0

    def update_experience(self, experience):
        self.stats.experience += experience
        if self.stats.experience > self.stats.max_experience:
            self.stats.level += 1
            self.stats.experience -= self.stats.max_experience
            self.stats.health += self.level_up_stats.health_inc_value
            self.stats.max_health += self.level_up_stats.health_inc_value
            self.stats.attack_damage += self.level_up_stats.strength_inc_value
            self.stats.max_experience = int(self.stats.max_experience * self.level_up_stats.experience_inc_ratio)
        if self.stats.experience < 0:
            self.stats.experience = 0
