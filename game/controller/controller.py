from enum import Enum
from pathlib import Path
import json
import numpy as np

from game.client.controller.network import Network
from game.client.model.action import Action, ActionType, ItemAction
from game.controller.command import MoveCommand, AttackCommand
from game.controller.command.drop_item_command import DropItemCommand
from game.controller.command.pick_command import PickCommand
from game.controller.command.use_item_command import UseItemCommand
from game.controller.status_manager import StatusManager
from game.controller.user_input_processor import UserInputProcessor, UserInput
from game.model import Model
from game import Position

import game.client.controller.controller as cli


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

        # Sorry @karvozavr and @oquechy, but TODO REFACTOR THIS SHIT
        game_config_path = Path('resources', 'config', 'game_config.json')
        entities_config_path = Path('resources', 'config', 'entities.json')

        with game_config_path.open('r') as f:
            self.game_config = json.load(f)
        with entities_config_path.open('r') as f:
            self.entities_desc = json.load(f)

    def start_game(self, view):
        """
        Starts the game loop.

        :param view: View
            View to work with
        """

        # TODO and this shit too
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

        # view.start(controller=self)
        cli_controller = cli.Controller(Network(self))
        cli_controller.start_game()

    def process_input(self, action: Action):
        """
        Processes user input.
        """
        commands = []
        if action.type == ActionType.MOVE_ACTION:
            position = Position.as_position(action.desc.row, action.desc.column)
            self._update_commands_with_move_action(commands, position)
        elif action.type == ActionType.INVENTORY_ACTION:
            item_id = action.desc.item_id
            item_action = action.desc.action
            self._update_commands_with_inventory_action(commands, item_id, item_action)

        for hero_command in commands:
            hero_command.execute()

        for mob in self.model.mobs:
            mob_command = mob.on_new_turn()
            mob_command.execute()

    def _update_commands_with_inventory_action(self, commands, item_id, item_action):
        character = self.model.hero
        if item_action == ItemAction.DROP:
            hero_command = DropItemCommand(self.model, item_id)
            commands.append(hero_command)
        elif item_action == ItemAction.USE:
            hero_command = UseItemCommand(self.model, item_id)
            commands.append(hero_command)
        self._update_commands_with_move_action(commands, character.position)

    def _update_commands_with_move_action(self, commands, position):
        character = self.model.hero
        enemy, item = None, None
        for _mob in self.model.mobs:
            if _mob.position == position:
                enemy = _mob
        for _item in self.model.items:
            if _item.position == position:
                item = _item

        if enemy is not None:
            hero_command = AttackCommand(character, enemy, self.model)
            commands.append(hero_command)
        elif item is not None:
            hero_command = PickCommand(character, item, self.model, position)
            commands.append(hero_command)
        else:
            hero_command = MoveCommand(character, position)
            commands.append(hero_command)