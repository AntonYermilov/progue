from dataclasses import dataclass
import numpy as np

from game.elements import MapBlock


@dataclass
class Labyrinth:
    rows: int
    columns: int
    labyrinth: np.ndarray
    is_wall: np.ndarray
    is_floor: np.ndarray

    def __init__(self, rows: int, columns: int, fill: MapBlock = MapBlock.WALL):
        self.rows = rows
        self.columns = columns
        self.labyrinth = np.zeros((rows, columns), dtype=np.object)
        self.labyrinth[:,:] = fill
        self.is_wall = self.labyrinth == MapBlock.WALL
        self.is_floor = self.labyrinth == MapBlock.FLOOR

    def __getitem__(self, key):
        return self.labyrinth[key]

    def __setitem__(self, key, value):
        self.labyrinth[key] = value
        self.is_wall[key] = self.labyrinth[key] == MapBlock.WALL
        self.is_floor[key] = self.labyrinth[key] == MapBlock.FLOOR

    def get_floor_cells(self) -> np.array:
        cells = np.array([[[i, j] for j in range(self.columns)] for i in range(self.rows)])
        return cells[self.is_floor]

    # Temporary function to test refactored code
    def visualize(self):
        cur = self.labyrinth.copy()
        cur[cur == MapBlock.FLOOR] = '.'
        cur[cur == MapBlock.WALL] = '#'
        return cur