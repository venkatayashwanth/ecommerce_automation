from selenium.webdriver.common.by import By


class InventoryPageLocators:
    first_item_add_button = (By.ID, "add-to-cart-sauce-labs-backpack")
    cart_icon = (By.CLASS_NAME, "shopping_cart_link")
