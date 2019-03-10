from game.elements import MapBlock, Artifact, Character, Object


class VisualElement:
    def __init__(self, symbol, color=0):
        self.symbol = symbol
        self.color = color


scheme = {
    MapBlock.WALL: VisualElement('#'),
    MapBlock.FLOOR: VisualElement(' '),
    Artifact.GOLD: VisualElement('$'),
    Artifact.HEALING_POTION: VisualElement('!'),
    Artifact.AMNESIA_POTION: VisualElement('!'),
    Artifact.KNOWLEDGE_SCROLL: VisualElement('♪'),
    Artifact.CURSED_SCROLL: VisualElement('♪'),
    Character.SNAKE: VisualElement('s'),
    Character.GHOST: VisualElement('g'),
    Character.HERO: VisualElement('@'),
    Object.EXIT: VisualElement('Ø')
}
