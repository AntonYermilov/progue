from game.controller.command import Command
from game.model import Model


class UseItemCommand(Command):
    def __init__(self, model: Model, item_id: int):
        self.model = model
        self.item_id = item_id

    def execute(self):
        hero = self.model.hero
        if self.item_id is not None and 0 <= self.item_id < len(hero.inventory):
            item = hero.inventory[self.item_id]
            item.apply(hero)
            hero.remove_item(item)
