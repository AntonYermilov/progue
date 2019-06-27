from game import Position
from game.server.controller.command import Command


class PickCommand(Command):

    def __init__(self, picker, target, model, new_position: Position):
        self.picker = picker
        self.target = target
        self.model = model
        self.new_position = new_position

    def execute(self):
        self.picker.pick_item(self.target)
        self.picker.move(self.new_position)
        self.model.remove_item(self.target)