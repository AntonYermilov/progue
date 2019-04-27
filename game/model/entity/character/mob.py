from typing import Dict

from game import Position
from game.model.entity.character.character import Character
from game.model.entity.character.strategy import strategies
from game.model.entity.character.strategy.strategy import Strategy


class Mob(Character):
    """
    Mob, the enemy to the player.
    """

    def __init__(self, position: Position, name: str, strategy: Strategy):
        super().__init__(position)
        self.name = name
        self.strategy = strategy

    def get_move(self) -> Position:
        return self.strategy.make_move(self)


class MobFactory:
    def __init__(self, model):
        self.model = model

    def generate_mob(self, position: Position, name: str, description: Dict):
        strategy = strategies[description['strategy']]
        return Mob(position, name, strategy(self.model))
