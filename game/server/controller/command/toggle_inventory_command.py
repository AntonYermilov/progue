from game.server.controller.command import Command


class ToggleInventoryCommand(Command):

    def __init__(self, model):
        self.model = model

    def execute(self):
        self.model.current_item = None if self.model.current_item else self.model.hero.get_item_if_any()
