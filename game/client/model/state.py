from dataclasses import dataclass
from typing import List

from game.client.model.inventory import Inventory
from game.model.entity.character import Hero, Mob
from game.model.entity.item.item import Item
from game.model.map import Labyrinth


"""
This class is a simple wrapping over data, received from the server.
It contains the description of the game model in a simple way and is later interpreted by the model class.
"""
@dataclass
class State:
    my_turn: bool
    hero: Hero
    mobs: List[Mob]
    items: List[Item]
    inventory: Inventory
    labyrinth: Labyrinth = None
