import subprocess
import time
import unittest

from game.client.controller.network import Network
from game.client.model.action import Action, ActionType, MoveAction


class TestClientServerInteraction(unittest.TestCase):

    def setUp(self) -> None:
        self.server = subprocess.Popen(["python3", "-m", "game", "--server"])
        time.sleep(2)

        network = Network(addr='127.0.0.1', port=1488)
        self.assertTrue(network.create_game(False, False))
        self.network = network

    def test_action(self):
        self.network.send_action(Action(ActionType.MOVE_ACTION, desc=MoveAction(row=42, column=42)))
        state = self.network.get_state()
        hero = state.hero
        self.assertEquals(42, hero.position.get_row())
        self.assertEquals(42, hero.position.get_col())

    def test_initial_state(self):
        state = self.network.get_state()
        self.assertTrue(state.my_turn)
        self.assertIsNotNone(state.hero)
        self.assertTrue(len(state.mobs) > 0)
        self.assertIsNotNone(state.labyrinth)

    def tearDown(self) -> None:
        self.network.send_action(Action(type=ActionType.QUIT_ACTION, desc=None))
        self.server.kill()
