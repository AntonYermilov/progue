import numpy as np
from .map import Labyrinth, MapBlock


class MapLoader:
    @staticmethod
    def load_map(layout: np.ndarray) -> Labyrinth:
        mapping = {'.': MapBlock.FLOOR, '#': MapBlock.WALL}
        def apply(c):
            if c in mapping:
                return mapping[c]
            raise ValueError(f'Incorrect labyrinth layout.\nExpected: . or #\nFound: {c}')

        labyrinth = Labyrinth(layout.shape[0], layout.shape[1])
        labyrinth[:,:] = apply(layout)
        return labyrinth