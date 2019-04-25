import curses
import logging
from functools import partial

from game.controller import Controller, StatusManager
from game.controller import UserInput
from game.elements import Character
from game.model import Model
from game.view.elements import scheme

KEY_BINDINGS = {
    curses.KEY_UP: UserInput.UP,
    curses.KEY_DOWN: UserInput.DOWN,
    curses.KEY_RIGHT: UserInput.RIGHT,
    curses.KEY_LEFT: UserInput.LEFT
}


class CursesView:
    """
    View of MVC model.

    Text interface based on Curses library.
    """

    def __init__(self, model: Model):
        self.model = model
        self.controller = None
        self.element_colors = {}

    def start(self, controller: Controller):
        """
        Start the drawing loop.

        :param controller:
            controller to work with
        """
        self.controller = controller
        curses.wrapper(partial(self.draw_scene))

    def draw_scene(self, screen):
        """
        Drawing loop.
        :param screen:
            curses screen
        """
        key_pressed = 0

        screen.clear()
        screen.refresh()

        self.initialise_colors()

        map_y = self.model.shape()[0]
        map_x = self.model.shape()[1]
        logging.debug(f"Map shape: y={map_y}, x={map_x}")
        map_pad = curses.newpad(map_y + 1, map_x + 1)  # pad should be +1 of it's working area

        while key_pressed != ord('q'):
            screen_height, screen_width = screen.getmaxyx()
            screen.clear()

            if key_pressed in KEY_BINDINGS:
                self.controller.process_input(KEY_BINDINGS[key_pressed])

            map_origin_y = screen_height // 2 - map_y // 2
            map_origin_x = screen_width // 2 - map_x // 2

            screen.refresh()

            self.draw_map(map_pad)
            map_pad.refresh(0, 0,
                            map_origin_y, map_origin_x,
                            min(map_origin_y + map_y, screen_height - 1), min(map_origin_x + map_x, screen_width - 1))

            self.draw_status_bar(screen)

            screen.refresh()
            key_pressed = screen.getch()

    def draw_element(self, window, y: int, x: int, element):
        """
        Draw an element in a given position.
        """
        window.attron(curses.color_pair(self.element_colors[element]))
        window.addstr(y, x, scheme[element].symbol.encode('utf-8'))
        window.attroff(curses.color_pair(self.element_colors[element]))

    def draw_map(self, pad):
        """
        Draws game map.
        :param pad:
            curses pad to draw on
        """
        for y, row in enumerate(self.model.labyrinth):
            for x, map_element in enumerate(row):
                self.draw_element(pad, y, x, map_element)

        for entity, instance in self.model.artifacts:
            y, x = instance.position
            self.draw_element(pad, y, x, entity)
        for entity, instance in self.model.mobs:
            y, x = instance.position
            self.draw_element(pad, y, x, entity)
        for entity, instance in self.model.objects:
            y, x = instance.position
            self.draw_element(pad, y, x, entity)

        y, x = self.model.get_hero().position
        self.draw_element(pad, y, x, Character.HERO)

    def draw_status_bar(self, screen):
        """
        Draws status bar.
        :param screen:
            curses screen
        """
        pass

    def initialise_colors(self):
        """
        Initialises curses color scheme.
        """
        curses.start_color()

        color_index = 1

        for element, visual in scheme.items():
            self.element_colors[element] = color_index
            curses.init_pair(color_index, visual.color.primary, visual.color.secondary)
            color_index += 1
