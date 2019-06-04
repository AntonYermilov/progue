from game.client.model.action import Action
from game.client.model.inventory import Inventory
from game.client.model.state import State


class Network:
    """
    Dummy network
    """
    def __init__(self, controller, *args, **kwargs):
        self.controller = controller

    def connect(self, *args, **kwargs):
        pass

    def get_state(self, *args, **kwargs):
        hero = self.controller.model.hero
        state = State(my_turn=True,
                      hero=self.controller.model.hero,
                      mobs=self.controller.model.mobs,
                      items=self.controller.model.items,
                      inventory=Inventory(capacity=hero.limit, items=hero.inventory),
                      labyrinth=self.controller.model.labyrinth)
        return state

    def send_action(self, action: Action, *args, **kwargs):
        self.controller.process_input(action)