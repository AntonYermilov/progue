from game.client.view.pad.pad import Pad


class MenuPad(Pad):
    TEXT_COLOR = '#eaeaea'
    HIGHLIGHTED_TEXT_COLOR = '#e6e600'
    BACKGROUND_COLOR = '#000000'

    def __init__(self, view, x0: int, y0: int, x1: int, y1: int):
        super().__init__(view, x0, y0, x1, y1)
        self.menu = None

    def set_menu(self, menu):
        self.menu = menu

    def refresh(self):
        if self.menu is not None:
            menu = self.menu
        else:
            menu = self.view.controller.menu

        for i, btn in enumerate(menu.buttons):
            x, y = self.x0 + 3, self.y0 + 2 * i
            self.view._put_colored_text(x=x, y=y, s=btn, color=self.TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)
            self.view._put_colored_symbol(x=x, y=y, c=btn[0], color=self.HIGHLIGHTED_TEXT_COLOR,
                                          bkcolor=self.BACKGROUND_COLOR)

        x, y = self.x0 + 1, self.y0 + menu.position * 2
        self.view._put_colored_symbol(x=x, y=y, c='*', color=self.HIGHLIGHTED_TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)
