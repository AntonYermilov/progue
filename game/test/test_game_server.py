import multiprocessing
import time
import unittest

from game.client.controller.network import Network
from game.server import start_server


class TestServer(unittest.TestCase):

    def setUp(self) -> None:
        self.interrupted = [False]
        t = multiprocessing.Process(target=start_server, args=[self.interrupted])
        t.start()

    def test_game_creation(self):
        network = Network()
        self.assertTrue(network.create_game('cool_game'))

    def tearDown(self) -> None:
        self.interrupted[0] = True
        time.sleep(3)
