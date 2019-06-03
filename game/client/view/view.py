from typing import Dict, List, Tuple

from bearlibterminal import terminal

from game.client.model.model import Model
from game.client.view.pad.legend import LegendPad
from game.client.view.pad.map import MapPad
from game.client.view.pad.pad import Pad


class View:
    def __init__(self, model: Model, entities_desc: Dict, *args, **kwargs):
        self.model = model
        self.entities_desc = entities_desc
        self.pads: List[Pad] = None
        pass

    @staticmethod
    def _generate_config(width: int, height: int):
        return f'window: title=\'progue\', size={width}x{height};' \
               f'font: resources/fonts/Menlo-Regular.ttf, size=10, spacing=0x0;'

    def _create_pads(self):
        map = MapPad(self, 0, 0, self.model.labyrinth.columns, self.model.labyrinth.rows)
        legend = LegendPad(self, 0, map.y1, map.x1, map.y1 + 1)
        self.pads = [map, legend]

    def initialize(self):
        terminal.open()
        self._create_pads()
        width = max(pad.x1 for pad in self.pads)
        height = max(pad.y1 for pad in self.pads)
        terminal.set(self._generate_config(width, height))

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

    def refresh(self):
        for pad in self.pads:
            pad.refresh()
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
