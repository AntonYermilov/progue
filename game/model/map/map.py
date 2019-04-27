from dataclasses import dataclass
import numpy as np
from enum import Enum

from game import Position


class MapBlock(Enum):
    FLOOR = 0
    WALL = 1

    def is_wall(self):
        return self == MapBlock.WALL

    def is_floor(self):
        return self == MapBlock.FLOOR


@dataclass
class Labyrinth:
    rows: int
    columns: int
    labyrinth: np.ndarray
    wall: np.ndarray
    floor: np.ndarray

    def __init__(self, rows: int, columns: int, fill: MapBlock = MapBlock.WALL):
        self.rows = rows
        self.columns = columns
        self.labyrinth = np.zeros((rows, columns), dtype=np.object)
        self.labyrinth[:,:] = fill
        self.wall = self.labyrinth == MapBlock.WALL
        self.floor = self.labyrinth == MapBlock.FLOOR

    def __getitem__(self, key):
        if isinstance(key, Position):
            key = (key.get_row(), key.get_col())
        return self.labyrinth[key]

    def __setitem__(self, key, value):
        if isinstance(key, Position):
            key = (key.get_row(), key.get_col())
        self.labyrinth[key] = value
        self.wall[key] = self.labyrinth[key] == MapBlock.WALL
        self.floor[key] = self.labyrinth[key] == MapBlock.FLOOR

    def get_floor_cells(self) -> np.array:
        cells = np.array([[[i, j] for j in range(self.columns)] for i in range(self.rows)])
        return cells[self.floor]

    def is_wall(self, *args):
        if len(args) == 1 and isinstance(args[0], Position):
            row, col = args[0].get_row(), args[0].get_col()
        else:
            row, col = args
        return self.wall[row, col]

    def is_floor(self, *args):
        if len(args) == 1 and isinstance(args[0], Position):
            row, col = args[0].get_row(), args[0].get_col()
        else:
            row, col = args
        return self.floor[row, col]

    # Temporary function to test refactored code
    def visualize(self):
        cur = self.labyrinth.copy()
        cur[cur == MapBlock.FLOOR] = '.'
        cur[cur == MapBlock.WALL] = '#'
        return cur