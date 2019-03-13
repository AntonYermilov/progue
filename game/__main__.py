import logging

from game.controller import Controller
from game.elements import Artifact, Character, Object
from game.model import Model
from game.view import CursesView


def setup_logging():
    logging.basicConfig(filename='progue.log', level=logging.DEBUG)


def main():
    setup_logging()
    logging.info("Initialised")

    model = Model()
    model.generate_labyrinth(base_side_length=7, min_labyrinth_size=190)
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
