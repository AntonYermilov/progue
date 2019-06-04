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

    def on_make_turn(self, player, action):
        with self.lock:
            if self.players[self.current_player].id == player.id:
                self.on_action(player, action)

    def on_action(self, player, action):
        # TODO
        pass