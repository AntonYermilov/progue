from typing import Union

import numpy as np

from game import Position, MOVES
from game.model.entity.character import Character
from game.server.controller.command import Command, AttackCommand, MoveCommand, IdleCommand
from .strategy import Strategy


"""
Describes behaviour of mobs with confused strategy.
This strategy is a decorator strategy for mobs that were confused.
Those mobs move randomly within a specified number of turns.
"""
class ConfusedStrategy(Strategy):
    def __init__(self, turns: int, character: Character):
        super().__init__(character.strategy.model)
        self.turns = turns
        self.character = character
        self.previous_strategy = character.strategy
        if isinstance(self.previous_strategy, ConfusedStrategy):
            self.previous_strategy = self.previous_strategy.previous_strategy

    def _get_random_move(self, character: Character) -> Union[Position, None]:
        available_moves = []
        for move in MOVES:
            position = character.position + move
            if self.model.get_labyrinth().is_wall(position):
                continue
            if any(mob.position == position for mob in self.model.mobs):
                continue
            available_moves.append(move)

        if len(available_moves) > 0:
            new_position = character.position + np.random.choice(available_moves)
            return new_position
        return None

    def _process_tick(self):
        self.turns -= 1
        if self.turns == 0:
            self.character.strategy = self.previous_strategy

    def on_new_turn(self, character: Character) -> Command:
        self._process_tick()
        new_position = self._get_random_move(character)
        if new_position is None:
            return IdleCommand()

        for hero in self.model.players.values():
            if new_position == hero.position:
                return AttackCommand(character, hero, self.model)
        return MoveCommand(character, new_position)
