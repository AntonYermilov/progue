from abc import ABC, abstractmethod
from game.model.character import Character
from game.model.position import Position


class Strategy(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def make_move(self, character: Character) -> Position:
        pass
