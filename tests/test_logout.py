import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from actions.login_actions import loginactions
from locators.login_locators import LoginPageLocators
from selenium.webdriver.common.by import By


def test_logout(driver):
    driver.get("https://www.saucedemo.com/")
    loginactions(driver, LoginPageLocators,"standard_user", "secret_sauce")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()

    # 🛠 Wait for sidebar animation and logout to become visible and clickable
    wait.until(EC.visibility_of_element_located((By.ID, "logout_sidebar_link")))
    wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()

    assert "saucedemo.com" in driver.current_url and "inventory" not in driver.current_url
