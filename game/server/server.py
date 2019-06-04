import threading
from concurrent import futures

import grpc

from .game import Game
from .generated import progue_pb2_grpc, progue_pb2
from game.client.model.action import *


class ProgueServer(progue_pb2_grpc.ProgueServerServicer):

    def __init__(self):
        super().__init__()
        self.games = dict()
        self.lock = threading.RLock()

    def GetState(self, request, context):
        # TODO
        with self.lock:
            return progue_pb2.State()

    def MakeTurn(self, request, context):
        if request.action.action_type is ActionType.MOVE_ACTION:
            action_desc = MoveAction(row=request.action.move_action.row,
                                     column=request.action.move_action.col)
        elif request.action_type is ActionType.INVENTORY_ACTION:
            action_desc = InventoryAction(item_id=request.action.inventory_action.item_id,
                                          action=request.action.inventory_action.action_type)
        else:
            print('Error: unknown action type')
            return None

        action = Action(type=request.action.action_type, desc=action_desc)
        player_id = request.player.id

        with self.lock:
            game = self.games[request.game_id.id]

        if game is None:
            return None

        game.on_make_turn(player_id, action)

        return progue_pb2.MakeTurnResponse()

    def ListGames(self, request, context):
        response = progue_pb2.ListGamesResponse()
        with self.lock:
            for game_id in self.games:
                response.game_ids.append(progue_pb2.GameId(id=game_id))
        return response

    def ConnectToGame(self, request, context):
        game_id = request.id
        with self.lock:
            if game_id in self.games:
                game = self.games[game_id]
                player_id = game.on_connect()
                return progue_pb2.ConnectToGameResponse(successfully_connected=True,
                                                        player=progue_pb2.Player(id=player_id))
            else:
                return progue_pb2.ConnectToGameResponse(successfully_connected=False)

    def CreateGame(self, request, context):
        game_id = request.id
        with self.lock:
            if game_id not in self.games:
                self.games[game_id] = Game()
                return progue_pb2.CreateGameResponse(successfully_created=True,
                                                     player=progue_pb2.Player(id='player1'))
            else:
                return progue_pb2.CreateGameResponse(successfully_created=False)


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
    server_object = ProgueServer()
    progue_pb2_grpc.add_ProgueServerServicer_to_server(server_object, server)
    server.add_insecure_port('[::]:51051')
    server.start()
