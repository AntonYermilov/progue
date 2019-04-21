import random

from game.elements import MapBlock, Character
from game.model.character import Hero
from game.model.elements import to_class
from .map import Labyrinth, MapLoader, MapGenerator
from .position import Position, Direction
import numpy as np



class Model:
    """
    Model of MVC architecture.
    """

    def __init__(self):
        self.labyrinth = None
        self.entities = []
        self.hero = None

    def shape(self):
        """
        Returns shape of the map (a pair).

        :return:
            shape of the map
        """
        return self.labyrinth.labyrinth.shape

    def get_hero(self) -> Hero:
        """
        Returns hero.
        :return:
            hero
        """
        return self.hero[1]

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

    def place_entities(self, entities: dict):
        """
        Places entities from given dict to the game map.
        :param entities:
            Dict entity_type -> count
        """
        cells = [Position.as_position(row, column) for row, column in self.labyrinth.get_floor_cells()]
        random.shuffle(cells)
        i = 0
        for entity, count in entities.items():
            for di in range(count):
                self.entities.append((entity, to_class[entity](cells[i + di])))
                if entity == Character.HERO:
                    self.hero = self.entities[-1]
            i += count
