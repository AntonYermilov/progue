from game.server.controller.command import Command


class IdleCommand(Command):
    """
    Idle command: do nothing.
    """

    def execute(self):
        pass
