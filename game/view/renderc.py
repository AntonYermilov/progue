import _curses
import curses

from game.model import Model
from game.view.elements import scheme
import logging


def draw_map(model: Model, pad):
    pad.attron(curses.color_pair(1))

    for y, row in enumerate(model.labyrinth):
        for x, map_element in enumerate(row):
            pad.addch(y, x, ord(scheme[map_element].symbol))

    for entity, instance in model.entities:
        y, x = instance.position
        pad.addstr(y, x, scheme[entity].symbol.encode('utf-8'))

    pad.attroff(curses.color_pair(1))


def draw_status_bar(model: Model, screen):
    pass


def draw_scene(model: Model, screen):
    key_pressed = 0

    screen.clear()
    screen.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN) # map colors
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    map_y = model.shape()[0]
    map_x = model.shape()[1]
    logging.debug(f"Map shape: y={map_y}, x={map_x}")
    map_pad = curses.newpad(map_y + 1, map_x + 1) # pad should be +1 of it's working area

    while key_pressed != ord('q'):
        screen_height, screen_width = screen.getmaxyx()
        # screen.clear()

        map_origin_y = screen_height // 2 - map_y // 2
        map_origin_x = screen_width // 2 - map_x // 2

        draw_map(model, map_pad)
        map_pad.refresh(0, 0, map_origin_y, map_origin_x, map_origin_y + 50, map_origin_x + 50)

        draw_status_bar(model, screen)

        screen.refresh()
        key_pressed = screen.getch()
