import pytest
from selenium import webdriver
import socket
import requests

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


