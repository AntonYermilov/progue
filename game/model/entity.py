from abc import ABC


class Entity(ABC):
    def __init__(self, position):
        self.position = position
        self.symbol = '.'
