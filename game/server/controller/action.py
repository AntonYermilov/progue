from enum import Enum
from typing import Union

from attr import dataclass


class ActionType(Enum):
    MOVE_ACTION: int = 0
    INVENTORY_ACTION: int = 1


@dataclass
class MoveAction:
    row: int
    col: int


class ItemAction(Enum):
    USE: int = 0
    DROP: int = 1
    PICK: int = 2


@dataclass
class InventoryAction:
    item_id: int
    action: ItemAction


@dataclass
class Action:
    type: ActionType
    desc: Union[MoveAction, InventoryAction]
