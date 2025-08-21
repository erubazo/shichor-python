import time
import allure
import pytest
from allure_commons.types import Severity
from tests.base_test import BaseTest

@pytest.mark.usefixtures("setup_driver_class")
@allure.epic("Sign In Tests")
@allure.feature("Sign In and Sign Up")
class TestClass(BaseTest):

    @allure.severity(Severity.CRITICAL)
    @allure.story("Sign Up Fail")
    @allure.description("Test to check failed sign up with incorrect email")
    @allure.title("failed signup Test")
    def test_01_failed_signup(self):
        result = self.signin_page.incorrect_email("loyekab865@jxbav.com")
        assert result == "The code is incorrect or expired."

    @allure.severity(Severity.NORMAL)
    @allure.story("Sign Up Wrong Format")
    @allure.description("Test to check signup with wrong format email")
    @allure.title("wrong format signup Test")
    def test_02_failed_wrong_format(self):
        result = self.signin_page.wrong_format("11111111111")
        assert result == "Please use this format: your@email.com"

    @allure.severity(Severity.NORMAL)
    @allure.story("Incorrect Booking Code")
    @allure.description("Test to check incorrect booking code")
    @allure.title("incorrect booking Test")
    def test_03_incorrect_code(self):
        result = self.signin_page.incorrect_booking("barakqa@gmail.com",12345678,"29","9","1992","LAX")
        assert result == "Booking not found. Are all the details correct?"
