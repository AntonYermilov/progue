from enum import Enum


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
