from game import Position
from game.controller.command import Command
from game.model import Model
from game.model.entity.character import Hero
from game.model.entity.item.item import Item


class PickCommand(Command):

    def __init__(self, picker: Hero, target: Item, model: Model, new_position: Position):
        self.picker = picker
        self.target = target
        self.model = model
        self.new_position = new_position

    def execute(self):
        self.picker.pick_item(self.target)
        self.picker.move(self.new_position)
        self.model.remove_item(self.target)