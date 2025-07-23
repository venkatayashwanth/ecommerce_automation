from actions.actions import Actions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartActions(Actions):
    def click_checkout(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.locators.checkout_button))
        self.click(self.locators.checkout_button)
