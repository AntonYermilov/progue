import numpy as np
from typing import Dict, Union

from game import Position
from game.model.entity.character import Hero, MobFactory
from game.model.entity.item.item import ItemFactory, Item
from game.model.map import MapLoader, MapGenerator, Labyrinth


class Model:
    """
    Model of MVC architecture.
    """

    def __init__(self):
        self.labyrinth = None
        self.hero = None
        self.mobs = []
        self.items = []
        self.current_item = None
        self.players = dict()

        self.mob_factory = MobFactory(self)
        self.item_factory = ItemFactory(self)

    def get_hero(self, player_id):
        if player_id in self.players:
            return self.players[player_id]
        else:
            return None

    def get_labyrinth(self) -> Labyrinth:
        return self.labyrinth

    def generate_labyrinth(self, rows: int, columns: int, free_cells_ratio: float = 0.5, prob: float = 0.25,
                           scale_rows: float = 1.0, scale_columns: float = 2.0):
        """
        Generates labyrinth based on params.
        """
        self.labyrinth = MapGenerator().generate(rows, columns, free_cells_ratio, prob, scale_rows, scale_columns)

    def upload_labyrinth(self, layout: np.ndarray):
        """
        Uploads labyrinth from a text representation.

        :param layout:
            Text representation of the labyrinth
        """
        self.labyrinth = MapLoader.load_map(layout)

    def _get_free_cell(self) -> Union[Position, None]:
        cells = np.array([Position.as_position(row, column) for row, column in self.labyrinth.get_floor_cells()])
        np.random.shuffle(cells)

        for cell in cells:
            is_free = True
            for hero in self.players.values():
                if hero.position == cell:
                    is_free = False
                    break

            for mob in self.mobs:
                if mob.position == cell:
                    is_free = False
                    break
            if is_free:
                return cell

        return None

    def place_hero(self, player_id, hero_desc: Dict):
        cell = self._get_free_cell()
        self.players[player_id] = Hero(cell, hero_desc)
        self.players[player_id].set_name(player_id)

    def place_new_mob(self, mob_name: str, mob_desc: Dict):
        cell = self._get_free_cell()
        self.mobs.append(self.mob_factory.generate_mob(cell, mob_name, mob_desc))

    def place_new_item(self, item_name: str, item_desc: Dict):
        cell = self._get_free_cell()
        self.items.append(self.item_factory.generate_item(cell, item_name, item_desc))

    def place_item(self, item: Item, position: Position):
        item.position = position
        self.items.append(item)

    def remove_item(self, item: Item):
        self.items.remove(item)
