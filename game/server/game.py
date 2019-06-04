from attr import dataclass
import threading


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

    def on_connect(self):
        with self.lock:
            player = Player(id=f'player{len(self.players) + 1}')
            self.players.append(player)
            return player.id

    def on_make_turn(self, player_id, action):
        with self.lock:
            if self.players[self.current_player].id == player_id:
                self.on_action_(self.players[self.current_player], action)
                self.on_turn_end_()

    def on_action_(self, player, action):
        # TODO command
        with self.lock:
            pass

    def on_turn_end_(self):
        with self.lock:
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0
                self.on_mobs_turn_()

    def on_mobs_turn_(self):
        # TODO
        with self.lock:
            pass
