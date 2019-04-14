from game.controller.status_manager import StatusManager
from game.controller.user_input_processor import UserInputProcessor, UserInput
from game.model import Model


class Controller:
    """
    Controller of MVC architecture.
    """

    def __init__(self, model: Model):
        """
        Initialises controller with given model.

        :param model: Model
            A model to work with
        """
        self.model = model
        self.status_manager = StatusManager()
        self.input_processor = UserInputProcessor(status_manager=self.status_manager, model=self.model)

    def start_game(self, view):
        """
        Starts the game loop.

        :param view: View
            View to work with
        """
        view.start(controller=self)

    def process_input(self, user_input: UserInput):
        """
        Processes user input.
        """
        command = self.input_processor.process_input(user_input)
        command.execute()
