from typing import Union

import numpy as np

from game import Position, Direction
from game.controller.command import Command, AttackCommand, MoveCommand, IdleCommand
from game.model.entity.character import Character
from .strategy import Strategy


class AggressiveStrategy(Strategy):
    MOVES = [Direction.as_position(-1, 0),
             Direction.as_position(1, 0),
             Direction.as_position(0, 1),
             Direction.as_position(0, -1)]

    def get_move_to_hero(self, character: Character) -> Union[Position, None]:
        hero_position = self.model.get_hero().position
        if any(character.position + move == hero_position for move in AggressiveStrategy.MOVES):
            return hero_position

        delta = self.model.hero.position - character.position
        dist_row, dist_col = delta.get_row(), delta.get_col()

        first_move = None
        while dist_row != 0 or dist_col != 0:
            dir_row = Direction.as_position(0 if dist_row == 0 else dist_row // abs(dist_row), 0)
            dir_col = Direction.as_position(0, 0 if dist_col == 0 else dist_col // abs(dist_col))
            if dist_row != 0 and dist_col != 0:
                move = np.random.choice([dir_row, dir_col])
            else:
                move = dir_row if dist_row != 0 else dir_col

            new_position = character.position + move
            if first_move is None:
                first_move = new_position

            if self.model.labyrinth.is_wall(new_position):
                return None

            dist_row -= move.row
            dist_col -= move.col

        if any(mob.position == first_move for mob in self.model.mobs):
            return None
        return first_move

    def get_random_move(self, character: Character) -> Union[Position, None]:
        empty_cells = []
        for move in AggressiveStrategy.MOVES:
            position = character.position + move
            if self.model.get_labyrinth().is_wall(position):
                continue
            if any(mob.position == position for mob in self.model.mobs):
                continue
            empty_cells.append(position)
        return np.random.choice(empty_cells) if len(empty_cells) > 0 else None

    def on_new_turn(self, character: Character) -> Command:
        new_position = self.get_move_to_hero(character)
        if new_position is None:
            new_position = self.get_random_move(character)

        if new_position is None:
            return IdleCommand()
        if new_position == self.model.get_hero().position:
            return AttackCommand(character, self.model.get_hero(), self.model)
        return MoveCommand(character, new_position)

