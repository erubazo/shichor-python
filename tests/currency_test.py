import time
import pytest
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.devtools.v136.page import navigate
from urllib3 import request
from pages.main_page import MainPage
from tests.base_test import BaseTest
from pages.cookie_page import CookiePage


@pytest.mark.usefixtures("setup_driver_class")
class TestClass(BaseTest):

    def test_01_change_coin(self):
        self.currency_page.select_currency("Euro")

    def test_02_change_region(self):
        self.currency_page.select_region("United States","English")





