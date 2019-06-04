import grpc

from game.client.model.action import Action, ActionType
from game.server.generated import progue_pb2_grpc, progue_pb2


class Network:
    """
    Dummy network
    """

    def __init__(self, *args, **kwargs):
        self.controller = None
        self.stub = None
        self.game_id = None
        self.player_id = None

    def connect(self, *args, **kwargs):
        channel = grpc.insecure_channel('localhost:51051')
        self.stub = progue_pb2_grpc.ProgueServerStub(channel)

    def get_state(self, *args, **kwargs):
        # hero = self.controller.model.hero
        # state = State(my_turn=True,
        #               hero=self.controller.model.hero,
        #               mobs=self.controller.model.mobs,
        #               items=self.controller.model.items,
        #               inventory=Inventory(capacity=hero.limit, items=hero.inventory),
        #               labyrinth=self.controller.model.labyrinth)

        # TODO state
        return None

    def send_action(self, action: Action, *args, **kwargs):
        progue_pb2.MakeTurnRequest()
        game_id = progue_pb2.GameId(id=self.game_id)
        player = progue_pb2.Player(id=self.player_id)
        if action.type is ActionType.MOVE_ACTION:
            action_type = 0
            action_ = progue_pb2.Action.MoveAction(row=action.desc.row, col=action.desc.column)
        elif action.type is ActionType.INVENTORY_ACTION:
            action_type = 1
            action_ = progue_pb2.Action.InventoryAction(item_id=action.desc.item_id, action_type=action.desc.action)
        elif action.type is ActionType.QUIT_ACTION:
            return
        else:
            return
        action_msg = progue_pb2.Action(action_type=action_type, action=action_)
        make_turn_msg = progue_pb2.MakeTurnRequest(game_id=game_id, player=player, action=action_msg)
        self.stub.MakeTurn(make_turn_msg)
