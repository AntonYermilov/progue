from game.model import Model
from game.elements import Artifact, Character, Object
from game.view import render

if __name__ == "__main__":
    m = Model()
    m.generate_labyrinth(base_side_length=7, min_labyrinth_size=190)
    m.place_entities({Artifact.GOLD: 10,
                      Character.GHOST: 5,
                      Character.SNAKE: 5,
                      Artifact.HEALING_POTION: 5,
                      Artifact.KNOWLEDGE_SCROLL: 5,
                      Character.HERO: 1,
                      Object.EXIT: 1})
    render(m)
