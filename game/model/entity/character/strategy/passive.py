from game.server.controller.command import Command, IdleCommand
from game.model.entity.character.character import Character
from .strategy import Strategy


"""
Describes behaviour of mobs with passive strategy.
Passive mobs do nothing even in case player attacks them.
"""
class PassiveStrategy(Strategy):
    def on_new_turn(self, character: Character) -> Command:
        return IdleCommand()
