import time
import pytest
import allure
from allure_commons.types import Severity

from pages.cookie_page import CookiePage
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_driver_class")
@allure.epic("Currency and Region Tests")
@allure.feature("Currency and Region Change")
class TestClass(BaseTest):

    @allure.severity(Severity.NORMAL)
    @allure.story("Changing Currency")
    @allure.description("Test to check coin change")
    @allure.title("Coin Change Test")
    def test_01_change_coin(self):
        with allure.step("Accept cookies if present"):
            self.main_page.accept_cookies()
        with allure.step("Changing currency to Euro"):
            self.currency_page.select_currency("Euro")

    @allure.severity(Severity.NORMAL)
    @allure.story("Changing Region")
    @allure.description("Test to check country change")
    @allure.title("Country Change Test")
    def test_02_change_region(self):
        with allure.step("Accept cookies if present"):
            self.main_page.accept_cookies()
        with allure.step("Changing region to United States and language to English"):
            self.currency_page.select_region("United States", "English")





