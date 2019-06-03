from game.client.view.pad.pad import Pad


class LegendPad(Pad):
    TEXT_COLOR = '#eaeaea'
    HIGHLIGHTED_TEXT_COLOR = '#e6e600'
    BACKGROUND_COLOR = '#26004d'

    def _refresh_inventory(self):
        self.view._put_colored_symbol(self.x0, self.y0, 'I', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_text(self.x0 + 1, self.y0, 'nventory', self.TEXT_COLOR, self.BACKGROUND_COLOR)

    def refresh(self):
        self._refresh_inventory()