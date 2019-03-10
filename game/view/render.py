from game.model import Model
from game.view.elements import scheme


def print_map(m: Model):
    layout = [[None] * len(m.labyrinth[0]) for _ in range(len(m.labyrinth))]
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            layout[i][j] = scheme[m.labyrinth[i][j]].symbol
    for entity, instance in m.entities:
        i, j = instance.position
        layout[i][j] = scheme[entity].symbol
    for row in layout:
        for symbol in row:
            print(symbol, end='')
        print()


def render(m: Model):
    print_map(m)
