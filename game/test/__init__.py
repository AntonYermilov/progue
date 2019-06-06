import unittest

from game.test.test_game_server import TestServer


def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestServer("test_game_creation"))
    suite.addTest(TestServer("test_game_connect"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
