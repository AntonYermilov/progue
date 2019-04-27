import numpy as np

from game import Position, Direction
from game.model.entity.character.character import Character

from .strategy import Strategy


class CowardStrategy(Strategy):
    MOVES = [Direction.as_position(-1, 0),
             Direction.as_position(1, 0),
             Direction.as_position(0, 1),
             Direction.as_position(0, -1)]

    def _get_dist_to_hero(self, position) -> int:
        hero_position = self.model.get_hero().position
        return abs(position.get_row() - hero_position.get_row()) + \
               abs(position.get_col() - hero_position.get_col())

    def make_move(self, character: Character) -> Position:
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

            if self.model.get_hero().position == new_position:
                is_empty = False

            new_dist_to_hero = self._get_dist_to_hero(new_position)
            if is_empty and new_dist_to_hero > dist_to_hero:
                empty_cells.append(new_position)

        return np.random.choice(empty_cells) if len(empty_cells) != 0 else character.position
