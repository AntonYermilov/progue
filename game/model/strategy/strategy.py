from abc import ABC, abstractmethod
from game.model.character import Character
from game.model.model import Model
from game.model.position import Position


class Strategy(ABC):
    def __init__(self, model: Model):
        self.model = model

    @abstractmethod
    def make_move(self, character: Character) -> Position:
        pass
