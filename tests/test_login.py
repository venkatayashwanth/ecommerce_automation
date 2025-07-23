import pytest
from actions.login_actions import loginactions
from locators.login_locators import LoginPageLocators
from utils.json_reader import load_json_data

test_data = load_json_data("login_data.json")


@pytest.mark.parametrize("data", test_data)
def test_login_with_json(driver, data):
    driver.delete_all_cookies()
    driver.get("https://www.saucedemo.com/")
    loginactions(driver, LoginPageLocators,data["username"], data["password"])
    if data["username"] == "locked_out_user":
        assert "inventory" not in driver.current_url
    else:
        assert "inventory" in driver.current_url
