from typing import Dict, List

from bearlibterminal import terminal

from game.client.model.model import Model
from game.client.view.pad.inventory import InventoryPad
from game.client.view.pad.legend import LegendPad
from game.client.view.pad.map import MapPad
from game.client.view.pad.menu import MenuPad
from game.client.view.pad.pad import Pad
from game.client.view.pad.stats import StatsPad
from game.client.view.user_command import UserCommand


class View:
    def __init__(self, controller, model: Model, entities_desc: Dict, *args, **kwargs):
        self.controller = controller
        self.model = model
        self.entities_desc = entities_desc
        self.game_pads: List[Pad] = None
        self.menu_pad = None

    @staticmethod
    def _generate_config(width: int, height: int):
        return f'window: title=\'progue\', size={width}x{height};' \
               f'font: resources/fonts/Menlo-Regular.ttf, size=10, spacing=0x0;'

    def _create_pads(self):
        # TODO maybe this should be added to config?
        stats = StatsPad(self, 0, 0, 21, 41)
        map = MapPad(self, 21, 2, 99, 41)
        legend = LegendPad(self, 0, 41, 104, 43)
        inventory = InventoryPad(self, 79, 0, 104, 41)
        self.game_pads = [stats, map, legend, inventory]
        self.menu_pad = MenuPad(self, 37, 18, 67, 24)

    def initialize(self):
        terminal.open()
        self._create_pads()
        width = max(pad.x1 for pad in self.game_pads)
        height = max(pad.y1 for pad in self.game_pads)
        terminal.set(self._generate_config(width, height))

    @staticmethod
    def _set_layer(layer: int):
        """
        Sets current layer.
        The argument is an index from 0 to 255 where 0 is the lowest (default) layer.
        """
        terminal.layer(layer)

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

    def refresh_main_menu(self):
        void = self.entities_desc['map']['void']['background_color']
        self._set_color(void, void)
        terminal.clear()

        self.menu_pad.refresh()
        terminal.refresh()

    def refresh_game(self):
        void = self.entities_desc['map']['void']['background_color']
        self._set_color(void, void)
        terminal.clear()

        map_pad, stats_pad = None, None
        for pad in self.game_pads:
            pad.refresh()
            if isinstance(pad, MapPad):
                map_pad = pad
            if isinstance(pad, StatsPad):
                stats_pad = pad
        stats_pad.refresh_enemies(map_pad.get_visible_enemies())

        terminal.refresh()

    @staticmethod
    def get_user_command() -> UserCommand:
        cmd = terminal.read()
        try:
            cmd = UserCommand(cmd)
        except ValueError:
            cmd = UserCommand.UNKNOWN
        return cmd

    @staticmethod
    def clear_user_command_queue():
        while terminal.has_input():
            terminal.read()

    @staticmethod
    def delay(sec: float):
        terminal.delay(int(sec * 1000))

    @staticmethod
    def destroy():
        terminal.close()
