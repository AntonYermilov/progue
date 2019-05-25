import logging

from game.controller import Controller
from game.model import Model
from game.view import CursesView

import numpy as np


def setup_logging():
    logging.basicConfig(filename='progue.log', level=logging.DEBUG)


def setup_labyrinth(model):
    while True:
        map_loading_mode = input('Type:\n'
                                 '\t0 - to generate new level automatically\n'
                                 '\t1 - to upload a custom layout\n'
                                 '\tq - to quit\n')

        if map_loading_mode == 'q':
            exit(0)

        if map_loading_mode not in ['0', '1']:
            continue

        map_loading_mode = int(map_loading_mode)
        if map_loading_mode:
            filename = input(
                'Layout is a 15x30 rectangle of dots \'.\' representing floor '
                'and sharp symbols \'#\' representing labyrinth walls.\n'
                'Insert a file name to load layout: ')
            try:
                with open(filename, 'r') as f:
                    layout = np.array([line.strip() for line in f.readlines() if not line.isspace()], dtype=np.str)
                    correct = lambda c: c == '.' or c == '#'
                    if not correct(layout).all():
                        print('Layout should only contain dots or sharp symbols')
                        continue
                    if layout.shape != (15, 30):
                        print('Layout should be 15x30 rectangle')
                        continue
                    model.upload_labyrinth(layout)
            except IOError:
                print('Can\'t read from file ', filename)
                continue
        else:
            model.generate_labyrinth(rows=19, columns=19, free_cells_ratio=0.3)

        break


def main():
    setup_logging()
    logging.info('Initialised')

    model = Model()
    setup_labyrinth(model)

    view = CursesView(model)
    game_controller = Controller(model)

    game_controller.start_game(view)


if __name__ == "__main__":
    main()
