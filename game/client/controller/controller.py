import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Union

from game import Position
from game.client.controller.menu import Menu
from game.client.model.action import Action, ActionType, MoveAction, InventoryAction, ItemAction
from game.client.model.model import Model
from game.client.view.user_command import UserCommand
from game.client.view.view import View


class Controller:
    FRAMES_PER_SECOND = 20
    GAME_CONFIG_PATH = Path('resources', 'config', 'game_config.json')
    ENTITIES_CONFIG_PATH = Path('resources', 'config', 'entities.json')
    LOG_DIR_PATH = Path('resources', 'logs')

    def __init__(self, *args, **kwargs):
        with self.GAME_CONFIG_PATH.open('r') as src:
            self.game_config = json.load(src)
        with self.ENTITIES_CONFIG_PATH.open('r') as src:
            self.entities_desc = json.load(src)
        self.model = Model()
        self.menu = None
        self.view = View(self, self.model, self.entities_desc)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self._create_log_handler()

    def _create_log_handler(self):
        if not Controller.LOG_DIR_PATH.exists():
            Controller.LOG_DIR_PATH.mkdir()

        current_date = datetime.now().strftime('%Y.%m.%d %H.%M.%S')
        log_name = 'client {}.txt'.format(current_date)
        log_file = Controller.LOG_DIR_PATH / log_name

        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    """
    Starts the game on the client side.
    Processes all user actions and interacts with server. 
    """
    def start_game(self):
        self.view.create()
        error = None

        self.logger.info('Game started')

        while True:
            self.logger.info('On new game stage')
            self.view.initialize()
            self.menu = Menu(self.view, error)
            error = None

            try:
                self.logger.info('On make_choice stage')
                network = self.menu.make_choice()
                if network is None:
                    self.logger.info('No network received, possible exit button was clicked')
                    break
                self.logger.info(f'Network was successfully created, singleplayer mode: {network.singleplayer}')

                if not network.singleplayer:
                    self.view.set_game_id(network.game_id)
                else:
                    self.view.set_game_id(None)

                self.logger.info('Starting game loop')
                while True:
                    self.logger.info('Receiving game state...')
                    state = network.get_state()
                    self.logger.info('Success')

                    self.model.update(state)
                    self.view.refresh_game()

                    if self.model.hero.stats.health == 0:
                        quit = False
                        while self.view.has_user_commands():
                            cmd = self.view.get_user_command()
                            if cmd == UserCommand.QUIT:
                                quit = True
                        if quit:
                            break
                    else:
                        self.view.clear_user_command_queue()
                        if state.my_turn:
                            action = self._get_user_action()
                            if action is None:
                                continue
                            network.send_action(action)
                            if action.type == ActionType.QUIT_ACTION:
                                break

                    self.view.delay(1.0 / self.FRAMES_PER_SECOND)
                self.logger.info('Game successfully finished')
            except Exception as e:
                error = 'Disconnected from server'
                self.logger.error('Disconnected from server')
                self.logger.exception(e)
            finally:
                self.menu.destroy()
        self.view.destroy()

    def _get_user_action(self) -> Union[Action, None]:
        while True:
            cmd = self.view.get_user_command()
            if cmd is UserCommand.UNKNOWN:
                return None
            if cmd in [UserCommand.UP, UserCommand.DOWN, UserCommand.LEFT, UserCommand.RIGHT, UserCommand.SKIP]:
                action = self._process_move(cmd)
                if action is not None:
                    return action
                continue
            if cmd == UserCommand.INVENTORY:
                action = self._process_inventory()
                if action is not None:
                    return action
                continue
            if cmd == UserCommand.QUIT:
                action = Action(type=ActionType.QUIT_ACTION, desc=None)
                return action
            # TODO add processing of other available commands

    def _process_move(self, cmd: UserCommand) -> Union[Action, None]:
        dr, dc = {UserCommand.UP:    (-1,  0),
                  UserCommand.DOWN:  (+1,  0),
                  UserCommand.LEFT:  ( 0, -1),
                  UserCommand.RIGHT: ( 0, +1),
                  UserCommand.SKIP:  ( 0,  0)}[cmd]
        hero_position = self.model.hero.position
        new_position = Position.as_position(hero_position.row + dr, hero_position.col + dc)
        if self.model.labyrinth.is_wall(new_position):
            return None
        return Action(type=ActionType.MOVE_ACTION,
                      desc=MoveAction(row=new_position.row, column=new_position.col))

    def _process_inventory(self) -> Union[Action, None]:
        inventory = self.model.inventory
        inventory.open()
        self.view.refresh_game()

        action = None
        while True:
            cmd = self.view.get_user_command()
            if cmd == UserCommand.INVENTORY:
                break
            if cmd == UserCommand.DOWN:
                inventory.select_next_item()
                self.view.refresh_game()
                continue
            if cmd == UserCommand.UP:
                inventory.select_previous_item()
                self.view.refresh_game()
                continue
            if inventory.no_item_selected():
                continue
            if cmd == UserCommand.USE:
                item_id = inventory.get_selected_item_position()
                action = Action(type=ActionType.INVENTORY_ACTION,
                                desc=InventoryAction(item_id=item_id, action=ItemAction.USE))
                break
            if cmd == UserCommand.DROP:
                item_id = inventory.get_selected_item_position()
                action = Action(type=ActionType.INVENTORY_ACTION,
                                desc=InventoryAction(item_id=item_id, action=ItemAction.DROP))
                break

        inventory.close()
        self.view.refresh_game()
        return action
