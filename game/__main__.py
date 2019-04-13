import logging

from game.controller import Controller
from game.elements import Artifact, Character, Object
from game.model import Model
from game.view import CursesView


def setup_logging():
    logging.basicConfig(filename='progue.log', level=logging.DEBUG)


def setup_labyrinth(model):
    while True:
        map_loading_mode = input('Type:\n'
                                 '\t0 - to generate new level automatically\n'
                                 '\t1 - to upload a custom layout\n')
        if map_loading_mode != '0' and map_loading_mode != '1':
            continue

        map_loading_mode = int(map_loading_mode)
        if map_loading_mode:
            filename = input(
                'Layout is a 15x30 rectangle of dots \'.\' representing floor '
                'and sharp symbols \'#\' representing labyrinth walls.\n'
                'Insert a file name to load layout: ')
            try:
                with open(filename, 'r') as f:
                    layout = f.readlines()
                    layout = [line.strip() for line in layout if not line.isspace()]
                    if not all(all(c == '.' or c == '#' for c in line) for line in layout):
                        print('Layout should only contain dots or sharp symbols')
                        continue
                    if not all(len(l) == 30 for l in layout) or len(layout) != 15:
                        print('Layout should be 15x30 rectangle')
                        continue
                    model.upload_labyrinth(layout)
            except IOError:
                print('Can\'t read from file ', filename)
                continue
        else:
            model.generate_labyrinth(base_side_length=7, min_labyrinth_size=190)

        break


def main():
    setup_logging()
    logging.info('Initialised')

    model = Model()
    setup_labyrinth(model)

    model.place_entities({Artifact.GOLD: 10,
                          Character.GHOST: 5,
                          Character.SNAKE: 5,
                          Artifact.HEALING_POTION: 5,
                          Artifact.KNOWLEDGE_SCROLL: 5,
                          Character.HERO: 1,
                          Object.EXIT: 1})

    view = CursesView(model)
    game_controller = Controller(model)

    game_controller.start_game(view)


if __name__ == "__main__":
    main()
