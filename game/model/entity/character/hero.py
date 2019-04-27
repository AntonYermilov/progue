from .character import Character
from game import Position


class Hero(Character):
    """
    Hero is the character controlled by the player.
    """

    def __init__(self, position: Position):
        super().__init__(position)
