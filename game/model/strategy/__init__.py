from .aggressive import AggressiveStrategy
from .coward import CowardStrategy
from .passive import PassiveStrategy

strategies = {
    'aggressive': AggressiveStrategy,
    'coward': CowardStrategy,
    'passive': PassiveStrategy
}