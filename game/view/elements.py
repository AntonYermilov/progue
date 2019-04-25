import curses
from collections import namedtuple

from game.elements import MapBlock, Artifact, Character, Object

Color = namedtuple('Color', ['primary', 'secondary'])


class VisualElement:
    def __init__(self, symbol, color=Color(primary=curses.COLOR_WHITE, secondary=curses.COLOR_BLACK)):
        self.symbol = symbol
        self.color = color


scheme = {
    MapBlock.WALL: VisualElement('#'),
    MapBlock.FLOOR: VisualElement(' '),
    Artifact.GOLD: VisualElement('$'),
    Artifact.HEALING_POTION: VisualElement('!'),
    Artifact.AMNESIA_POTION: VisualElement('!'),
    # Artifact.KNOWLEDGE_SCROLL: VisualElement('♪'),
    Artifact.KNOWLEDGE_SCROLL: VisualElement('S'),
    # Artifact.CURSED_SCROLL: VisualElement('♪'),
    Artifact.CURSED_SCROLL: VisualElement('S'),
    Character.SNAKE: VisualElement('s'),
    Character.GHOST: VisualElement('g'),
    Character.HERO: VisualElement('@', Color(primary=curses.COLOR_RED, secondary=curses.COLOR_YELLOW)),
    Object.EXIT: VisualElement('Ø')
}
