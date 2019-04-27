from game import Position
from .character import Character, CharacterStats


class Hero(Character):
    """
    Hero is the character controlled by the player.
    """

    def on_destroy(self, model):
        print('Hero destroyed')

    def __init__(self, position: Position,
                 stats: CharacterStats = CharacterStats(attack_damage=5, max_health=50, health=50)):
        super().__init__(position, stats)
