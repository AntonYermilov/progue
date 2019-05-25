from abc import ABC, abstractmethod

from game.model.entity.item.item import Item


class InventoryKeeper(ABC):
    """
        Enables ability to keep items.
    """
    def __init__(self, limit):
        self.inventory = []
        self.limit = limit

    def pick_item(self, item: Item):
        """
        Try to add an item to inventory.
        :param item: item
        """
        if len(self.inventory) + 1 <= self.limit:
            self.inventory.append(item)

    @abstractmethod
    def use_item(self, item: Item):
        """
        Try to add an item to inventory.
        :param item: item
        """
        pass
