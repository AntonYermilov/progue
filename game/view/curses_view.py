import curses
import logging
from functools import partial
from typing import Dict

from game.controller import Controller
from game.model import Model
from game.view.bindings import KEY_BINDINGS, LEGEND

COLOR_MAP = {
    'black': curses.COLOR_BLACK,
    'white': curses.COLOR_WHITE,
    'grey': 110,
    'red': curses.COLOR_RED,
    'blue': curses.COLOR_BLUE,
    'cyan': curses.COLOR_CYAN,
    'green': curses.COLOR_GREEN,
    'magenta': curses.COLOR_MAGENTA,
    'yellow': curses.COLOR_YELLOW,
    'orange': 166,
    'marine': 30,
    'parchment': 222,
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
1
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

        legend_y, legend_x = self.get_text_dimensions(LEGEND)
        legend_pad = curses.newpad(legend_y + 1, legend_x + 1)

        stats_y, stats_x = 3, 25
        stats_pad = curses.newpad(stats_y, stats_x)

        inventory_y, inventory_x = self.model.hero.limit + 5, 25
        inventory_pad = curses.newpad(inventory_y, inventory_x)

        while key_pressed != ord('q'):
            screen.refresh()

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

            self.draw_legend(legend_pad)
            legend_pad.refresh(0, 0,
                               map_y + 1, 0,
                               min(map_y + 1 + legend_y, screen_height - 1),
                               min(legend_x, screen_width - 1))

            self.draw_stats(stats_pad, self.model.get_hero().stats)
            stats_pad.refresh(0, 0,
                              0, map_x + 1,
                              min(stats_y, screen_height - 1),
                              min(map_x + 1 + stats_x, screen_width - 1))

            inventory_desc = self.get_inventory_list()
            self.draw_inventory(inventory_pad, inventory_desc)
            inventory_pad.refresh(0, 0,
                                  stats_y, map_x + 1,
                                  min(stats_y + inventory_y, screen_height - 1),
                                  min(map_x + 1 + inventory_x, screen_width - 1))

            screen.refresh()
            key_pressed = screen.getch()

    def get_inventory_list(self):
        return 'Inventory (15 items max):\n' + '\n'.join(
            [str(i) + '. ' + item.name + (' *' if item == self.model.current_item else '') for i, item in
             enumerate(self.model.hero.inventory)])

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

        for item in self.model.items:
            y, x = item.position
            self.draw_element(pad, y, x, self.controller.entities_desc['items'][item.name])

        for mob in self.model.mobs:
            y, x = mob.position
            self.draw_element(pad, y, x, self.controller.entities_desc['mobs'][mob.name])

        y, x = self.model.get_hero().position
        self.draw_element(pad, y, x, self.controller.entities_desc['hero'])

    @staticmethod
    def draw_legend(pad):
        """
        Draws map legend.
        :param screen: curses screen
        """
        pad.addstr(0, 0, LEGEND)

    @staticmethod
    def get_text_dimensions(text):
        rows = text.split('\n')
        return len(LEGEND.split('\n')), max(len(row) for row in rows)

    @staticmethod
    def draw_inventory(pad, inventory_desc):
        pad.clear()
        pad.addstr(0, 0, inventory_desc)

    @staticmethod
    def draw_stats(pad, stats):
        pad.clear()
        health = f'Health: {int(100 * stats.health /stats.max_health)}%'
        pad.addstr(1, 0, health)
