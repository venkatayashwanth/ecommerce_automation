from actions.actions import Actions


class CartActions(Actions):
    def click_checkout(self):
        self.click(self.locators.checkout_button)
