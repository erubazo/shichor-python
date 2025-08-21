import time
import allure
import pytest
from allure_commons.types import Severity

from pages.cookie_page import CookiePage
from tests.base_test import BaseTest


@pytest.mark.usefixtures("setup_driver_class")
@allure.severity(Severity.CRITICAL)
@allure.epic("Main Page Tests")
@allure.feature("Main Page functionality")
class TestClass(BaseTest):

    @allure.severity(Severity.NORMAL)
    @allure.description("Test to check cookie customization and retrieval")
    @allure.title("Cookie Customization Test")
    @allure.story("Cookie Management")
    def test_01_cookie_test(self):
        self.cookie_page.customize_cookies(False, True, True, True)
        time.sleep(2)
        cookie = self.cookie_page.get_cookie()
        assert cookie == "true"

    @allure.severity(Severity.NORMAL)
    @allure.story("Links Check")
    @allure.description("Test to check links on the main page")
    @allure.title("Links check Test")
    def test_02_links_check(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Check cars link on the main page"):
            cars = self.main_page.link_checker_diff(self.main_page.CARS, "Cars")
            print(cars)
        with allure.step("Check stay link on the main page"):
            stay = self.main_page.link_checker_diff(self.main_page.STAYS, "Stay")
            print(stay)
        with allure.step("Check magazine link on the main page"):
            magazine = self.main_page.link_checker_diff(self.main_page.MAGAZINE, "Magazine")
            print(magazine)
        with allure.step("Check travel hacks link on the main page"):
            hacks = self.main_page.link_checker_same(self.main_page.TRAVLE_HACKS, "Travel Hacks")
            print(hacks)
            self.main_page.driver.back()
        with allure.step("Check deals link on the main page"):
            deals = self.main_page.link_checker_same(self.main_page.DEALS, "Deals")
            print(deals)
            self.main_page.driver.back()
        with allure.step("Check help link on the main page"):
            help_btn = self.main_page.link_checker_diff(self.main_page.HELP, "Help")
            print(help_btn)
        result = all([cars, stay, magazine, hacks, deals, help_btn])
        assert result == True

    @allure.severity(Severity.NORMAL)
    @allure.story("trip ticket selection")
    @allure.description("Test to check trip ticket")
    @allure.title("trip ticket selection Test")
    def test_03_trip_ticket(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Select one-way trip"):
            self.main_page.choose_trip("oneway")
        with allure.step("Select return trip"):
            result = self.main_page.choose_trip("return")
            assert result == "Return"

    @allure.severity(Severity.CRITICAL)
    @allure.story("class ticket selection")
    @allure.description("Test to check class")
    @allure.title("class ticket selection Test")
    def test_04_class(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Select premium class"):
            self.main_page.choose_class("premium", True)
        with allure.step("Select business class"):
            self.main_page.choose_class("business")
        with allure.step("Select first class"):
            self.main_page.choose_class("firstclass")
        with allure.step("Select economy class"):
            result = self.main_page.choose_class("economy")
            assert result == "Economy"

    @allure.severity(Severity.CRITICAL)
    @allure.story("passengers ticket selection")
    @allure.description("Test to number of passengers")
    @allure.title("passengers ticket selection Test")
    def test_05_passengers(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Select 4 adults, 2 children, 1 infant, 1 senior, 1 youth"):
            self.main_page.choose_passenger(4, 2, 1, 1, 1)
        with allure.step("Select 2 adults, 1 child, 0 infant, 0 senior, 0 youth"):
            result = self.main_page.choose_passenger(2, 1, 0, 0, 0)
            assert result in "3 Passengers"


    @allure.severity(Severity.CRITICAL)
    @allure.story("origin selection")
    @allure.description("Test to choose origin")
    @allure.title("origin selection Test")
    def test_06_origin(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose origin"):
            result = self.main_page.choose_origin("Los Angeles")
            assert result == "Los Angeles"

    @allure.severity(Severity.CRITICAL)
    @allure.description("Test to choose destination")
    @allure.title("Destination selection Test")
    def test_07_destination(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose destination"):
            result = self.main_page.choose_destination("Tel Aviv")
            assert result == "Tel Aviv"

    @allure.severity(Severity.CRITICAL)
    @allure.story("departure date selection")
    @allure.description("Test to choose departure date")
    @allure.title("departure date selection Test")
    def test_08_departure_date(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose departure date"):
            result = self.main_page.choose_departure_date("2025-08-01")
            assert "1 Aug" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("return date selection")
    @allure.description("Test to choose return date")
    @allure.title("return date selection Test")
    def test_09_return_date(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose return date"):
            result = self.main_page.choose_return_date("2025-08-01")
            assert "1 Aug" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("departure and return dates selection")
    @allure.description("Test to choose departure and return dates")
    @allure.title("departure and return dates selection Test")
    def test_10_both_dates(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose departure and return dates"):
            result = self.main_page.choose_dates("2025-08-01", "2025-08-09", False)
            assert "1 Aug" in result and "9 Aug" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("cancel departure and return dates selection")
    @allure.description("Test to choose cancel departure and return dates")
    @allure.title("cancel departure and return dates selection Test")
    def test_11_both_dates_cancel(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose departure and return dates and cancel it"):
            result = self.main_page.choose_dates("2025-08-01", "2025-08-09", True)
            assert "Anytime" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("order first class ticket")
    @allure.description("Test to order first class ticket")
    @allure.title("Order first class ticket Test")
    def test_12_order_first(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose first class"):
            self.main_page.choose_class("firstclass")
            time.sleep(2)
        with  allure.step("Choose passengers"):
            self.main_page.choose_passenger(3, 2, 0, 1, 1)
            time.sleep(2)
        with allure.step("Choose origin"):
            self.main_page.choose_origin("New York")
            time.sleep(2)
        with allure.step("Choose destination"):
            self.main_page.choose_destination("Tel Aviv")
            time.sleep(2)
        with allure.step("Choose dates"):
            self.main_page.choose_dates("2025-08-01", "2025-08-09", False)
            time.sleep(2)
        with allure.step("Click search"):
            self.main_page.click(self.main_page.SEARCH)
            time.sleep(2)
        with allure.step("Switch to new window"):
            self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        with allure.step("Check result"):
            result = self.main_page.driver.title
            assert "New York" in result and "Tel Aviv" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("order economy ticket")
    @allure.description("Test to order economy ticket")
    @allure.title("economy ticket order Test")
    def test_13_order_economy(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose passengers"):
            self.main_page.choose_passenger(2, 1, 1, 1, 1)
            time.sleep(2)
        with allure.step("Choose origin"):
            self.main_page.choose_origin("Los Angeles")
            time.sleep(2)
        with allure.step("Choose destination"):
            self.main_page.choose_destination("Tel Aviv")
            time.sleep(2)
        with allure.step("Choose dates"):
            self.main_page.choose_dates("2025-09-01", "2025-10-01", False)
            time.sleep(2)
        with allure.step("Click search"):
            self.main_page.click(self.main_page.SEARCH)
            time.sleep(2)
        with allure.step("Switch to new window"):
            self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        with allure.step("Check result"):
            result = self.main_page.driver.title
            assert "New York" in result and "Tel Aviv" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("order premium ticket")
    @allure.description("test to order premium ticket")
    @allure.title("premium class ticket selection Test")
    def test_14_order_premium(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose premium class"):
            self.main_page.choose_class("premium")
            time.sleep(2)
        with allure.step("Choose passengers"):
            self.main_page.choose_passenger(1, 0, 0, 1, 1)
            time.sleep(2)
        with allure.step("Choose origin"):
            self.main_page.choose_origin("New York")
            time.sleep(2)
        with allure.step("Choose destination"):
            self.main_page.choose_destination("Tel Aviv")
            time.sleep(2)
        with allure.step("Choose dates"):
            self.main_page.choose_dates("2025-08-15", "2025-08-20", False)
            time.sleep(2)
        with allure.step("Click search"):
            self.main_page.click(self.main_page.SEARCH)
            time.sleep(2)
        with allure.step("Switch to new window"):
            self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        with allure.step("Check result"):
            result = self.main_page.driver.title
            assert "New York" in result and "Tel Aviv" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("order business class ticket")
    @allure.description("Test to order business class ticket")
    @allure.title("business class ticket selection Test")
    def test_15_order_business(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose business class"):
            self.main_page.choose_class("buissness")
            time.sleep(2)
        with allure.step("Choose passengers"):
            self.main_page.choose_passenger(3, 2, 0, 1, 1)
            time.sleep(2)
        with allure.step("Choose origin"):
            self.main_page.choose_origin("New York")
            time.sleep(2)
        with allure.step("Choose destination"):
            self.main_page.choose_destination("Tel Aviv")
            time.sleep(2)
        with allure.step("Choose dates"):
            self.main_page.choose_dates("2025-09-01", "2025-09-02", False)
            time.sleep(2)
        with allure.step("Click search"):
            self.main_page.click(self.main_page.SEARCH)
            time.sleep(2)
        with allure.step("Switch to new window"):
            self.main_page.driver.switch_to.window(self.main_page.driver.window_handles[1])
        with allure.step("Check result"):
            result = self.main_page.driver.title
            assert "New York" in result and "Tel Aviv" in result

    @allure.severity(Severity.CRITICAL)
    @allure.story("switch origin and destination")
    @allure.description("Test to check switch origin and destination")
    @allure.title("switching location selection Test")
    def test_16_switch(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose origin"):
            self.main_page.choose_origin("New York")
            time.sleep(2)
        with allure.step("Choose destination"):
            self.main_page.choose_destination("Tel Aviv")
            time.sleep(2)
        with allure.step("Switch origin and destination"):
            self.main_page.click(self.main_page.SWITCH)
            time.sleep(2)
            place_elements = self.main_page.driver.find_elements(*self.main_page.PLACE)
            origin = place_elements[0].text
            destination = place_elements[1].text
        with allure.step("Check origin and destination"):
            assert "Tel Aviv" in origin and "New York" in destination

    @allure.severity(Severity.CRITICAL)
    @allure.story("multiple cities selection")
    @allure.description("Test to select multiple cities")
    @allure.title("Multiple cities selection Test")
    def test_17_multiple_cities(self):
        with allure.step("Accept cookies if present"):
            CookiePage(self.main_page.driver).accept_if_present()
        with allure.step("Choose multiple origin cities"):
            self.main_page.choose_origin("New York", 0, False)
            time.sleep(2)
            self.main_page.choose_origin("London", 0, False)
            time.sleep(2)
        with allure.step("Choose multiple destination cities"):
            self.main_page.choose_destination("Tel Aviv", 0, False)
            time.sleep(2)
            self.main_page.choose_destination("Paris", 0, False)
            time.sleep(2)
