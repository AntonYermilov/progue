from abc import ABC
from typing import Dict

from game import Position
from game.model.entity import Entity
from game.model.entity.character import Character


class Item(Entity, ABC):

    def __init__(self, position: Position, name: str, description: Dict):
        super().__init__(position)
        self.name = name
        self.description = description

    def apply(self, target: Character):
        target.stats.experience += self.description.get('experience', 0)
        target.stats.health += self.description.get('health', 0)


class ItemFactory:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def generate_item(position: Position, name: str, description: Dict):
        return Item(position, name, description)
