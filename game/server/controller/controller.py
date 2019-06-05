import json
from pathlib import Path

import numpy as np

from game import Position
from game.client.model.action import Action, ActionType, ItemAction
from game.model import Model
from game.server.controller import StatusManager
from game.server.controller.command import DropItemCommand
from game.server.controller.command import MoveCommand, AttackCommand
from game.server.controller.command import PickCommand
from game.server.controller.command import UseItemCommand


class Controller:
    """
    Controller of MVC architecture.
    """

    def __init__(self, model: Model):
        """
        Initialises controller with given mod`el.

        :param model: Model
            A model to work with
        """
        self.model = model
        self.status_manager = StatusManager()

        game_config_path = Path('resources', 'config', 'game_config.json')
        entities_config_path = Path('resources', 'config', 'entities.json')

        with game_config_path.open('r') as f:
            self.game_config = json.load(f)
        with entities_config_path.open('r') as f:
            self.entities_desc = json.load(f)

    def start_game(self, player_id: str):
        """
        Starts the game loop.

        :param player_id: str
            Player id
        """

        self.add_player(player_id)
        self.place_mobs()
        self.place_items()

    def add_player(self, player_id):
        self.model.place_hero(player_id, self.game_config['hero'])
        self.get_player(player_id).set_name(player_id)
        print('Connected: ', self.get_player(player_id))

    def place_items(self):
        items_number = np.random.randint(self.game_config['items']['min_items_count'],
                                         self.game_config['items']['max_items_count'] + 1)
        item_names = list(self.entities_desc['items'].keys())
        for i in range(items_number):
            item_name = np.random.choice(item_names)
            self.model.place_new_item(item_name, self.entities_desc['items'][item_name]['upd'])

    def place_mobs(self):
        mobs_number = np.random.randint(self.game_config['mobs']['min_mobs_count'],
                                        self.game_config['mobs']['max_mobs_count'] + 1)
        mob_names = list(self.entities_desc['mobs'].keys())
        for i in range(mobs_number):
            mob_name = np.random.choice(mob_names)
            self.model.place_new_mob(mob_name, self.entities_desc['mobs'][mob_name])

    def on_action(self, player_id: str, action: Action):
        """
        Processes user input.
        """
        commands = []
        if action.type == ActionType.MOVE_ACTION:
            position = Position.as_position(action.desc.row, action.desc.column)
            self._update_commands_with_move_action(player_id, commands, position)
        elif action.type == ActionType.INVENTORY_ACTION:
            item_id = action.desc.item_id
            item_action = action.desc.action
            self._update_commands_with_inventory_action(player_id, commands, item_id, item_action)

        for hero_command in commands:
            hero_command.execute()

    def on_mobs_turn(self):
        for mob in self.model.mobs:
            mob_command = mob.on_new_turn()
            mob_command.execute()

    def _update_commands_with_inventory_action(self, player_id, commands, item_id, item_action):
        character = self.get_player(player_id)
        if item_action == ItemAction.DROP:
            hero_command = DropItemCommand(self.model, player_id, item_id)
            commands.append(hero_command)
        elif item_action == ItemAction.USE:
            hero_command = UseItemCommand(self.model, player_id, item_id)
            commands.append(hero_command)
        self._update_commands_with_move_action(player_id, commands, character.position)

    def _update_commands_with_move_action(self, player_id, commands, position):
        character = self.get_player(player_id)
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

    def add_player(self, player_id):
        self.model.place_hero(player_id, self.game_config['hero'])

    def get_player(self, player_id):
        return self.model.players[player_id]
