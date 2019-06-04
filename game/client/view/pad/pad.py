from abc import ABC, abstractmethod


class Pad(ABC):
    def __init__(self, view, x0: int, y0: int, x1: int, y1: int):
        """
        Creates pad with corners in specified coordinates
        :param view: base view instance
        :param x0: x-coordinate of top left corner (included)
        :param y0: y-coordinate of top left corner (included)
        :param x1: x-coordinate of bottom right corner (excluded)
        :param y1: y-coordinate of bottom right corner (excluded)
        """
        self.view = view
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    @abstractmethod
    def refresh(self):
        pass