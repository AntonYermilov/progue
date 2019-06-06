import threading
import time
from concurrent import futures

import grpc

from game.client.model.action import *
from game.util import serialize_object
from .generated import progue_pb2_grpc, progue_pb2


class ProgueServer(progue_pb2_grpc.ProgueServerServicer):

    def __init__(self):
        super().__init__()
        self.games = dict()
        self.lock = threading.RLock()
        self.received = False

    def GameSaveManage(self, request, context):
        with self.lock:
            game = self.games[0]
        if request.type == 0:
            game.save_game()
        elif request.type == 1:
            game.load_game()
        elif request.type == 2:
            game.delete_save()

        return progue_pb2.GameSaveResponse()

    def GetState(self, request, context):
        with self.lock:
            game = self.games[request.game_id.id]

            state = game.get_state(request.player.id)
            return progue_pb2.State(state=serialize_object(state))

    def MakeTurn(self, request, context):
        self.received = True

        if request.action.action_type is 0:
            action_type = ActionType.MOVE_ACTION
            action_desc = MoveAction(row=request.action.move_action.row,
                                     column=request.action.move_action.col)
        elif request.action.action_type is 1:
            action_type = ActionType.INVENTORY_ACTION
            action_desc = InventoryAction(item_id=request.action.inventory_action.item_id,
                                          action=request.action.inventory_action.action_type)
        elif request.action.action_type is 2:
            self.quit(request.game_id.id, request.player.id)
            return progue_pb2.MakeTurnResponse()
        else:
            print('Error: unknown action type')
            return None

        action = Action(type=action_type, desc=action_desc)
        player_id = request.player.id

        with self.lock:
            game = self.games[request.game_id.id]

        if game is None:
            return None

        try:
            game.on_make_turn(player_id, action)
        except Exception as e:
            print(e)

        return progue_pb2.MakeTurnResponse()

    def quit(self, game_id, player_id):
        with self.lock:
            game = self.games[game_id]

            if game.player_quit(player_id):
                del self.games[game_id]

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
        from .game import Game
        game_id = request.id
        with self.lock:
            if game_id not in self.games:

                self.games[game_id] = Game()
                player = progue_pb2.Player(id='player1')
                response = progue_pb2.CreateGameResponse(successfully_created=True,
                                                         player=player)
                return response
            else:
                return progue_pb2.CreateGameResponse(successfully_created=False)


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=(('grpc.so_reuseport', 0),))
    progue_pb2_grpc.add_ProgueServerServicer_to_server(ProgueServer(), server)
    result = server.add_insecure_port('0.0.0.0:1488')
    server.start()
    print(f'Serving on {result}')
    try:
        while True:
            time.sleep(20000)
    except KeyboardInterrupt:
        print('Keyboard interrupt, shutting server down.')
    finally:
        server.stop(0)
