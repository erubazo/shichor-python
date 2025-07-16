import time
import pytest
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.devtools.v136.page import navigate
from urllib3 import request
from pages.main_page import MainPage
from tests.base_test import BaseTest
from pages.cookie_page import CookiePage

@pytest.mark.usefixtures("setup_driver_class")  # Apply fixture at class level
class TestClass(BaseTest):

    def test_01_failed_signup(self):
        result = self.signin_page.incorrect_email("loyekab865@jxbav.com")
        assert result == "The code is incorrect or expired."


    def test_02_failed_wrong_format(self):
        result = self.signin_page.wrong_format("11111111111")
        assert result == "Please use this format: your@email.com"


    def test_03_incorrect_code(self):
        result = self.signin_page.incorrect_booking("barakqa@gmail.com",12345678,"29","9","1992","LAX")
        assert result == "Booking not found. Are all the details correct?"
