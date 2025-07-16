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

    def test_01_cookie_test(self):
        self.cookie_page.customize_cookies(False, True, True, True)
        cookie = self.cookie_page.get_cookie()
        assert cookie == "true"

    def test_02_links_check(self):
        self.main_page.click(self.main_page.ACCEPT)
        cars = self.main_page.link_checker_diff(self.main_page.CARS,"Cars")
        print(cars)
        stay = self.main_page.link_checker_diff(self.main_page.STAYS,"Stay")
        print(stay)
        magazine = self.main_page.link_checker_diff(self.main_page.MAGAZINE,"Magazine")
        print(magazine)
        hacks = self.main_page.link_checker_same(self.main_page.TRAVLE_HACKS, "Travel Hacks")
        print(hacks)
        self.main_page.driver.back()
        deals = self.main_page.link_checker_same(self.main_page.DEALS,"Deals")
        print(deals)
        self.main_page.driver.back()
        help_btn = self.main_page.link_checker_diff(self.main_page.HELP,"Help")
        result = all([cars, stay, magazine, hacks, deals, help_btn])
        assert result == True

    def test_03_trip_ticket(self):
        self.main_page.cookie_accept()
        self.main_page.choose_trip("oneway")
        result = self.main_page.choose_trip("return")
        assert result == "Return"

    def test_04_class(self):
        self.main_page.cookie_accept()
        self.main_page.choose_class("premium",True)
        self.main_page.choose_class("business")
        self.main_page.choose_class("firstclass")
        result = self.main_page.choose_class("economy")
        assert result == "Economy"

    def test_05_passengers(self):
        self.main_page.cookie_accept()
        self.main_page.choose_passenger(4,2,1,1,1)
        result = self.main_page.choose_passenger(2,1,0,0,0)
        assert result in "3 Passenger"

    def test_06_origin(self):
        self.main_page.cookie_accept()
        result = self.main_page.choose_origin("Los Angeles")
        assert result == "Los Angeles"

    def test_07_destination(self):
        self.main_page.cookie_accept()
        result = self.main_page.choose_destination("Tel Aviv")
        assert result == "Tel Aviv"

    def test_08_departure_date(self):
        self.main_page.cookie_accept()
        result = self.main_page.choose_departure_date("2025-08-01")
        assert "1 Aug" in result

    def test_09_return_date(self):
        self.main_page.cookie_accept()
        result = self.main_page.choose_return_date("2025-08-01")
        assert "1 Aug" in result

    def test_10_both_dates(self):
        self.main_page.cookie_accept()
        result = self.main_page.choose_dates("2025-08-01", "2025-08-09",False)
        assert "1 Aug" in result and  "9 Aug" in result

    def test_11_both_dates_cancel(self):
        self.main_page.cookie_accept()
        result = self.main_page.choose_dates("2025-08-01", "2025-08-09", True)
        assert "Anytime" in result

    def test_12_order_first(self):
        self.main_page.cookie_accept()
        self.main_page.choose_class("firstclass")
        time.sleep(2)
        self.main_page.choose_passenger(3, 2, 0, 1, 1)
        time.sleep(2)
        self.main_page.choose_origin("New York")
        time.sleep(2)
        self.main_page.choose_destination("Tel Aviv")
        time.sleep(2)
        self.main_page.choose_dates("2025-08-01", "2025-08-09", False)
        time.sleep(2)
        self.main_page.click(self.main_page.SEARCH)
        time.sleep(2)
        self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        result = self.main_page.driver.title
        assert "New York" in result and "Tel Aviv" in result

    def test_13_order_economy(self):
        self.main_page.cookie_accept()
        self.main_page.choose_passenger(2, 1, 1, 1, 1)
        time.sleep(2)
        self.main_page.choose_origin("Los Angeles")
        time.sleep(2)
        self.main_page.choose_destination("Tel Aviv")
        time.sleep(2)
        self.main_page.choose_dates("2025-09-01", "2025-10-01", False)
        time.sleep(2)
        self.main_page.click(self.main_page.SEARCH)
        time.sleep(2)
        self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        result = self.main_page.driver.title
        assert "New York" in result and "Tel Aviv" in result

    def test_14_order_premium(self):
        self.main_page.cookie_accept()
        self.main_page.choose_class("premium")
        time.sleep(2)
        self.main_page.choose_passenger(1, 0, 0, 1, 1)
        time.sleep(2)
        self.main_page.choose_origin("New York")
        time.sleep(2)
        self.main_page.choose_destination("Tel Aviv")
        time.sleep(2)
        self.main_page.choose_dates("2025-08-15", "2025-08-20", False)
        time.sleep(2)
        self.main_page.click(self.main_page.SEARCH)
        time.sleep(2)
        self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        result = self.main_page.driver.title
        assert "New York" in result and "Tel Aviv" in result

    def test_15_order_business(self):
        self.main_page.cookie_accept()
        self.main_page.choose_class("buissness")
        time.sleep(2)
        self.main_page.choose_passenger(3, 2, 0, 1, 1)
        time.sleep(2)
        self.main_page.choose_origin("New York")
        time.sleep(2)
        self.main_page.choose_destination("Tel Aviv")
        time.sleep(2)
        self.main_page.choose_dates("2025-09-01", "2025-09-02", False)
        time.sleep(2)
        self.main_page.click(self.main_page.SEARCH)
        time.sleep(2)
        self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        result = self.main_page.driver.title
        assert "New York" in result and "Tel Aviv" in result

    def test_16_switch(self):
        self.main_page.cookie_accept()
        self.main_page.choose_origin("New York")
        time.sleep(2)
        self.main_page.choose_destination("Tel Aviv")
        time.sleep(2)
        self.main_page.click(self.main_page.SWITCH)
        time.sleep(2)
        place_elements = self.main_page.driver.find_elements(*self.main_page.PLACE)
        origin = place_elements[0].text
        destination = place_elements[1].text
        assert "Tel Aviv" in origin and "New York" in destination

    def test_17_multiple_cities(self):
        self.main_page.cookie_accept()
        self.main_page.choose_origin("New York", 0,False)
        time.sleep(2)
        self.main_page.choose_origin("London",0,False)
        time.sleep(2)
        self.main_page.choose_origin("Berlin",1,False)
        time.sleep(2)
        self.main_page.choose_destination("Tel Aviv", 0,False)
        time.sleep(2)
        self.main_page.choose_destination("Paris", 0,True)
        time.sleep(2)







