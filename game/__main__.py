import logging
import sys

import game.client.controller.controller as cli
from game.server import start_server
from game.test import run_tests


def setup_logging():
    logging.basicConfig(filename='progue.log', level=logging.DEBUG)


def main():
    setup_logging()
    logging.info('Initialised')

    if len(sys.argv) > 1:
        port = '1488'
        if sys.argv[1] == '--server':
            if len(sys.argv) > 2 and sys.argv[2].isdigit():
                port = sys.argv[2]
            start_server(port)
        elif sys.argv[1] == '--test':
            run_tests()
    else:
        cli_controller = cli.Controller()
        cli_controller.start_game()


if __name__ == "__main__":
    main()
