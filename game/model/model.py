import random

from game.elements import MapBlock, Character
from game.model.character import Hero
from game.model.elements import to_class

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def on_map(m, i, j):
    n = len(m)
    return 0 <= i < n and 0 <= j < n


def is_visited(m, i, j):
    return m[i][j] is not None


def is_wall(labyrinth, i, j):
    return labyrinth[i][j] == MapBlock.WALL


def remove_isolated_cells(labyrinth):
    for i, row in enumerate(labyrinth):
        for j, cell in enumerate(row):
            if is_wall(labyrinth, i, j) and \
                    all(not is_wall(labyrinth, i + di, j + dj) for di, dj in moves if
                        on_map(labyrinth, i + di, j + dj)):
                labyrinth[i][j] = MapBlock.FLOOR
    return labyrinth


def generate_labyrinth(n, prob):
    m = [[None] * n for _ in range(n)]

    def dfs(i, j):
        if not on_map(m, i, j) or \
                is_visited(m, i, j) or \
                all(is_visited(m, i + di, j + dj) for di, dj in moves if on_map(m, i + di, j + dj)):
            return

        m[i][j] = []

        direction = random.choice(moves)
        while direction:
            new_i, new_j = i + direction[0], j + direction[1]
            if on_map(m, new_i, new_j) and not is_visited(m, new_i, new_j):
                m[i][j].append(direction)
                dfs(new_i, new_j)
                direction = None
            else:
                direction = random.choice(moves)

        random.shuffle(moves)
        for di, dj in moves:
            if random.random() < prob:
                if 0 <= i + di < n and 0 <= j + dj < n:
                    m[i][j].append((di, dj))
                    dfs(i + di, j + dj)

    dfs(n // 2, n // 2)

    size = 2 * n + 1
    labyrinth = [[MapBlock.WALL] * size for _ in range(size)]
    for i, row in enumerate(m):
        for j, directions in enumerate(row):
            if directions is not None:
                for di, dj in directions:
                    li, lj = 1 + 2 * i, 1 + 2 * j
                    for k in range(3):
                        labyrinth[li + di * k][lj] = MapBlock.FLOOR
                    for k in range(3):
                        labyrinth[li][lj + dj * k] = MapBlock.FLOOR

    return remove_isolated_cells(labyrinth)


def scale_labyrinth(m, cell_height, cell_width):
    labyrinth = [[None] * len(m) * cell_width for _ in range(len(m) * cell_height)]
    for i, row in enumerate(m):
        for j, cell in enumerate(row):
            li, lj = i * cell_height, j * cell_width
            for di in range(cell_height):
                for dj in range(cell_width):
                    labyrinth[li + di][lj + dj] = m[i][j]
    return labyrinth


def labyrinth_len(labyrinth):
    floor_cells = 0
    for row in labyrinth:
        for cell in row:
            floor_cells += cell is MapBlock.FLOOR
    return floor_cells


def floor_cells(labyrinth):
    cells = []
    for i, row in enumerate(labyrinth):
        for j, cell in enumerate(row):
            if cell is MapBlock.FLOOR:
                cells.append((i, j))
    return cells


class Model:

    def __init__(self):
        self.labyrinth = []
        self.entities = []
        self.hero = None

    def shape(self):
        return len(self.labyrinth), len(self.labyrinth[0])

    def get_hero(self) -> Hero:
        return self.hero[1]

    def generate_labyrinth(self, base_side_length, min_labyrinth_size, factor=0.25, scale_h=1, scale_w=2):
        while labyrinth_len(self.labyrinth) < min_labyrinth_size:
            self.labyrinth = generate_labyrinth(base_side_length, factor)
            self.labyrinth = scale_labyrinth(self.labyrinth, scale_h, scale_w)

    def place_entities(self, entities: dict):
        cells = floor_cells(self.labyrinth)
        random.shuffle(cells)
        i = 0
        for entity, count in entities.items():
            for di in range(count):
                self.entities.append((entity, to_class[entity](cells[i + di])))
                if entity == Character.HERO:
                    self.hero = self.entities[-1]
            i += count
