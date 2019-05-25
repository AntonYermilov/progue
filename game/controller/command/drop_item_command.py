from game.controller.command import Command
from game.model import Model


class DropItemCommand(Command):

    def __init__(self, model: Model):
        self.model = model

    def execute(self):
        hero = self.model.hero
        item = self.model.current_item
        if item:
            idx = hero.inventory.index(item)
            if len(hero.inventory) == 1:
                self.model.current_item = None
            elif idx == len(hero.inventory) - 1:
                self.model.current_item = hero.inventory[idx - 1]
            else:
                self.model.current_item = hero.inventory[idx + 1]
            hero.remove_item(item)
            self.model.place_item(item, hero.position)
