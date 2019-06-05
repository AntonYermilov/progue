import subprocess
import time

from game.client.controller.network import Network
from game.client.view.user_command import UserCommand


class Menu:
    SINGLEPLAYER = 'Singleplayer'
    MULTIPLAYER_NEW = 'Create Multiplayer Game'
    MULTIPLAYER_CONNECT = 'Connect Multiplayer Game'
    EXIT = 'Exit'

    def __init__(self, view):
        self.network = Network()
        self.buttons = [
            self.SINGLEPLAYER,
            self.MULTIPLAYER_NEW,
            self.MULTIPLAYER_CONNECT,
            self.EXIT
        ]
        self.position = 0
        self.view = view
        self.server = None

    def _select_next(self):
        self.position += 1
        if self.position == len(self.buttons):
            self.position = 0

    def _select_prev(self):
        self.position -= 1
        if self.position < 0:
            self.position += len(self.buttons)

    def _start_singleplayer(self):
        self.server = subprocess.Popen(["python3", "-m", "game", "--server"])
        time.sleep(1)

        self.network.connect()
        self.network.create_game('game1')  # TODO REFACTOR
        return self.network

    def _start_multiplayer(self):
        self.network.connect()
        self.network.create_game('game1')  # TODO REFACTOR
        return self.network

    def _connect_multiplayer(self):
        self.network.connect()
        self.network.create_game('game1')  # TODO REFACTOR
        return self.network

    @staticmethod
    def _exit():
        return None

    def _apply_selection(self):
        return {0: self._start_singleplayer,
                1: self._start_multiplayer,
                2: self._connect_multiplayer,
                3: self._exit}[self.position]()

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
                return self._apply_selection()

    def destroy(self):
        if self.server:
            self.server.kill()