from concurrent import futures
import grpc

from .generated import progue_pb2_grpc, progue_pb2


class ProgueServer(progue_pb2_grpc.ProgueServerServicer):
    def GetState(self, request, context):
        return progue_pb2.State()

    def MakeTurn(self, request, context):
        if request.action_type == 1:
            pass

        return progue_pb2.MakeTurnResponse()

    def server_loop(self):
        pass


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
    server_object = ProgueServer()
    progue_pb2_grpc.add_ProgueServerServicer_to_server(server_object, server)
    server.add_insecure_port('[::]:51051')
    server.start()

