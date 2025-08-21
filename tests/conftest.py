import os
import allure
import pytest
from selenium import webdriver
from pages.cookie_page import CookiePage
from pages.currency_page import CurrencyPage
from pages.main_page import MainPage
from pages.signin_page import SignInPage
from utils.config import ConfigReader

@pytest.fixture(scope="class")
def setup_driver_class(request):
    url = ConfigReader.read_config("general", "base_url")
    
    # Set Chrome options
    options = webdriver.ChromeOptions()
    if os.getenv("GITHUB_ACTIONS"):  # Running in GitHub Actions
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:  # Local environment
        options.add_argument("--start-maximized")

    # Launch Chrome
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver

    # Navigate to base URL
    driver.get(url)

    # Initialize page objects
    request.cls.main_page = MainPage(driver)
    request.cls.cookie_page = CookiePage(driver)
    request.cls.currency_page = CurrencyPage(driver)
    request.cls.signin_page = SignInPage(driver)

    yield
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def attach_driver_to_node(request):
    """Attach driver instance to node for Allure screenshots on failure."""
    if hasattr(request.cls, "driver"):
        request.node.driver = request.cls.driver

def pytest_exception_interact(node, call, report):
    """Attach screenshot to Allure if a test fails."""
    driver = getattr(node, "driver", None)
    if report.failed and driver:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
