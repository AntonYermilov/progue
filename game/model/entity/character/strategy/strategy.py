from abc import ABC, abstractmethod
from game.server.controller.command import Command
from game.model.entity.character.character import Character


"""
Base strategy class
"""
class Strategy(ABC):
    def __init__(self, model):
        self.model = model

    """
    Determines the move of the specified character on the new turn.
    Returns the character action as a command.
    """
    @abstractmethod
    def on_new_turn(self, character: Character) -> Command:
        pass
