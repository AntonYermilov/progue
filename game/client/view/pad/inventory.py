from game.client.model.inventory import Inventory
from game.client.view.pad.pad import Pad


class InventoryPad(Pad):
    TEXT_COLOR = '#eaeaea'
    HIGHLIGHTED_TEXT_COLOR = '#e6e600'
    # BACKGROUND_COLOR = '#26004d'
    BACKGROUND_COLOR = '#000000'

    EMPTY_INVENTORY_TEXT = 'INVENTORY IS EMPTY'

    def _determine_width(self, inventory: Inventory):
        if inventory.size() == 0:
            return len(self.EMPTY_INVENTORY_TEXT) + 6
        width = 0
        for item in inventory.items:
            desc = self.view.entities_desc['items'][item.name]['desc']
            width = max(width, len(desc))
        return width + 6

    def _refresh_background(self, width: int, height: int):
        for x in range(self.x1 - width, self.x1):
            for y in range(self.y0, self.y0 + height):
                self.view._put_colored_symbol(x=x, y=y, c=' ', color=self.TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)

    def _determine_text_position(self, width: int, text):
        return self.x1 - (width + 1) // 2 - (len(text) + 1) // 2

    def _refresh_inventory(self, width: int, inventory: Inventory):
        if inventory.size() == 0:
            text = 'INVENTORY IS EMPTY'
            x, y= self._determine_text_position(width, text), self.y0 + 1
            self.view._put_colored_text(x=x, y=y, s=text, color=self.HIGHLIGHTED_TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)
            return

        for i, item in enumerate(inventory.items):
            desc = self.view.entities_desc['items'][item.name]['desc']
            x, y = self.x1 - width + 3, self.y0 + i + 1
            self.view._put_colored_text(x=x, y=y, s=desc, color=self.TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)

        if inventory.get_selected_item() is not None:
            x, y = self.x1 - width + 1, self.y0 + 1 + inventory.get_selected_item_position()
            self.view._put_colored_symbol(x=x, y=y, c='*', color=self.HIGHLIGHTED_TEXT_COLOR, bkcolor=self.BACKGROUND_COLOR)

    def refresh(self):
        inventory = self.view.model.inventory
        if not inventory.is_opened():
            return
        width = self._determine_width(inventory)
        height = max(1, inventory.size()) + 2
        self._refresh_background(width, height)
        self._refresh_inventory(width, inventory)
