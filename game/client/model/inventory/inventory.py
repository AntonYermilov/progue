from dataclasses import dataclass
from typing import Union, List

from game.model.entity.item.item import Item


@dataclass
class Inventory:
    capacity: int
    items: List[Item]
    selected_item: Union[int, None]

    def __init__(self, capacity: int, items: List[Item] = None):
        self.capacity = capacity
        if items is None:
            self.items = []
        else:
            self.items = items
        self.selected_item = None

    def open(self) -> None:
        """
        Opens inventory and sets cursor to the default position (no item is selected)
        """
        self.selected_item = -1

    def is_opened(self) -> bool:
        """
        Returns true if inventory is already opened; false otherwise
        """
        return self.selected_item is not None

    def get_selected_item(self) -> Union[Item, None]:
        """
        Returns an item under a cursor, i.e. selected one
        """
        if self.selected_item is None or self.selected_item == -1:
            return None
        return self.items[self.selected_item]

    def get_selected_item_position(self) -> Union[int, None]:
        """
        Returns position of the selected item in the inventory
        """
        return self.selected_item

    def no_item_selected(self) -> bool:
        """
        Returns true if no item selected; false otherwise
        """
        return self.selected_item is None or self.selected_item == -1

    def select_next_item(self) -> int:
        """
        Moves cursor to the next item if exists; either sets cursor to the default position (no item is selected)
        :return: new position of cursor
        """
        if not self.is_opened():
            self.open()
        self.selected_item += 1
        if self.selected_item == len(self.items):
            self.selected_item = -1
        return self.selected_item

    def select_previous_item(self) -> int:
        """
        Moves cursor to the previous item if exists; either sets cursor to the default position (no item is selected)
        :return: new position of cursor
        """
        if not self.is_opened():
            self.open()
        self.selected_item -= 1
        if self.selected_item < -1:
            self.selected_item = len(self.items) - 1
        return self.selected_item

    def remove_item(self, item: Item) -> Union[Item, None]:
        """
        Removes specified item from the inventory. Returns removed item.
        """
        try:
            self.items.remove(item)
        except ValueError:
            return None
        return item

    def remove_item_by_position(self, position: int) -> Union[Item, None]:
        """
        Removes item from the inventory by its position in it. Returns removed item.
        """
        if 0 <= position < len(self.items):
            return self.remove_item(self.items[position])
        return None

    def add_item(self, item: Item) -> bool:
        """
        Adds an item to the inventory. Returns true if succeeded; false otherwise.
        """
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

    def size(self):
        """
        Returns size of the inventory, i.e. number of items in it
        """
        return len(self.items)

    def close(self) -> None:
        """
        Closes inventory
        """
        self.selected_item = None
