import unittest

from game.test.test_client_server_interaction import TestClientServerInteraction
from game.test.test_game_server import TestServer


def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestServer("test_game_creation"))
    suite.addTest(TestServer("test_game_connect"))

    suite.addTest(TestClientServerInteraction("test_initial_state"))
    suite.addTest(TestClientServerInteraction("test_action"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
