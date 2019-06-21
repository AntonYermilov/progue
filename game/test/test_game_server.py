import subprocess
import time
import unittest

from game.client.controller.network import Network


class TestServer(unittest.TestCase):

    def setUp(self) -> None:
        self.server = subprocess.Popen(["python3", "-m", "game", "--server"])
        time.sleep(2)

    def test_game_creation(self):
        network = Network(addr='127.0.0.1', port=1488)
        self.assertTrue(network.create_game(False, False))

    def test_game_connect(self):
        network = Network(addr='127.0.0.1', port=1488)
        network.create_game(False, False)
        self.assertTrue(network.connect_to_game('cool_game'))

    def tearDown(self) -> None:
        self.server.kill()
