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

    MOVES_TO_STORE = 10

    MOVE_MAX_WEIGHT = 2.5
    MOVE_MID_WEIGHT = 1.7
    MOVE_MIN_WEIGHT = 1

    MOVE_WEIGHTS = np.array([
        [MOVE_MAX_WEIGHT, MOVE_MIN_WEIGHT, MOVE_MID_WEIGHT, MOVE_MID_WEIGHT],
        [MOVE_MIN_WEIGHT, MOVE_MAX_WEIGHT, MOVE_MID_WEIGHT, MOVE_MID_WEIGHT],
        [MOVE_MID_WEIGHT, MOVE_MID_WEIGHT, MOVE_MAX_WEIGHT, MOVE_MIN_WEIGHT],
        [MOVE_MID_WEIGHT, MOVE_MID_WEIGHT, MOVE_MIN_WEIGHT, MOVE_MAX_WEIGHT],
    ])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_moves = []
        self.total_move_weights = np.ones(len(self.MOVES))

    def _update_move_weights(self):
        self.total_move_weights = np.ones(len(self.MOVES))
        for i, move in enumerate(self.last_moves):
            self.total_move_weights += self.MOVE_WEIGHTS[self.MOVES.index(move)]**(i+1)

    def _add_move(self, move: Direction):
        self.last_moves.append(move)
        if len(self.last_moves) > self.MOVES_TO_STORE:
            self.last_moves = self.last_moves[-self.MOVES_TO_STORE:]
        self._update_move_weights()

    def _get_move_weight(self, move: Direction):
        return self.total_move_weights[self.MOVES.index(move)]

    def _get_move_to_hero(self, character: Character) -> Union[Position, None]:
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

    def _get_random_move(self, character: Character) -> Union[Position, None]:
        available_moves = []
        for move in AggressiveStrategy.MOVES:
            position = character.position + move
            if self.model.get_labyrinth().is_wall(position):
                continue
            if any(mob.position == position for mob in self.model.mobs):
                continue
            available_moves.append(move)

        if len(available_moves) > 0:
            probabilities = np.array([self._get_move_weight(move) for move in available_moves])
            probabilities /= sum(probabilities)
            new_position = character.position + np.random.choice(available_moves, p=probabilities)
            return new_position
        return None

    def on_new_turn(self, character: Character) -> Command:
        new_position = self._get_move_to_hero(character)
        if new_position is None:
            new_position = self._get_random_move(character)

        if new_position is None:
            return IdleCommand()
        if new_position == self.model.get_hero().position:
            return AttackCommand(character, self.model.get_hero(), self.model)

        self._add_move(new_position - character.position)
        return MoveCommand(character, new_position)

