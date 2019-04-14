from abc import ABC, abstractmethod

from game.controller.status_manager import StatusManager


class Command(ABC):
    """
    Command base class.

    Implementation of command pattern for player actions.
    """

    def __init__(self, status_manager: StatusManager):
        self.status_manager = status_manager

    @abstractmethod
    def execute(self, ):
        """
        Executes this command.
        """
        pass

    def emit_message(self, message):
        self.status_manager.register_message(message)
