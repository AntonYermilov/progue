from bearlibterminal import terminal
from typing import Dict

from game import Position
from game.client.model.model import Model


class View:
    def __init__(self, model: Model, entities_desc: Dict, *args, **kwargs):
        self.model = model
        self.entities_desc = entities_desc
        pass

    def _terminal_dimensions(self) -> (int, int):
        """
        Determines terminal dimensions depending on game config
        :return: x-dim size, y-dim size
        """
        return 78, 39  # TODO

    def initialize(self):
        terminal.open()
        w, h = self._terminal_dimensions()
        terminal.set(f'window: title=\'progue\', size={w}x{h};')

    @staticmethod
    def _set_tk_color(color: int, bkcolor: int):
        """
        Sets current foreground and background color which will be used by all output functions called later.
        Colors should be provided in TK (BGRA) format
        :param color: foreground color
        :param bkcolor: background color
        """
        terminal.color(color)
        terminal.bkcolor(bkcolor)

    @staticmethod
    def _set_color(color: str, bkcolor: str):
        """
        Sets current foreground and background color which will be used by all output functions called later.
        Color may be specified in a following ways: name, hexadecimal format, comma-separated format or an
        integer formatted to a string.
        :param color: foreground color
        :param bkcolor: background color
        """
        View._set_tk_color(terminal.color_from_name(color), terminal.color_from_name(bkcolor))

    @staticmethod
    def _put_symbol(x: int, y: int, c: str):
        """
        Puts a symbol into a specified position
        :param x: x-coordinate
        :param y: y-coordinate
        :param c: symbol to be printed
        """
        terminal.put(int(x), int(y), ord(c))

    @staticmethod
    def _put_colored_symbol(x: int, y: int, c: str, color: str, bkcolor: str):
        """
        Puts a symbol into a specified position
        :param x: x-coordinate
        :param y: y-coordinate
        :param c: symbol to be printed
        :param color: foreground color
        :param bkcolor: background color
        :return:
        """
        View._set_color(color, bkcolor)
        View._put_symbol(int(x), int(y), c)

    @staticmethod
    def _put_text(x: int, y: int, s: str):
        """
        Puts a text into a specified position
        :param x: x-coordinate
        :param y: y-coordinate
        :param s: text to be printed
        """
        terminal.printf(int(x), int(y), s)

    @staticmethod
    def _put_colored_text(x: int, y: int, s: str, color: str, bkcolor: str):
        """
        Puts a text into a specified position
        :param x: x-coordinate
        :param y: y-coordinate
        :param s: text to be printed
        :param color: foreground color
        :param bkcolor: background color
        """
        View._set_color(color, bkcolor)
        View._put_text(int(x), int(y), s)

    def _refresh_map(self):
        labyrinth = self.model.labyrinth
        for row in range(labyrinth.rows):
            for col in range(labyrinth.columns):
                position = Position.as_position(row, col)
                cell_desc = self.entities_desc['map']['wall' if labyrinth.is_wall(position) else 'floor']
                view, color, bkcolor = cell_desc['view'], cell_desc['foreground_color'], cell_desc['background_color']
                self._put_colored_symbol(x=position.get_x(), y=position.get_y(), c=view, color=color, bkcolor=bkcolor)

    def _refresh_items(self):
        items = self.model.items
        for item in items:
            x, y = item.position.get_x(), item.position.get_y()
            item_desc = self.entities_desc['items'][item.name]
            view, color, bkcolor = item_desc['view'], item_desc['foreground_color'], item_desc['background_color']
            self._put_colored_symbol(x=x, y=y, c=view, color=color, bkcolor=bkcolor)

    def _refresh_enemies(self):
        enemies = self.model.mobs
        for enemy in enemies:
            x, y = enemy.position.get_x(), enemy.position.get_y()
            enemy_desc = self.entities_desc['mobs'][enemy.name]
            view, color, bkcolor = enemy_desc['view'], enemy_desc['foreground_color'], enemy_desc['background_color']
            self._put_colored_symbol(x=x, y=y, c=view, color=color, bkcolor=bkcolor)

    def _refresh_hero(self):
        hero = self.model.hero
        x, y = hero.position.get_x(), hero.position.get_y()
        hero_desc = self.entities_desc['hero']
        view, color, bkcolor = hero_desc['view'], hero_desc['foreground_color'], hero_desc['background_color']
        self._put_colored_symbol(x=x, y=y, c=view, color=color, bkcolor=bkcolor)

    def refresh(self):
        self._refresh_map()
        self._refresh_items()
        self._refresh_enemies()
        self._refresh_hero()
        terminal.refresh()

    @staticmethod
    def get_user_command():
        return terminal.read()

    @staticmethod
    def delay(sec: float):
        terminal.delay(int(sec * 1000))

    @staticmethod
    def destroy():
        terminal.close()
