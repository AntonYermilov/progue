from .map import Labyrinth
from game.elements import MapBlock
import numpy as np


class MapGenerator:
    MOVES = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]], dtype=np.int32)

    def __init__(self):
        self.is_visited = None
        self.rand_directions = None
        self.rows = None
        self.columns = None
        self.prob = None

    def _on_map(self, i: int, j: int) -> bool:
        return 0 <= i < self.rows and 0 <= j < self.columns

    @staticmethod
    def _remove_isolated_cells(labyrinth: Labyrinth) -> Labyrinth:
        for i in range(1, labyrinth.rows - 1):
            for j in range(1, labyrinth.columns - 1):
                is_isolated = labyrinth.wall[i, j]
                for di, dj in MapGenerator.MOVES:
                    is_isolated &= labyrinth.floor[i + di, j + dj]
                if is_isolated:
                    labyrinth[i, j] = MapBlock.FLOOR
        return labyrinth

    def _dfs(self, i: int, j: int):
        inside_visited = True
        correct_moves = np.zeros(4, dtype=np.bool)
        for k, (di, dj) in enumerate(MapGenerator.MOVES):
            correct_moves[k] = self._on_map(i + di, j + dj)
            if correct_moves[k]:
                inside_visited &= self.is_visited[i + di, j + dj]
        if inside_visited:
            return

        self.is_visited[i, j] = True
        self.rand_directions[i, j] = []

        correct_moves = np.arange(MapGenerator.MOVES.shape[0])[correct_moves]
        direction = MapGenerator.MOVES[np.random.choice(correct_moves)]
        self.rand_directions[i, j].append(direction)
        if not self.is_visited[i + direction[0], j + direction[1]]:
            self._dfs(i + direction[0], j + direction[1])

        np.random.shuffle(correct_moves)
        for move in MapGenerator.MOVES[correct_moves]:
            di, dj = move
            if np.random.random() < self.prob:
                self.rand_directions[i, j].append(move)
                if not self.is_visited[i + di, j + dj]:
                    self._dfs(i + di, j + dj)

    def _generate(self, rows: int, columns: int, prob: float) -> Labyrinth:
        self.is_visited = np.zeros((rows, columns), dtype=np.int32)
        self.rand_directions = np.zeros((rows, columns), dtype=np.object)
        self.rand_directions.fill(None)
        self.rows, self.columns, self.prob = rows, columns, prob

        self._dfs(rows // 2, columns // 2)

        labyrinth = Labyrinth(2 * rows + 1, 2 * columns + 1, MapBlock.WALL)
        for i in range(self.rand_directions.shape[0]):
            for j in range(self.rand_directions.shape[1]):
                directions = self.rand_directions[i, j]
                if directions is None:
                    continue

                r, c = 2 * i + 1, 2 * j + 1
                for dr, dc in directions:
                    for k in range(3):
                        if 0 <= r + dr * k < 2 * rows + 1:
                            labyrinth[r + dr * k, c] = MapBlock.FLOOR
                        if 0 <= c + dc * k < 2 * columns + 1:
                            labyrinth[r, c + dc * k] = MapBlock.FLOOR

        return MapGenerator._remove_isolated_cells(labyrinth)

    @staticmethod
    def _scale(labyrinth: Labyrinth, scale_rows: float, scale_columns: float) -> Labyrinth:
        new_rows = int(labyrinth.rows * scale_rows)
        new_columns = int(labyrinth.columns * scale_columns)
        new_labyrinth = Labyrinth(new_rows, new_columns, MapBlock.WALL)

        for i in range(new_labyrinth.rows):
            for j in range(new_labyrinth.columns):
                new_labyrinth[i, j] = labyrinth[int(i / scale_rows), int(j / scale_columns)]
        return new_labyrinth

    def generate(self, rows: int, columns: int, free_cells_ratio: float = 0.5, prob: float = 0.25,
                 scale_rows: float = 1.0, scale_columns: float = 2.0) -> Labyrinth:
        labyrinth = Labyrinth(rows, columns, MapBlock.WALL)
        while labyrinth.floor.sum() < free_cells_ratio * labyrinth.rows * labyrinth.columns:
            labyrinth = self._generate(rows, columns, prob)
        return self._scale(labyrinth, scale_rows, scale_columns)
