from dataclasses import dataclass
from typing import List

from game.client.model.inventory.inventory import Inventory
from game.client.model.state import State
from game.model.entity.character import Hero, Mob
from game.model.entity.item.item import Item
from game.model.map import Labyrinth


@dataclass
class Model:
    my_turn: bool = False
    hero: Hero = None
    mobs: List[Mob] = None
    items: List[Item] = None
    inventory: Inventory = None
    labyrinth: Labyrinth = None

    # TODO Dummy update method, need to change
    def update(self, state: State):
        self.my_turn = state.my_turn
        self.hero = state.hero
        self.mobs = state.mobs
        self.items = state.items
        self.inventory = state.inventory
        if state.labyrinth is not None:
            self.labyrinth = state.labyrinth
