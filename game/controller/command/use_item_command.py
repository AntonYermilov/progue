from game.controller.command import Command
from game.model import Model


class UseItemCommand(Command):
    def __init__(self, model: Model):
        self.model = model

    def execute(self):
        hero = self.model.hero
        self.model.current_item.apply(hero)
        hero.remove_item(self.model.current_item)
        self.model.current_item = hero.get_item_if_any()

