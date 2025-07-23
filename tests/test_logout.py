import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from actions.login_actions import loginactions
from locators.login_locators import LoginPageLocators


def test_logout(driver):
    driver.delete_all_cookies()
    driver.get("https://www.saucedemo.com/")
    loginactions(driver, LoginPageLocators, "standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)

    # Open side menu
    menu = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
    menu.click()

    # Wait for menu animation and logout link
    logout_link = wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
    logout_link.click()

    # Wait until login button appears again (after redirect to login page)
    login_btn = wait.until(EC.visibility_of_element_located((By.ID, "login-button")))

    assert login_btn.is_displayed()
