from abc import ABC, abstractmethod
from game import Position
from game.controller.command import Command
from game.model.entity.character.character import Character


class Strategy(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def make_move(self, character: Character) -> Position:
        pass

    @abstractmethod
    def on_new_turn(self, character: Character) -> Command:
        pass
