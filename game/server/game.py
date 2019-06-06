import os
import threading
from dataclasses import dataclass

from game.client.model.action import Action
from game.client.model.inventory import Inventory
from game.client.model.state import State
from game.model import Model
from game.server.controller.controller import Controller
from game.util import serialize_object, deserialize_object

SAVE_FILE_NAME = 'game_save.rsf'


@dataclass
class Player:
    id: str


class Game:
    """
    Game class - game management based on async events.
    """

    def __init__(self, player_id='player1'):
        self.players = [Player(id=player_id)]
        self.current_player = 0
        self.lock = threading.RLock()

        model = Model()
        model.generate_labyrinth(rows=19, columns=19, free_cells_ratio=0.3)

        self.controller = Controller(model)
        self.controller.start_game(player_id)

    def save_game(self):
        with self.lock:
            data = serialize_object(self.controller)
            with open(SAVE_FILE_NAME, 'wb') as save_file:
                save_file.write(data)

    def load_game(self):
        with self.lock:
            with open(SAVE_FILE_NAME, 'rb') as save_file:
                data = save_file.read()
                self.controller = deserialize_object(data)

    def delete_save(self):
        with self.lock:
            os.remove(SAVE_FILE_NAME)

    def get_state(self, player_id):
        with self.lock:
            hero = self.controller.model.players[player_id]
            players = []
            for p in self.players:
                 if p.id != player_id:
                    players.append(self.controller.get_player(p.id))
            state = State(my_turn=self.players[self.current_player].id == player_id,
                          hero=hero,
                          mobs=self.controller.model.mobs + players,
                          items=self.controller.model.items,
                          inventory=Inventory(capacity=hero.limit, items=hero.inventory),
                          labyrinth=self.controller.model.labyrinth)
            return state

    def on_connect(self):
        with self.lock:
            player = Player(id=f'player{len(self.players) + 1}')
            self.players.append(player)
            self.controller.add_player(player.id)
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
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0
                self.on_mobs_turn_()

    def on_mobs_turn_(self):
        with self.lock:
            self.controller.on_mobs_turn()
