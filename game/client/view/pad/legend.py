from game.client.view.pad.pad import Pad


class LegendPad(Pad):
    TEXT_COLOR = '#eaeaea'
    HIGHLIGHTED_TEXT_COLOR = '#e6e600'
    BACKGROUND_COLOR = '#26004d'
    # BACKGROUND_COLOR = '#000000'

    INVENTORY_TEXT = '   Inventory   '
    SKIP_TEXT = '   Skip turn   '
    NEXT_TEXT = '  Next (↓)  '
    PREV_TEXT = '  Prev (↑)  '
    USE_TEXT = '   Use   '
    DROP_TEXT = '  Drop  '
    QUIT_TEXT = '  Quit  '
    ORDER = [INVENTORY_TEXT, SKIP_TEXT, NEXT_TEXT, PREV_TEXT, USE_TEXT, DROP_TEXT]

    @staticmethod
    def _get_shift(text):
        shift = 0
        for btn_text in LegendPad.ORDER:
            if btn_text == text:
                break
            shift += len(btn_text) + 4
        return shift

    def _refresh_background(self):
        void_color = self.view.entities_desc['map']['void']['background_color']
        for x in range(self.x0, self.x1):
            for y in range(self.y0, self.y1):
                self.view._put_colored_symbol(x=x, y=y, c=' ', color=void_color, bkcolor=void_color)

    def _refresh_inventory(self):
        x, y = self.x0 + self._get_shift(self.INVENTORY_TEXT), self.y1 - 1
        xi = self.INVENTORY_TEXT.index('I')
        self.view._put_colored_text(x, y, self.INVENTORY_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xi, y, 'I', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def _refresh_skip(self):
        x, y = self.x0 + self._get_shift(self.SKIP_TEXT), self.y1 - 1
        xs = self.SKIP_TEXT.index('S')
        self.view._put_colored_text(x, y, self.SKIP_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xs, y, 'S', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def _refresh_next(self):
        if not self.view.model.inventory.is_opened():
            return
        x, y = self.x0 + self._get_shift(self.NEXT_TEXT), self.y1 - 1
        xd = self.NEXT_TEXT.index('↓')
        self.view._put_colored_text(x, y, self.NEXT_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xd, y, '↓', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def _refresh_prev(self):
        if not self.view.model.inventory.is_opened():
            return
        x, y = self.x0 + self._get_shift(self.PREV_TEXT), self.y1 - 1
        xu = self.PREV_TEXT.index('↑')
        self.view._put_colored_text(x, y, self.PREV_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xu, y, '↑', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def _refresh_use(self):
        if not self.view.model.inventory.is_opened():
            return
        if self.view.model.inventory.get_selected_item() is None:
            return
        x, y = self.x0 + self._get_shift(self.USE_TEXT), self.y1 - 1
        xu = self.USE_TEXT.index('U')
        self.view._put_colored_text(x, y, self.USE_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xu, y, 'U', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def _refresh_drop(self):
        if not self.view.model.inventory.is_opened():
            return
        if self.view.model.inventory.get_selected_item() is None:
            return
        x, y = self.x0 + self._get_shift(self.DROP_TEXT), self.y1 - 1
        xd = self.DROP_TEXT.index('D')
        self.view._put_colored_text(x, y, self.DROP_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xd, y, 'D', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def _refresh_quit(self):
        if self.view.model.inventory.is_opened():
            return
        x, y = self.x1 - len(self.QUIT_TEXT), self.y1 - 1
        xq = self.QUIT_TEXT.index('Q')
        self.view._put_colored_text(x, y, self.QUIT_TEXT, self.TEXT_COLOR, self.BACKGROUND_COLOR)
        self.view._put_colored_symbol(x + xq, y, 'Q', self.HIGHLIGHTED_TEXT_COLOR, self.BACKGROUND_COLOR)

    def refresh(self):
        self._refresh_background()
        if self.view.model.hero.stats.health > 0:
            self._refresh_inventory()
            self._refresh_skip()
            self._refresh_next()
            self._refresh_prev()
            self._refresh_use()
            self._refresh_drop()
        self._refresh_quit()
