import pytest
import os
from selenium import webdriver
from datetime import datetime

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox"
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        options = ChromeOptions()
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        service = Service(log_path=os.devnull)
        driver = webdriver.Chrome(service=service,options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        #options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = os.path.join("screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)
            driver.save_screenshot(filepath)
            print(f"\n[📸 Screenshot saved]: {filepath}")
