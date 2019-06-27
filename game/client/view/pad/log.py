from game.client.view.pad.pad import Pad


class LogPad(Pad):
    TEXT_COLOR = '#eaeaea'
    HIGHLIGHTED_TEXT_COLOR = '#e6e600'
    BACKGROUND_COLOR = '#000000'

    def refresh(self):
        for x in range(self.x0, self.x1):
            for y in range(self.y0, self.y1):
                self.view._put_colored_symbol(x=x, y=y, c=' ', color=self.BACKGROUND_COLOR, bkcolor=self.BACKGROUND_COLOR)

        if self.view.game_id is not None:
            x, y, s = self.x0, self.y0, self.view.game_id
            self.view._put_colored_text(x=x, y=y, s=s, color=self.HIGHLIGHTED_TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)
            shift = 1
        else:
            shift = 0

        if self.view.model.hero.stats.health == 0:
            x, y, s = self.x0, self.y0 + shift, 'You died'
            self.view._put_colored_text(x=x, y=y, s=s, color=self.HIGHLIGHTED_TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)
        elif self.view.model.my_turn:
            x, y, s = self.x0, self.y0 + shift, 'Your turn'
            self.view._put_colored_text(x=x, y=y, s=s, color=self.HIGHLIGHTED_TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)