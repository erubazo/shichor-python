import pytest
from selenium import webdriver
import socket
import requests

from pages.api_page import ApiPage
from pages.cookie_page import CookiePage
from pages.currency_page import CurrencyPage
from pages.main_page import MainPage
from pages.signin_page import SignInPage
from utils.config import ConfigReader


@pytest.fixture(scope="class")
def setup_driver_class(request):
    url = ConfigReader.read_config("general","base_url")
    request.cls.driver = webdriver.Chrome()
    request.cls.driver.maximize_window()
    request.cls.driver.get(url)
    request.cls.main_page = MainPage(request.cls.driver)
    request.cls.cookie_page = CookiePage(request.cls.driver)
    request.cls.currency_page = CurrencyPage(request.cls.driver)
    request.cls.signin_page = SignInPage(request.cls.driver)
    yield
    request.cls.driver.quit()

@pytest.fixture(scope="class")
def setup_api_class(request):
    """Initialize ApiPage for API tests"""
    try:
        # Try to get api_url from config first
        try:
            from utils.config import ConfigReader
            api_url = ConfigReader.read_config("general", "api_url")
            print(f"Using API URL from config: {api_url}")
        except Exception:
            # Fall back to default URL
            from data.test_data import Test_data
            api_url = Test_data.Base_URL
            print(f"Using default API URL: {api_url}")

        # Check if localhost is in the URL and verify server is running
        if "localhost" in api_url or "127.0.0.1" in api_url:
            # Parse host and port from URL
            parts = api_url.split("://")[1].split("/")[0].split(":")
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 80

            # Check if port is open
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()

            if result != 0:
                print(f"WARNING: Cannot connect to API server at {host}:{port}")
                print("==========================================================")
                print("MAKE SURE YOUR API SERVER IS RUNNING BEFORE RUNNING TESTS!")
                print("==========================================================")

        # Initialize ApiPage without a driver
        request.cls.api_page = ApiPage(base_url=api_url)
        print(f"API Page initialized in fixture with URL: {request.cls.api_page.base_url}")
    except Exception as e:
        print(f"Error in setup_api_class fixture: {e}")
        import traceback
        traceback.print_exc()

        # Still create the api_page so tests don't fail immediately
        try:
            from data.test_data import Test_data
            request.cls.api_page = ApiPage(base_url=Test_data.Base_URL)
        except Exception:
            pass
    yield
