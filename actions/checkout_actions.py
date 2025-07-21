from actions.actions import Actions


class CheckoutActions(Actions):
    def enter_checkout_info(self, first_name, last_name, postal_code):
        self.enter_text(self.locators.first_name, first_name)
        self.enter_text(self.locators.last_name, last_name)
        self.enter_text(self.locators.postal_code, postal_code)
        self.click(self.locators.continue_button)

    def finish_checkout(self):
        self.click(self.locators.finish_button)
