from dataclasses import dataclass


@dataclass
class Position:
    row: int
    col: int

    @staticmethod
    def as_point(x: int, y: int):
        return Position(y, x)

    @staticmethod
    def as_position(row: int, col: int):
        return Position(row, col)

    def __add__(self, other):
        return Position(self.row + other.row, self.col + other.col)

    def __iter__(self):
        return iter((self.row, self.col))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def get_x(self) -> int:
        return self.col

    def get_y(self) -> int:
        return self.row


Direction = Position