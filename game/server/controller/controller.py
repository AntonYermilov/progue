import json
from pathlib import Path

import numpy as np

from game import Position
from game.server.controller.status_manager import StatusManager
from game.server.controller.user_input_processor import UserInputProcessor, UserInput
from game.model import Model

Direction = Position


class Controller:
    """
    Controller of MVC architecture.
    """

    def __init__(self, model: Model):
        """
        Initialises controller with given model.

        :param model: Model
            A model to work with
        """
        self.model = model
        self.status_manager = StatusManager()
        self.input_processor = UserInputProcessor(status_manager=self.status_manager, model=self.model)

        game_config_path = Path('resources', 'config', 'game_config.json')
        entities_config_path = Path('resources', 'config', 'entities.json')

        with game_config_path.open('r') as f:
            self.game_config = json.load(f)
        with entities_config_path.open('r') as f:
            self.entities_desc = json.load(f)

    def start_game(self):
        """
        Starts the game loop.
        """

        # TODO IMPLEMENT MULTIPLE CHARACTERS
        self.model.place_hero(self.game_config['hero'])

        mobs_number = np.random.randint(self.game_config['mobs']['min_mobs_count'],
                                        self.game_config['mobs']['max_mobs_count'] + 1)
        mob_names = list(self.entities_desc['mobs'].keys())
        for i in range(mobs_number):
            mob_name = np.random.choice(mob_names)
            self.model.place_new_mob(mob_name, self.entities_desc['mobs'][mob_name])

        items_number = np.random.randint(self.game_config['items']['min_items_count'],
                                         self.game_config['items']['max_items_count'] + 1)
        item_names = list(self.entities_desc['items'].keys())
        for i in range(items_number):
            item_name = np.random.choice(item_names)
            self.model.place_new_item(item_name, self.entities_desc['items'][item_name]['upd'])

    def on_player_action(self, player, action):
        # TODO COMMAND CREATION
        # hero_command = self.input_processor.process_input(user_input)
        hero_command = None
        hero_command.execute()

    def on_mob_turn(self):
        for mob in self.model.mobs:
            mob_command = mob.on_new_turn()
            mob_command.execute()
