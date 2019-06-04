import grpc

from game.client.model.action import Action, ActionType
from game.server.generated import progue_pb2_grpc, progue_pb2
from game.util import deserialize_object


class Network:
    """
    Dummy network
    """

    def __init__(self):
        self.stub = None
        self.game_id = None
        self.player_id = None
        self.addr = '127.0.0.1:1488'

    def connect(self, *args, **kwargs):
        pass

    def list_games(self):
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.ListGames(progue_pb2.ListGamesRequest())
            return list(map(lambda x: x.id, response.game_ids))

    def connect_to_game(self, game_id: str):
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.ConnectToGame(progue_pb2.GameId(id=game_id))
            if response.successfully_connected:
                self.player_id = response.player.id
                self.game_id = game_id
                return True
        return False

    def create_game(self, game_id: str):
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.CreateGame(progue_pb2.GameId(id=game_id))
            if response.successfully_created:
                self.player_id = response.player.id
                self.game_id = game_id
            else:
                raise RuntimeError()

    def get_state(self):
        request = progue_pb2.StateRequest(game_id=progue_pb2.GameId(id=self.game_id),
                                          player=progue_pb2.Player(id=self.player_id))
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.GetState(request)
        state = deserialize_object(response.state)

        return state

    def send_action(self, action: Action):
        progue_pb2.MakeTurnRequest()
        game_id = progue_pb2.GameId(id=self.game_id)
        player = progue_pb2.Player(id=self.player_id)
        if action.type is ActionType.MOVE_ACTION:
            action_type = 0
            action_ = progue_pb2.Action.MoveAction(row=action.desc.row, col=action.desc.column)
            action_msg = progue_pb2.Action(action_type=action_type, move_action=action_)
        elif action.type is ActionType.INVENTORY_ACTION:
            action_type = 1
            action_ = progue_pb2.Action.InventoryAction(item_id=action.desc.item_id, action_type=action.desc.action)
            action_msg = progue_pb2.Action(action_type=action_type, inventory_action=action_)
        elif action.type is ActionType.QUIT_ACTION:
            return
        else:
            return

        make_turn_msg = progue_pb2.MakeTurnRequest(game_id=game_id, player=player, action=action_msg)
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            stub.MakeTurn(make_turn_msg)
