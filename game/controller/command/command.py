from abc import ABC, abstractmethod


class Command(ABC):
    """
    Command base class.

    Implementation of command pattern for player actions.
    """

    @abstractmethod
    def execute(self, ):
        """
        Executes this command.
        """
        pass
