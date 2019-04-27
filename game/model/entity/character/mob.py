from typing import Dict

from game import Position
from game.controller.command import Command
from game.model.entity.character.character import Character, CharacterStats
from game.model.entity.character.strategy import strategies
from game.model.entity.character.strategy.strategy import Strategy


class Mob(Character):
    """
    Mob, the enemy to the player.
    """

    def __init__(self, position: Position, name: str, strategy: Strategy, stats: CharacterStats):
        super().__init__(position, stats)
        self.name = name
        self.strategy = strategy

    def get_move(self) -> Position:
        return self.strategy.make_move(self)

    def on_new_turn(self) -> Command:
        return self.strategy.on_new_turn(self)

    def on_destroy(self, model):
        lst = model.mobs

        idx = 0
        while idx < len(lst):
            if lst[idx] is self:
                del lst[idx]
            else:
                idx = idx + 1


class MobFactory:
    def __init__(self, model):
        self.model = model

    def generate_mob(self, position: Position, name: str, description: Dict):
        strategy = strategies[description['strategy']]
        stats = CharacterStats(attack_damage=5, max_health=20, health=20)
        return Mob(position, name, strategy(self.model), stats)
