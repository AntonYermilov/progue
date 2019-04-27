import curses
import logging
from typing import Dict
from functools import partial

from game.controller import Controller, StatusManager
from game.controller import UserInput
from game.model import Model


KEY_BINDINGS = {
    curses.KEY_UP: UserInput.UP,
    curses.KEY_DOWN: UserInput.DOWN,
    curses.KEY_RIGHT: UserInput.RIGHT,
    curses.KEY_LEFT: UserInput.LEFT
}


COLOR_MAP = {
    'black': curses.COLOR_BLACK,
    'white': curses.COLOR_WHITE,
    'red': curses.COLOR_RED,
    'blue': curses.COLOR_BLUE,
    'cyan': curses.COLOR_CYAN,
    'green': curses.COLOR_GREEN,
    'magenta': curses.COLOR_MAGENTA,
    'yellow': curses.COLOR_YELLOW
}


class CursesView:
    """
    View of MVC model.

    Text interface based on Curses library.
    """

    def __init__(self, model: Model):
        self.model = model
        self.controller = None
        self.colors = {}

    def start(self, controller: Controller):
        """
        Start the drawing loop.

        :param controller: controller to work with
        """
        self.controller = controller
        curses.wrapper(partial(self.draw_scene))


    def draw_scene(self, screen):
        """
        Drawing loop.
        :param screen: curses screen
        """
        key_pressed = 0

        curses.curs_set(0)

        screen.clear()
        screen.refresh()
        screen.idcok(False)
        screen.idlok(False)

        map_y = self.model.get_labyrinth().rows
        map_x = self.model.get_labyrinth().columns
        logging.debug(f"Map shape: y={map_y}, x={map_x}")
        map_pad = curses.newpad(map_y + 1, map_x + 1)  # pad should be +1 of it's working area

        while key_pressed != ord('q'):
            screen_height, screen_width = screen.getmaxyx()

            if key_pressed in KEY_BINDINGS:
                self.controller.process_input(KEY_BINDINGS[key_pressed])

            map_origin_y = 0
            map_origin_x = 0

            screen.refresh()

            self.draw_map(map_pad)
            map_pad.refresh(0, 0,
                            map_origin_y, map_origin_x,
                            min(map_origin_y + map_y, screen_height - 1), min(map_origin_x + map_x, screen_width - 1))

            self.draw_status_bar(screen)

            screen.refresh()
            key_pressed = screen.getch()

    def get_color(self, element_desc: Dict):
        foreground = element_desc['foreground_color']
        background = element_desc['background_color']
        color = (foreground, background)

        if color not in self.colors:
            i = len(self.colors) + 1
            self.colors[color] = i
            curses.start_color()
            curses.init_pair(i, COLOR_MAP[background], COLOR_MAP[foreground])

        return curses.color_pair(self.colors[color])


    def draw_element(self, window, y: int, x: int, element_desc: Dict):
        """
        Draw an element in a given position.
        """
        window.attron(self.get_color(element_desc))
        window.addstr(y, x, element_desc['view'].encode('utf-8'))
        window.attroff(self.get_color(element_desc))

    def draw_map(self, pad):
        """
        Draws game map.
        :param pad: curses pad to draw on
        """
        labyrinth = self.model.get_labyrinth()
        for row in range(labyrinth.rows):
            for col in range(labyrinth.columns):
                cell_desc = self.controller.entities_desc['map']['wall' if labyrinth.is_wall(row, col) else 'floor']
                self.draw_element(pad, row, col, cell_desc)

        for mob in self.model.mobs:
            y, x = mob.position
            self.draw_element(pad, y, x, self.controller.entities_desc['mobs'][mob.name])

        y, x = self.model.get_hero().position
        self.draw_element(pad, y, x, self.controller.entities_desc['hero'])

    def draw_status_bar(self, screen):
        """
        Draws status bar.
        :param screen: curses screen
        """
        pass
