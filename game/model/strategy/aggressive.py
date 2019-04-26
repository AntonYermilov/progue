import numpy as np

from .strategy import Strategy
from game.model.character import Character
from game.model.position import Position, Direction


class AggressiveStrategy(Strategy):
    MOVES = [Direction.as_position(-1, 0),
             Direction.as_position(1, 0),
             Direction.as_position(0, 1),
             Direction.as_position(0, -1)]

    def make_move(self, character: Character) -> Position:
        empty_cells = []
        cell_with_hero = None
        for move in AggressiveStrategy.MOVES:
            new_position = character.position + move
            if self.model.get_labyrinth().is_wall(new_position):
                continue

            is_empty = True
            for mob in self.model.mobs:
                mob = mob[1]
                if mob.position == new_position:
                    is_empty = False
                    break

            if self.model.get_hero().position == new_position:
                cell_with_hero = new_position
                is_empty = False

            if is_empty:
                empty_cells.append(new_position)

        if cell_with_hero is not None:
            return cell_with_hero
        return np.random.choice(empty_cells) if len(empty_cells) != 0 else character.position
