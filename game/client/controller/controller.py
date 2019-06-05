import json
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

    def __init__(self, *args, **kwargs):
        with self.GAME_CONFIG_PATH.open('r') as src:
            self.game_config = json.load(src)
        with self.ENTITIES_CONFIG_PATH.open('r') as src:
            self.entities_desc = json.load(src)
        self.model = Model()
        self.menu = None
        self.view = View(self, self.model, self.entities_desc)

    def start_game(self):
        self.view.initialize()

        while True:
            self.menu = Menu(self.view)
            try:
                network = self.menu.make_choice()
                if network is None:
                    break

                while True:
                    state = network.get_state()
                    self.model.update(state)
                    self.view.refresh_game()
                    if state.my_turn:
                        # TODO add start_turn call
                        action = self.get_user_action()
                        network.send_action(action)
                        if action.type == ActionType.QUIT_ACTION:
                            break
                        # TODO add finish_turn call

                    # TODO fix lugs when using delay command
                    # self.view.delay(1.0 / self.FRAMES_PER_SECOND)
            finally:
                self.menu.destroy()
        self.view.destroy()

    def get_user_action(self) -> Union[Action, None]:
        while True:
            cmd = self.view.get_user_command()
            if cmd in [UserCommand.UP, UserCommand.DOWN, UserCommand.LEFT, UserCommand.RIGHT]:
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
        dr, dc = {UserCommand.UP:    (-1, 0),
                  UserCommand.DOWN:  (+1, 0),
                  UserCommand.LEFT:  (0, -1),
                  UserCommand.RIGHT: (0, +1)}[cmd]
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
