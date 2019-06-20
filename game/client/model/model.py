from dataclasses import dataclass
from typing import List

from game.client.model.inventory.inventory import Inventory
from game.client.model.state import State
from game.model.entity.character import Hero, Mob
from game.model.entity.item.item import Item
from game.model.map import Labyrinth


"""
This class describes game model. It contains relevant description of the environment,
description of all existing entities, and is used to render them in view module
"""
@dataclass
class Model:
    my_turn: bool = False
    hero: Hero = None
    mobs: List[Mob] = None
    items: List[Item] = None
    inventory: Inventory = None
    labyrinth: Labyrinth = None

    """
    Updates model with the state, received from the server
    """
    def update(self, state: State):
        self.my_turn = state.my_turn
        if state.hero is not None:
            self.hero = state.hero
        else:
            self.hero.stats.health = 0
        self.mobs = state.mobs
        self.items = state.items
        if state.inventory is not None:
            self.inventory = state.inventory
        if state.labyrinth is not None:
            self.labyrinth = state.labyrinth
