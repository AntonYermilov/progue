import curses
import logging
from functools import partial

from game.controller import Controller, Action
from game.model import Model
from game.view.elements import scheme

KEY_BINDINGS = {
    curses.KEY_UP: Action.MOVE_UP,
    curses.KEY_DOWN: Action.MOVE_DOWN,
    curses.KEY_RIGHT: Action.MOVE_RIGHT,
    curses.KEY_LEFT: Action.MOVE_LEFT
}


class CursesView:

    def __init__(self, model: Model):
        self.model = model
        self.controller = None
        self.element_colors = {}

    def start(self, controller: Controller):
        self.controller = controller
        curses.wrapper(partial(self.draw_scene))

    def draw_scene(self, screen):
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
        window.attron(curses.color_pair(self.element_colors[element]))
        window.addstr(y, x, scheme[element].symbol.encode('utf-8'))
        window.attroff(curses.color_pair(self.element_colors[element]))

    def draw_map(self, pad):
        for y, row in enumerate(self.model.labyrinth):
            for x, map_element in enumerate(row):
                self.draw_element(pad, y, x, map_element)

        for entity, instance in self.model.entities:
            y, x = instance.position
            self.draw_element(pad, y, x, entity)

    def draw_status_bar(self, screen):
        pass

    def initialise_colors(self):
        curses.start_color()

        color_index = 1

        for element, visual in scheme.items():
            self.element_colors[element] = color_index
            curses.init_pair(color_index, visual.color.primary, visual.color.secondary)
            color_index += 1
