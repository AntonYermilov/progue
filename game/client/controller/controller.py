import json
from pathlib import Path

from game.client.model.action import Action
from game.client.model.model import Model
from game.client.view.view import View
from game.client.controller.network import Network


class Controller:
    FRAMES_PER_SECOND = 20
    GAME_CONFIG_PATH = Path('resources', 'config', 'game_config.json')
    ENTITIES_CONFIG_PATH = Path('resources', 'config', 'entities.json')

    def __init__(self, network: Network, *args, **kwargs):
        with self.GAME_CONFIG_PATH.open('r') as src:
            self.game_config = json.load(src)
        with self.ENTITIES_CONFIG_PATH.open('r') as src:
            self.entities_desc = json.load(src)
        self.network = network
        self.model = Model()
        self.view = View(self.model, self.entities_desc)

    def start_game(self):
        self.view.initialize()
        self.network.connect()
        while True:
            state = self.network.get_state()
            self.model.update(state)
            self.view.refresh()
            if state.my_turn:
                action = self.get_user_action()
                self.network.send_action(action)
            self.view.delay(1.0 / self.FRAMES_PER_SECOND)

    def get_user_action(self) -> Action:
        pass