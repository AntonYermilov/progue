import subprocess
from abc import ABC
from typing import Union

from game import SAVE_FILE_NAME
from game.client.controller.network import Network
from game.client.view.user_command import UserCommand

"""
This class contains a simple description of menu
"""
class AbstractMenu(ABC):
    def __init__(self, buttons, active, view):
        self.buttons = buttons
        self.position = 0
        self.active = active
        self.view = view

    def _select_next(self):
        self.position += 1
        if self.position == len(self.buttons):
            self.position = 0

    def _select_prev(self):
        self.position -= 1
        if self.position < 0:
            self.position += len(self.buttons)


"""
This class describes behaviour of the menu for choosing multiplayer game.
"""
class GameChoiceMenu(AbstractMenu):
    def __init__(self, view, network):
        buttons = network.list_games() + ['Back']
        active = [True] * len(self.buttons)

        super().__init__(buttons, active, view)
        self.view.menu_pad.set_menu(self)

    """
    When choice is made, returns either multiplayer game id, or None if no game was selected
    """
    def make_choice(self) -> Union[str, None]:
        self.view.refresh_main_menu()
        if len(self.buttons) == 0:
            return None
        while True:
            cmd = self.view.get_user_command()
            if cmd == UserCommand.UP:
                self._select_prev()
                self.view.refresh_main_menu()
                continue
            if cmd == UserCommand.DOWN:
                self._select_next()
                self.view.refresh_main_menu()
                continue
            if cmd == UserCommand.ENTER:
                return self.buttons[self.position] if self.position + 1 < len(self.buttons) else None


"""
This class describes behaviour of the main menu
"""
class Menu(AbstractMenu):
    """
    Available main menu buttons
    """
    SINGLEPLAYER_NEW = 'New Singleplayer Game'
    SINGLEPLAYER_CONTINUE = 'Continue Singleplayer Game'
    MULTIPLAYER_NEW = 'New Multiplayer Game'
    MULTIPLAYER_CONNECT = 'Connect Multiplayer Game'
    EXIT = 'Exit'

    def __init__(self, view):
        buttons = [
            self.SINGLEPLAYER_NEW,
            self.SINGLEPLAYER_CONTINUE,
            self.MULTIPLAYER_NEW,
            self.MULTIPLAYER_CONNECT,
            self.EXIT
        ]
        active = [
            True,
            SAVE_FILE_NAME.exists(),
            True,
            True,
            True
        ]

        super().__init__(buttons, active, view)
        self.network = None
        self.server = None

    def _start_singleplayer(self):
        self.network = Network(addr='127.0.0.1:1489')
        self.server = subprocess.Popen(["python3", "-m", "game", "--server", "1489"])

        while True:
            try:
                self.network.create_game(singleplayer=True, load=False)
                break
            except:
                pass
        return self.network

    def _continue_singleplayer(self):
        if not self.active[1]:
            return None

        self.network = Network(addr='127.0.0.1:1489')
        self.server = subprocess.Popen(["python3", "-m", "game", "--server", "1489"])

        while True:
            try:
                self.network.create_game(singleplayer=True, load=True)
                break
            except:
                pass
        return self.network

    def _start_multiplayer(self):
        self.network = Network()
        try:
            self.network.create_game(singleplayer=False, load=False)
        except Exception as e:
            print(f'Failed to connect: {e}')
            return None
        return self.network

    def _connect_multiplayer(self):
        self.network = Network()
        try:
            game_id = GameChoiceMenu(self.view, self.network).make_choice()

            if game_id is not None:
                self.network.connect_to_game(game_id)
                self.view.menu_pad.set_menu(self)
            else:
                self.view.menu_pad.set_menu(self)
                self.view.refresh_main_menu()
                return None
        except Exception as e:
            print(f'Failed to connect: {e}')
            return None
        return self.network

    @staticmethod
    def _exit():
        return 'exit'

    def _apply_selection(self):
        return {0: self._start_singleplayer,
                1: self._continue_singleplayer,
                2: self._start_multiplayer,
                3: self._connect_multiplayer,
                4: self._exit}[self.position]()

    """
    When choice is made, returns the network we need to connect to. 
    It may be either a local network in case of a singleplayer game, or a global network (i.e. server)
    in case of a multiplayer game.
    """
    def make_choice(self) -> Network:
        self.view.refresh_main_menu()
        while True:
            cmd = self.view.get_user_command()
            if cmd == UserCommand.UP:
                self._select_prev()
                self.view.refresh_main_menu()
                continue
            if cmd == UserCommand.DOWN:
                self._select_next()
                self.view.refresh_main_menu()
                continue
            if cmd == UserCommand.ENTER:
                result = self._apply_selection()
                if result is None:
                    continue
                return result

    """
    Destroys menu and kills local server if it was created (for singleplayer only)
    """
    def destroy(self):
        if self.server:
            self.server.kill()
