import threading
from dataclasses import dataclass

from game.client.model.action import Action
from game.model import Model
from game.server.controller import Controller


@dataclass
class Player:
    id: str


class Game:
    """
    Game class - game management based on async events.
    """

    def __init__(self):
        self.players = [Player(id='player1')]
        self.current_player = 0
        self.lock = threading.RLock()

        model = Model()
        model.generate_labyrinth(rows=19, columns=19, free_cells_ratio=0.3)

        self.controller = Controller(model)

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
            self.on_turn_end_()

    def on_turn_end_(self):
        with self.lock:
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0
                self.on_mobs_turn_()

    def on_mobs_turn_(self):
        with self.lock:
            self.controller.on_mobs_turn()
