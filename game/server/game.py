import threading
from dataclasses import dataclass

import numpy as np

from game import SAVE_FILE_NAME
from game.client.model.action import Action
from game.client.model.inventory import Inventory
from game.client.model.state import State
from game.model import Model
from game.server.controller.controller import Controller
from game.util import serialize_object, deserialize_object


@dataclass
class Player:
    id: str


class Game:
    """
    Game class - game management based on async events.
    """

    def __init__(self, load=False, singleplayer=False):
        self.players = []
        self.current_player = None
        self.lock = threading.RLock()
        self.singleplayer = singleplayer

        if singleplayer and not load:
            self.delete_save()

        self.load = load
        if not load:
            model = Model()
            model.generate_labyrinth(rows=19, columns=19, free_cells_ratio=0.3)

            self.controller = Controller(model)
            self.controller.start_game()
        else:
            with SAVE_FILE_NAME.open('rb') as save_file:
                data = save_file.read()
                self.controller = deserialize_object(data)

    def player_quit(self, player_id):
        with self.lock:
            if self.singleplayer:
                self.save_game()
                return True

            del self.controller.model.players[player_id]
            self.on_turn_end_()
            return all(self.controller.get_player(p.id) is None for p in self.players)

    def save_game(self):
        with self.lock:
            data = serialize_object(self.controller)
            if not SAVE_FILE_NAME.parent.exists():
                SAVE_FILE_NAME.parent.mkdir(parents=True)
            with SAVE_FILE_NAME.open('wb') as save_file:
                save_file.write(data)

    def delete_save(self):
        with self.lock:
            if SAVE_FILE_NAME.exists():
                SAVE_FILE_NAME.unlink()

    def get_state(self, player_id):
        with self.lock:
            hero = self.controller.get_player(player_id)
            players = []

            # remove players that were killed on last turn
            for p in self.players:
                if p.id != player_id and self.controller.get_player(p.id) is not None:
                    players.append(self.controller.get_player(p.id))
            my_turn = self.current_player is not None and self.players[self.current_player].id == player_id
            state = State(my_turn=my_turn,
                          hero=hero,
                          mobs=self.controller.model.mobs + players,
                          items=self.controller.model.items,
                          inventory=Inventory(capacity=hero.limit, items=hero.inventory) if hero is not None else None,
                          labyrinth=self.controller.model.labyrinth)
            return state

    def on_connect(self):
        with self.lock:
            if self.singleplayer and self.load:
                player_id = None
                for pid in self.controller.model.players.keys():
                    player_id = pid
            else:
                player_id = str(np.random.randint(1 << 30))
                self.controller.add_player(player_id)
            player = Player(id=player_id)
            self.players.append(player)
            if self.current_player is None:
                self.current_player = 0
            return player.id

    def on_make_turn(self, player_id, action):
        with self.lock:
            if self.players[self.current_player].id == player_id:
                self.on_action_(self.players[self.current_player], action)
                self.on_turn_end_()

    def on_action_(self, player, action: Action):
        with self.lock:
            self.controller.on_action(player.id, action)

    def on_turn_end_(self):
        with self.lock:
            while True:
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0
                    break
                if self.controller.get_player(self.players[self.current_player].id) is not None:
                    break

            if self.current_player == 0:
                self.on_mobs_turn_()
                with self.lock:
                    for i, p in enumerate(self.players):
                        if self.controller.get_player(p.id) is None:
                            del self.players[i]

            if self.current_player == len(self.players):
                if self.singleplayer:
                    self.delete_save()
                self.current_player = None
            elif self.singleplayer:
                self.save_game()

    def on_mobs_turn_(self):
        with self.lock:
            self.controller.on_mobs_turn()
