import grpc

from game.client.model.action import Action, ActionType
from game.server.generated import progue_pb2_grpc, progue_pb2
from game.util import deserialize_object


"""
This class describes the interaction with the server
"""
class Network:
    def __init__(self, addr, port):
        self.stub = None
        self.game_id = None
        self.player_id = None
        self.addr = f'{addr}:{port}'
        self.singleplayer = None

    """
    Sends request to the server.
    Receives the list of available multiplayer games.
    """
    def list_games(self):
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.list_games(progue_pb2.ListGamesRequest())
            return list(map(lambda x: x.id, response.game_ids))

    """
    Sends request to the server. 
    Tries to connect to the specified game. Returns true if succeeded. 
    """
    def connect_to_game(self, game_id: str):
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.connect_to_game(progue_pb2.GameId(id=game_id))
            if response.successfully_connected:
                self.player_id = response.player.id
                self.game_id = game_id
                self.singleplayer = False
                return True
        return False

    """
    Sends request to the server. 
    Creates new game. Returns true if succeeded.
    """
    def create_game(self, singleplayer: bool, load: bool):
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.create_game(progue_pb2.CreateGameRequest(singleplayer=singleplayer, load=load))
            if response.successfully_created:
                self.player_id = response.player.id
                self.game_id = response.id
                self.singleplayer = singleplayer
                return True
        return False

    """
    Sends request to the server.
    Receives relevant state (description) of the game model
    """
    def get_state(self):
        request = progue_pb2.StateRequest(game_id=progue_pb2.GameId(id=self.game_id),
                                          player=progue_pb2.Player(id=self.player_id))
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            response = stub.get_state(request)
        state = deserialize_object(response.state)

        return state

    """
    Sends information about user action to the server.
    """
    def send_action(self, action: Action):
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
            action_type = 2
            action_msg = progue_pb2.Action(action_type=action_type)
        else:
            return

        make_turn_msg = progue_pb2.MakeTurnRequest(game_id=game_id, player=player, action=action_msg)
        with grpc.insecure_channel(self.addr) as channel:
            stub = progue_pb2_grpc.ProgueServerStub(channel)
            stub.make_turn(make_turn_msg)
