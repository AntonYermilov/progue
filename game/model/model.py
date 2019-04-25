import numpy as np

from game.model.elements import to_class
from .artifacts import Artifact
from .character import Mob, Hero
from .map import MapLoader, MapGenerator, Labyrinth
from .position import Position


class Model:
    """
    Model of MVC architecture.
    """

    def __init__(self):
        self.labyrinth = None
        self.artifacts = []
        self.mobs = []
        self.objects = []
        self.hero = None

    def get_hero(self) -> Hero:
        """
        Returns hero.
        :return: hero
        """
        return self.hero[1]

    def get_labyrinth(self) -> Labyrinth:
        """
        Returns labyrinth
        :return: labyrinth
        """
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

    def place_entities(self, entities_desc: dict):
        """
        Places entities from given dict to the game map.
        :param entities_desc:
            Dict entity_type -> count
        """
        cells = np.array([Position.as_position(row, column) for row, column in self.labyrinth.get_floor_cells()])
        np.random.shuffle(cells)

        i = 0
        for entity, count in entities_desc.items():
            for di in range(count):
                obj = to_class[entity](cells[i + di])

                if isinstance(obj, Artifact):
                    self.artifacts.append((entity, obj))
                elif isinstance(obj, Mob):
                    self.mobs.append((entity, obj))
                elif isinstance(obj, Hero):
                    self.hero = (entity, obj)
                else:
                    self.objects.append((entity, obj))
            i += count


