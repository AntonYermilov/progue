from typing import Tuple, List

from game import Position
from game.model.entity.character import Hero
from .pad import Pad


class MapPad(Pad):
    SHADE_DISTANCE = 11

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.distance = None
        self.visited = set()
        self.first_refresh = True
        self.visible_enemies = []

    @staticmethod
    def _shade_hex_color(color: str):
        r, g, b = f'0x{color[1:3]}', f'0x{color[3:5]}', f'0x{color[5:7]}'
        r, g, b = int(r, base=16), int(g, base=16), int(b, base=16)
        return f'{r // 4},{g // 4},{b // 4}'

    def _update_colors(self, position: Position, color: str, bkcolor: str) -> Tuple[str, str]:
        if self.distance[position.row, position.col] > self.SHADE_DISTANCE:
            color = self._shade_hex_color(color)
            bkcolor = self._shade_hex_color(bkcolor)
        return color, bkcolor

    def _set_visited(self, position: Position):
        self.visited.add((position.row, position.col))

    def _is_visited(self, position: Position) -> bool:
        return (position.row, position.col) in self.visited

    def _refresh_map(self):
        labyrinth = self.view.model.labyrinth
        for row in range(labyrinth.rows):
            for col in range(labyrinth.columns):
                position = Position.as_position(row, col)
                x, y = self.x0 + position.get_x(), self.y0 + position.get_y()
                if self.distance[position.row, position.col] <= self.SHADE_DISTANCE:
                    cell_desc = self.view.entities_desc['map']['wall' if labyrinth.is_wall(position) else 'floor']
                    c, color, bkcolor = cell_desc['view'], cell_desc['foreground_color'], cell_desc['background_color']
                    self._set_visited(position)
                elif self._is_visited(position):
                    cell_desc = self.view.entities_desc['map']['wall' if labyrinth.is_wall(position) else 'floor']
                    c, color, bkcolor = cell_desc['view'], cell_desc['foreground_color'], cell_desc['background_color']
                    color, bkcolor = self._update_colors(position, color, bkcolor)
                else:
                    cell_desc = self.view.entities_desc['map']['void']
                    c, color, bkcolor = cell_desc['view'], cell_desc['foreground_color'], cell_desc['background_color']
                self.view._put_colored_symbol(x=x, y=y, c=c, color=color, bkcolor=bkcolor)

    def _refresh_items(self):
        items = self.view.model.items
        for item in items:
            x, y = self.x0 + item.position.get_x(), self.y0 + item.position.get_y()
            if self.distance[item.position.row, item.position.col] > self.SHADE_DISTANCE:
                continue
            item_desc = self.view.entities_desc['items'][item.name]
            c, color, bkcolor = item_desc['view'], item_desc['foreground_color'], item_desc['background_color']
            self.view._put_colored_symbol(x=x, y=y, c=c, color=color, bkcolor=bkcolor)

    def _refresh_enemies(self):
        enemies = self.view.model.mobs
        self.visible_enemies = []
        for enemy in enemies:

            x, y = self.x0 + enemy.position.get_x(), self.y0 + enemy.position.get_y()
            if self.distance[enemy.position.row, enemy.position.col] > self.SHADE_DISTANCE:
                continue
            self.visible_enemies.append(enemy)
            if enemy.name not in self.view.entities_desc['mobs']:
                enemy_desc = self.view.entities_desc['hero'].copy()
                enemy_desc['foreground_color'] = '#0000ff'
            else:
                enemy_desc = self.view.entities_desc['mobs'][enemy.name]
            c, color, bkcolor = enemy_desc['view'], enemy_desc['foreground_color'], enemy_desc['background_color']
            self.view._put_colored_symbol(x=x, y=y, c=c, color=color, bkcolor=bkcolor)

    def _refresh_hero(self):
        hero = self.view.model.hero
        x, y = self.x0 + hero.position.get_x(), self.y0 + hero.position.get_y()
        hero_desc = self.view.entities_desc['hero']
        c, color, bkcolor = hero_desc['view'], hero_desc['foreground_color'], hero_desc['background_color']
        self.view._put_colored_symbol(x=x, y=y, c=c, color=color, bkcolor=bkcolor)

    def refresh(self):
        labyrinth = self.view.model.labyrinth
        hero = self.view.model.hero
        self.distance = labyrinth.get_distances(hero.position, self.SHADE_DISTANCE)

        if self.first_refresh:
            labyrinth.initialize_void_cells()

        self._refresh_map()
        self._refresh_items()
        self._refresh_enemies()
        self._refresh_hero()

        self.first_refresh = False

    def get_visible_enemies(self) -> List:
        return self.visible_enemies
