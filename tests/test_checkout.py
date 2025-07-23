import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from actions.login_actions import loginactions
from actions.inventory_actions import InventoryActions
from actions.cart_actions import CartActions
from actions.checkout_actions import CheckoutActions
from locators.login_locators import LoginPageLocators
from locators.inventory_locators import InventoryPageLocators
from locators.cart_locators import CartPageLocators
from locators.checkout_locators import CheckoutPageLocators


def test_checkout_process(driver):
    driver.delete_all_cookies()
    driver.get("https://www.saucedemo.com/")
    loginactions(driver, LoginPageLocators, "standard_user", "secret_sauce")
    time.sleep(3)  # adjust this if needed
    driver.execute_script(""" 
        const observer = new MutationObserver((mutations) => {
            const popup = document.querySelector('div[role="dialog"], .modal, #popup-modal');
            if (popup) {
                popup.remove();
            }
            const backdrop = document.querySelector('.modal-backdrop, .MuiBackdrop-root');
            if (backdrop) {
                backdrop.remove();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    """)

    inventory = InventoryActions(driver, InventoryPageLocators)
    cart = CartActions(driver, CartPageLocators)
    checkout = CheckoutActions(driver, CheckoutPageLocators)

    inventory.add_first_item_to_cart()
    inventory.go_to_cart()
    #element = WebDriverWait(driver,10).until(EC.presence_of_element_located(CheckoutPageLocators.checkout_button))
    #driver.execute_script("arguments[0].scrollIntoView();", element)
    cart.click_checkout()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "first-name")))  # ✅ Ensures we are on checkout step one

    checkout.enter_checkout_info("John", "Doe", "12345")
    wait.until(EC.presence_of_element_located((By.ID, "finish")))

    checkout.finish_checkout()

    # Wait until redirected to checkout complete page
    wait.until(EC.url_contains("checkout-complete"))

    assert "checkout-complete" in driver.current_url
