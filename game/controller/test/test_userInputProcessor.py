from unittest import TestCase

from game.controller import StatusManager
from game.controller.move_command import MoveCommand
from game.controller.user_input_processor import UserInputProcessor, UserInput
from game.elements import Artifact, Character, Object
from game.model import Model


class TestUserInputProcessor(TestCase):
    def test_process_input(self):
        status_manager = StatusManager()
        model = Model()
        model.generate_labyrinth(base_side_length=7, min_labyrinth_size=190)
        model.place_entities({Artifact.GOLD: 10,
                              Character.GHOST: 5,
                              Character.SNAKE: 5,
                              Artifact.HEALING_POTION: 5,
                              Artifact.KNOWLEDGE_SCROLL: 5,
                              Character.HERO: 1,
                              Object.EXIT: 1})

        input_processor = UserInputProcessor(model=model, status_manager=status_manager)

        command = input_processor.process_input(UserInput.LEFT)

        assert type(command) is MoveCommand
