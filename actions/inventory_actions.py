from actions.actions import Actions


class InventoryActions(Actions):
    def add_first_item_to_cart(self):
        self.click(self.locators.first_item_add_button)

    def go_to_cart(self):
        self.click(self.locators.cart_icon)
