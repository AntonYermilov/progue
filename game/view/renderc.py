import curses
import logging

from game.model import Model
from game.view.elements import scheme

element_colors = {}


def draw_element(window, y: int, x: int, element):
    window.attron(curses.color_pair(element_colors[element]))
    window.addstr(y, x, scheme[element].symbol.encode('utf-8'))
    window.attroff(curses.color_pair(element_colors[element]))


def draw_map(model: Model, pad):
    for y, row in enumerate(model.labyrinth):
        for x, map_element in enumerate(row):
            draw_element(pad, y, x, map_element)

    for entity, instance in model.entities:
        y, x = instance.position
        draw_element(pad, y, x, entity)


def draw_status_bar(model: Model, screen):
    pass


def initialise_colors():
    curses.start_color()

    color_index = 1

    for element, visual in scheme.items():
        element_colors[element] = color_index
        curses.init_pair(color_index, visual.color.primary, visual.color.secondary)
        color_index += 1


def draw_scene(model: Model, screen):
    key_pressed = 0

    screen.clear()
    screen.refresh()

    initialise_colors()

    map_y = model.shape()[0]
    map_x = model.shape()[1]
    logging.debug(f"Map shape: y={map_y}, x={map_x}")
    map_pad = curses.newpad(map_y + 1, map_x + 1)  # pad should be +1 of it's working area

    while key_pressed != ord('q'):
        screen_height, screen_width = screen.getmaxyx()
        screen.clear()

        map_origin_y = screen_height // 2 - map_y // 2
        map_origin_x = screen_width // 2 - map_x // 2

        screen.refresh()

        draw_map(model, map_pad)
        map_pad.refresh(0, 0, map_origin_y, map_origin_x, map_origin_y + 50, map_origin_x + 50)

        draw_status_bar(model, screen)

        screen.refresh()
        key_pressed = screen.getch()
