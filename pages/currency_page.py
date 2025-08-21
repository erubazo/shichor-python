import time
import datetime

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.cookie_page import CookiePage


class CurrencyPage(BasePage):
    CURRENCY_SELECTOR = (By.CSS_SELECTOR,'[data-test="currency-selector"]')
    CURRENCY_SELECTOR_OPTIONS = (By.CSS_SELECTOR, '[data-test="currency-tile"]')
    REGION_SELECTOR = (By.CSS_SELECTOR, '[data-test="region-tile"]')
    LANGUAGE_SELECTOR = (By.CSS_SELECTOR, '[data-test="language-selector"]')

    def __init__(self, driver):
        super().__init__(driver)

    @property
    def main_page(self):
        from pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step("Select currency: {coin} from the dropdown")
    def select_currency(self, coin: str):
        self.main_page.click(self.main_page.CURRENCY)
        time.sleep(1)
        self.click(self.CURRENCY_SELECTOR)
        currencies = self.driver.find_elements(*self.CURRENCY_SELECTOR_OPTIONS)
        for currency in currencies:
            currency_text = currency.text.lower()
            if coin.lower() in currency_text:
                print(f'Selecting currency: {currency_text}')
                currency.click()
                time.sleep(1)
                return
        raise ValueError(f"Currency '{coin}' not found in the dropdown options.")

    @allure.step("Select country: {country} and language: {lan} from the dropdown")
    def select_region(self, country: str, lan: str = "English"):
        self.main_page.click(self.main_page.CURRENCY)
        time.sleep(1)
        countries = self.driver.find_elements(*self.REGION_SELECTOR)
        for country_option in countries:
            country_text = country_option.text.lower()
            if country.lower() in country_text:
                print(f'Selecting region: {country_text}')
                # scroll_to_element_iterate expects a list, so wrap the element
                self.scroll_to_element_iterate([country_option])
                country_option.click()
                languges = self.driver.find_elements(*self.LANGUAGE_SELECTOR)
                for language in languges:
                    language_text = language.text.lower()
                    if lan.lower() in language_text:
                        print(f'Selecting language: {language_text}')
                        self.scroll_to_element_iterate([language])
                        language.click()
                        time.sleep(5)
                        return  # Select and exit immediately if found
                return
