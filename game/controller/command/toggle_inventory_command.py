from game.controller.command import Command
from game.model import Model


class ToggleInventoryCommand(Command):

    def __init__(self, model: Model):
        self.model = model

    def execute(self):
        self.model.current_item = None if self.model.current_item else self.model.hero.get_item_if_any()
        print(f'set current item to {self.model.current_item}')
