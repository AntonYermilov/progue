from dataclasses import dataclass
from typing import List

from game.client.model.inventory import Inventory
from game.model.entity.character import Hero, Mob
from game.model.entity.item.item import Item
from game.model.map import Labyrinth


@dataclass
class State:
    my_turn: bool
    hero: Hero
    mobs: List[Mob]
    items: List[Item]
    inventory: Inventory
    labyrinth: Labyrinth = None
