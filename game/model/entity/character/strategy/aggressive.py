import numpy as np

from game import Position, Direction
from game.controller.command import Command, AttackCommand, MoveCommand, IdleCommand
from game.model.entity.character import Character
from .strategy import Strategy


class AggressiveStrategy(Strategy):
    def on_new_turn(self, character: Character) -> Command:
        empty_cells = []
        cell_with_hero = None
        for move in AggressiveStrategy.MOVES:
            new_position = character.position + move
            if self.model.get_labyrinth().is_wall(new_position):
                continue

            is_empty = True
            for mob in self.model.mobs:
                if mob.position == new_position:
                    is_empty = False
                    break

            if self.model.get_hero().position == new_position:
                cell_with_hero = new_position
                is_empty = False

            if is_empty:
                empty_cells.append(new_position)

        if cell_with_hero is not None:
            return AttackCommand(character, self.model.get_hero(), self.model)

        if len(empty_cells) != 0:
            return MoveCommand(character, np.random.choice(empty_cells))
        else:
            return IdleCommand()

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
