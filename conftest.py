import pytest
import os
from selenium import webdriver
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()
    # Enable headless mode if environment variable is set
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")  # use "--headless=new" for newer Chrome versions

    # Disable password manager completely
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Disable extensions, info bars, and automation controls
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    # Start Chrome in incognito mode
    options.add_argument("--incognito")

    # Hide "Chrome is being controlled by automated test software"
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Additional trick to prevent detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver


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
