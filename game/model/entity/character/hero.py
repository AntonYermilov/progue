from game import Position
from game.model.entity.inventory.inventory_keeper import InventoryKeeper
from game.model.entity.item.item import Item
from .character import Character, CharacterStats


class Hero(Character, InventoryKeeper):
    """
    Hero is the character controlled by the player.
    """

    def __init__(self, position: Position, inventory_limit=15,
                 stats: CharacterStats = CharacterStats(attack_damage=5, max_health=50, health=50, experience=0)):
        Character.__init__(self, position=position, stats=stats)
        InventoryKeeper.__init__(self, limit=inventory_limit)

    def use_item(self, item: Item):
        item.apply(self)
        self.inventory.remove(item)

    def on_destroy(self, model):
        # print('Hero destroyed')
        pass

    def remove_item(self, item: Item):
        self.inventory.remove(item)

    def get_item_if_any(self):
        return self.inventory[0] if len(self.inventory) else None

    def get_prev_item_if_any(self, item: Item):
        idx = self.inventory.index(item)
        return self.inventory[idx - 1] if idx - 1 >= 0 else item

    def get_next_item_if_any(self, item: Item):
        idx = self.inventory.index(item)
        return self.inventory[idx + 1] if idx + 1 < len(self.inventory) else item
