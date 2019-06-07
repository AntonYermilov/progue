from typing import List
import numpy as np

from game.client.view.pad.pad import Pad


class StatsPad(Pad):
    TEXT_COLOR = '#eaeaea'
    HIGHLIGHTED_TEXT_COLOR = '#e6e600'
    BACKGROUND_COLOR = '#000000'

    HEALTH_GRADATION = ['#0052cc', '#0047b3', '#003d99', '#003380', '#002966', '#001433']
    EXPERIENCE_GRADATION = ['#b300b3', '#990099', '#800080', '#660066', '#4d004d', '#330033']

    NAME_ROW = 0
    HEALTH_ROW = 1
    EXPERIENCE_ROW = 2

    MOB_ROW = 6

    @staticmethod
    def _fit_text_to_length(text: str, length: int):
        while len(text) < length:
            text = ' ' + text + ' '
        if len(text) > 20:
            text = text[1:]
        return text

    def _refresh_character_health(self, character, x0, y0, width):
        health_text = self._fit_text_to_length('Health', width)
        cur, step = 0, character.stats.max_health / width
        health = character.stats.health
        for i, c in enumerate(health_text):
            if cur + step < health:
                bkcolor = self.HEALTH_GRADATION[0]
            elif cur > health:
                bkcolor = self.HEALTH_GRADATION[-1]
            else:
                position = int(np.floor(5 * (cur + step - health) / step))
                bkcolor = self.HEALTH_GRADATION[position]
            x, y = x0 + i, y0
            self.view._put_colored_symbol(x=x, y=y, c=c, color=self.TEXT_COLOR, bkcolor=bkcolor)
            cur += step

    def _refresh_hero_experience(self, hero, x0, y0, width):
        experience_text = self._fit_text_to_length('Experience', width)
        cur, step = 0, hero.stats.max_experience / width
        experience = hero.stats.experience
        for i, c in enumerate(experience_text):
            if cur + step < experience:
                bkcolor = self.EXPERIENCE_GRADATION[0]
            elif cur > experience:
                bkcolor = self.EXPERIENCE_GRADATION[-1]
            else:
                position = int(np.floor(5 * (cur + step - experience) / step))
                bkcolor = self.EXPERIENCE_GRADATION[position]
            x, y = x0 + i, y0
            self.view._put_colored_symbol(x=x, y=y, c=c, color=self.TEXT_COLOR, bkcolor=bkcolor)
            cur += step

    def _refresh_hero_stats(self, width: int):
        x, y = self.x0, self.y0 + self.NAME_ROW
        color = self.view.entities_desc['hero']['foreground_color']
        bkcolor = self.view.entities_desc['hero']['background_color']
        desc = f': You (level {self.view.model.hero.stats.level})'
        self.view._put_colored_symbol(x=x, y=y, c='@', color=color, bkcolor=bkcolor)
        self.view._put_colored_text(x=x+1, y=y, s=desc, color=self.TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)

        self._refresh_character_health(self.view.model.hero, self.x0, self.y0 + self.HEALTH_ROW, width)
        self._refresh_hero_experience(self.view.model.hero, self.x0, self.y0 + self.EXPERIENCE_ROW, width)

    def refresh(self):
        width = self.x1 - self.x0 - 1
        self._refresh_hero_stats(width)

    def refresh_enemies(self, visible_enemies: List):
        width = self.x1 - self.x0 - 1
        for i, enemy in enumerate(visible_enemies):
            if enemy.name not in self.view.entities_desc['mobs']:
                enemy_desc = self.view.entities_desc['hero'].copy()
                enemy_desc['foreground_color'] = '#0000ff'
            else:
                enemy_desc = self.view.entities_desc['mobs'][enemy.name]
            view = enemy_desc['view']
            color = enemy_desc['foreground_color']
            bkcolor = enemy_desc['background_color']
            desc = f': {enemy.name}'
            x, y = self.x0, self.y0 + self.MOB_ROW + i * 3
            self.view._put_colored_symbol(x=x, y=y, c=view, color=color, bkcolor=bkcolor)
            self.view._put_colored_text(x=x+1, y=y, s=desc, color=self.TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)
            self._refresh_character_health(enemy, x, y + 1, width)