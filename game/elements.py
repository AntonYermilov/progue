from enum import Enum

from game.model.artifacts import Gold, HealingPotion, KnowledgeScroll, AmnesiaPotion, CursedScroll
from game.model.character import Snake, Ghost, Hero
from game.model.exit import Exit


class MapBlock(Enum):
    FLOOR = 0
    WALL = 1


class Object(Enum):
    EXIT = 0


class Artifact(Enum):
    GOLD = 1
    HEALING_POTION = 2
    AMNESIA_POTION = 3
    KNOWLEDGE_SCROLL = 4
    CURSED_SCROLL = 5


class Character(Enum):
    HERO = 0
    SNAKE = 1
    GHOST = 2
