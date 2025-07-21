import pytest
from actions.login_actions import loginactions
from actions.inventory_actions import InventoryActions
from actions.cart_actions import CartActions
from actions.checkout_actions import CheckoutActions
from locators.login_locators import LoginPageLocators
from locators.inventory_locators import InventoryPageLocators
from locators.cart_locators import CartPageLocators
from locators.checkout_locators import CheckoutPageLocators


def test_checkout_process(driver):
    driver.get("https://www.saucedemo.com/")
    loginactions(driver, LoginPageLocators,"standard_user", "secret_sauce")
    InventoryActions(driver, InventoryPageLocators).add_first_item_to_cart()
    InventoryActions(driver, InventoryPageLocators).go_to_cart()
    CartActions(driver, CartPageLocators).click_checkout()

    checkout = CheckoutActions(driver, CheckoutPageLocators)
    checkout.enter_checkout_info("John", "Doe", "12345")
    checkout.finish_checkout()

    assert "checkout-complete" in driver.current_url
