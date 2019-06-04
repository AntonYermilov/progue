import numpy as np

from game import Direction
from game.server.controller.command import Command, MoveCommand, IdleCommand
from game.model.entity.character.character import Character
from .strategy import Strategy


class CowardStrategy(Strategy):
    MOVES = [Direction.as_position(-1, 0),
             Direction.as_position(1, 0),
             Direction.as_position(0, 1),
             Direction.as_position(0, -1)]

    def _get_dist_to_hero(self, position) -> int:
        min_dist = float('inf')
        for hero in self.model.players.values():
            delta = hero.position - position
            dist_row_, dist_col_ = delta.get_row(), delta.get_col()
            dist = abs(dist_row_) + abs(dist_col_)
            if dist < min_dist:
                min_dist = dist

        return min_dist

    def on_new_turn(self, character: Character) -> Command:
        empty_cells = []

        dist_to_hero = self._get_dist_to_hero(character.position)
        for move in CowardStrategy.MOVES:
            new_position = character.position + move
            if self.model.get_labyrinth().is_wall(new_position):
                continue

            is_empty = True
            for mob in self.model.mobs:
                if mob.position == new_position:
                    is_empty = False
                    break

            for hero in self.model.players.values():
                if hero.position == new_position:
                    is_empty = False
                    break

            new_dist_to_hero = self._get_dist_to_hero(new_position)
            if is_empty and new_dist_to_hero > dist_to_hero:
                empty_cells.append(new_position)

        if len(empty_cells) != 0:
            return MoveCommand(character, np.random.choice(empty_cells))
        else:
            return IdleCommand()
