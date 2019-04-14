from game.controller.command import Command


class IdleCommand(Command):
    """
    Idle command: do nothing.
    """

    def execute(self):
        self.emit_message("I'll just stay here for now.")
