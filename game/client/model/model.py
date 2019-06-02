from typing import List

from game.client.model.state import State


class Model:
    def __init__(self, *args, **kwargs):
        self.labyrinth = None
        self.hero = None
        self.mobs: List = None
        self.items: List = None

    def update(self, state: State):
        pass
