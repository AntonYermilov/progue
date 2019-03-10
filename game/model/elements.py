from game.elements import Object, Artifact, Character
from game.model.artifacts import Gold, CursedScroll, KnowledgeScroll, AmnesiaPotion, HealingPotion
from game.model.character import Hero, Snake, Ghost
from game.model.exit import Exit

to_class = {
    Object.EXIT: Exit,
    Artifact.GOLD: Gold,
    Artifact.CURSED_SCROLL: CursedScroll,
    Artifact.KNOWLEDGE_SCROLL: KnowledgeScroll,
    Artifact.AMNESIA_POTION: AmnesiaPotion,
    Artifact.HEALING_POTION: HealingPotion,
    Character.HERO: Hero,
    Character.SNAKE: Snake,
    Character.GHOST: Ghost
}
