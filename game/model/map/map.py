from dataclasses import dataclass
import numpy as np
from enum import Enum

from game import Position, Direction


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
    void: np.ndarray

    def __init__(self, rows: int, columns: int, fill: MapBlock = MapBlock.WALL):
        self.rows = rows
        self.columns = columns
        self.labyrinth = np.zeros((rows, columns), dtype=np.object)
        self.labyrinth[:,:] = fill
        self.wall = self.labyrinth == MapBlock.WALL
        self.floor = self.labyrinth == MapBlock.FLOOR
        self.void = None

    def initialize_void_cells(self):
        self.void = np.zeros((self.rows, self.columns), dtype=np.bool)
        for i in range(self.rows):
            for j in range(self.columns):
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if 0 <= i + di < self.rows and 0 <= j + dj < self.columns:
                            self.void[i, j] |= self.labyrinth[i + di, j + dj] == MapBlock.FLOOR
        self.void = np.invert(self.void)

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

    def is_void(self, *args):
        if len(args) == 1 and isinstance(args[0], Position):
            row, col = args[0].get_row(), args[0].get_col()
        else:
            row, col = args
        return self.void[row, col]

    def get_distances(self, position: Position, max_dist: int) -> np.ndarray:
        queue = []
        head, tail = 0, 0
        dist = np.zeros((self.rows, self.columns), dtype=np.int32)
        dist[:,:] = 1 << 30

        dist[position.row, position.col] = 0
        queue.append((position.row, position.col))
        tail += 1

        while head < tail:
            (i, j) = queue[head]
            head += 1

            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if dist[i, j] + 1 < dist[i + di, j + dj]:
                    dist[i + di, j + dj] = dist[i, j] + (1 if di == 0 else 2)
                    if self.floor[i + di, j + dj] and dist[i + di, j + dj] < max_dist:
                        queue.append((i + di, j + dj))
                        tail += 1
            for di, dj in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                if self.wall[i + di, j + dj] and dist[i, j] + 1 < dist[i + di, j + dj]:
                    dist[i + di, j + dj] = dist[i, j] + (1 if di == 0 else 2)

        return dist
