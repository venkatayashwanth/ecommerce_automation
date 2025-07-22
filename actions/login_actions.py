from actions.actions import Actions


def loginactions(driver, locators, username, password):
    login = Actions(driver, locators)
    login.enter_text(locators.username, username)
    login.enter_text(locators.password, password)
    login.click(locators.login_button)
