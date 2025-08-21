import time
import datetime

import allure
import requests  # Add this import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.main_page import MainPage


class SignInPage(BasePage):
    SIGN_UP_BUTTON = (By.CSS_SELECTOR, r'#react-view > div.orbit-modal-body.z-overlay.font-base.fixed.inset-0.box-border.size-full.overflow-x-hidden.outline-none.bg-\[black\]\/50.lm\:overflow-y-auto.lm\:p-1000.lm\:bg-\[black\]\/50 > div > div > div.flex.items-center.flex-col.pt-\[32px\] > div.orbit-box.font-base.box-border.flex.items-center > button')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-test="MagicLogin-Email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, '[data-test="MagicLogin-Continue"]')
    PASS = (By.CSS_SELECTOR, r'#react-view > div.orbit-modal-body.z-overlay.font-base.fixed.inset-0.box-border.size-full.overflow-x-hidden.outline-none.bg-\[black\]\/50.lm\:overflow-y-auto.lm\:p-1000.lm\:bg-\[black\]\/50 > div > div > section > form > div.group.w-full.flex.items-center.justify-center.has-\[\:disabled\]\:opacity-30.mb-\[32px\] > div:nth-child(2) > input')
    ERROR = (By.CSS_SELECTOR, r'#react-view > div.orbit-modal-body.z-overlay.font-base.fixed.inset-0.box-border.size-full.overflow-x-hidden.outline-none.bg-\[black\]\/50.lm\:overflow-y-auto.lm\:p-1000.lm\:bg-\[black\]\/50 > div > div > section > form > p.orbit-text.font-base.text-small.leading-small.font-normal.text-critical-foreground.\[\&_a\:not\(\.orbit-text-link\)\]\:text-link-critical-foreground.hover\:\[\&_a\:not\(\.orbit-text-link\)\]\:text-link-critical-foreground-hover.active\:\[\&_a\:not\(\.orbit-text-link\)\]\:text-link-critical-foreground-active.text-start.mb-400.m-0.\[\&_a\:not\(\.orbit-text-link\)\]\:font-medium.\[\&_a\:not\(\.orbit-text-link\)\]\:underline.hover\:\[\&_a\:not\(\.orbit-text-link\)\]\:no-underline.active\:\[\&_a\:not\(\.orbit-text-link\)\]\:no-underline.hover\:\[\&_a\:not\(\.orbit-text-link\)\]\:outline-none.active\:\[\&_a\:not\(\.orbit-text-link\)\]\:outline-none')
    INCORRECT_EMAIL = (By.CSS_SELECTOR, '[data-test="MagicLogin-IncorrectEmail"]')
    BOOKING_NUMBER = (By.CSS_SELECTOR, '[data-test="MagicLogin-BookingId"]')
    DAY = (By.CSS_SELECTOR, '[data-test="MagicLogin-DateInput-Date"]')
    MONTH = (By.CSS_SELECTOR, '[data-test="MagicLogin-DateInput-Month"]')
    YEAR = (By.CSS_SELECTOR, '[data-test="MagicLogin-DateInput-Year"]')
    IATA = (By.CSS_SELECTOR, '[data-test="MagicLogin-IATAPickerInput"]')
    AIRPORT = (By.CSS_SELECTOR, 'div.pe-300.flex.w-full.flex-col.justify-center')
    SUMBIT = (By.CSS_SELECTOR, '[data-test="MagicLogin-GetSingleBookingSubmit"]')
    ERROR2 = (By.CSS_SELECTOR, r'#react-view > div.orbit-modal-body.z-overlay.font-base.fixed.inset-0.box-border.size-full.overflow-x-hidden.outline-none.bg-\[black\]\/50.lm\:overflow-y-auto.lm\:p-1000.lm\:bg-\[black\]\/50 > div > div > section > form > div > div.orbit-stack.items-start.content-start.flex-nowrap.grow.shrink-0.justify-start.flex-col.flex.gap-400.w-full > div.orbit-alert.rounded-150.text-ink-dark.font-base.text-normal.p-300.relative.box-border.flex.w-full.border.border-t-\[3px\].leading-normal.lm\:border-s-\[3px\].lm\:border-t.tb\:rounded-100.bg-red-light.border-red-light-hover.lm\:border-t-red-light-hover.border-t-red-normal.lm\:border-s-red-normal > div.flex.flex-1.flex-col.items-center > div > p')
    ERROR3 = (By.CSS_SELECTOR, r'#react-view > div.orbit-modal-body.z-overlay.font-base.fixed.inset-0.box-border.size-full.overflow-x-hidden.outline-none.bg-\[black\]\/50.lm\:overflow-y-auto.lm\:p-1000.lm\:bg-\[black\]\/50 > div > div > section > form > div.orbit-alert.rounded-150.text-ink-dark.font-base.text-normal.p-300.relative.box-border.flex.w-full.border.border-t-\[3px\].leading-normal.lm\:border-s-\[3px\].lm\:border-t.tb\:rounded-100.bg-red-light.border-red-light-hover.lm\:border-t-red-light-hover.border-t-red-normal.lm\:border-s-red-normal > div.flex.flex-1.flex-col.items-center > div')


    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_element(self, locator, timeout=10, condition="visible"):
        """
        Wait for an element to be in the specified condition

        Args:
            locator: Tuple with (By.*, selector_string)
            timeout: Maximum time to wait in seconds
            condition: 'visible', 'clickable', or 'present'

        Returns:
            The WebElement once found
        """
        wait = WebDriverWait(self.driver, timeout)

        if condition == "visible":
            return wait.until(EC.visibility_of_element_located(locator))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable(locator))
        elif condition == "present":
            return wait.until(EC.presence_of_element_located(locator))
        else:
            raise ValueError(f"Unsupported condition: {condition}")

    @property
    def main_page(self):
        from pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step("Sign up with incorrect email: {email}")
    def incorrect_email(self,email)-> str:
        self.main_page.click(self.main_page.ACCEPT)
        self.wait_for_element(self.main_page.SIGN_IN, condition="clickable")
        self.click(self.main_page.SIGN_IN)
        self.wait_for_element(self.SIGN_UP_BUTTON, condition="clickable")
        self.click(self.SIGN_UP_BUTTON)
        self.wait_for_element(self.EMAIL_INPUT, condition="visible")
        self.click(self.EMAIL_INPUT)
        self.fill_text(self.EMAIL_INPUT, email)
        self.click(self.CONTINUE_BTN)

        # Wait for password field to appear
        self.wait_for_element(self.PASS, condition="visible")
        self.fill_text(self.PASS, "12345678")

        # Wait for error message to appear
        error_element = self.wait_for_element(self.ERROR3, condition="visible")
        gettext = error_element.text
        print(gettext)
        return gettext

    @allure.step("Sign up with wrong email format: {email}")
    def wrong_format(self,email)-> str:
        self.main_page.click(self.main_page.ACCEPT)
        self.wait_for_element(self.main_page.SIGN_IN, condition="clickable")
        self.click(self.main_page.SIGN_IN)
        self.wait_for_element(self.SIGN_UP_BUTTON, condition="clickable")
        self.click(self.SIGN_UP_BUTTON)
        self.wait_for_element(self.EMAIL_INPUT, condition="visible")
        self.click(self.EMAIL_INPUT)
        self.fill_text(self.EMAIL_INPUT, email)
        self.click(self.CONTINUE_BTN)

        # Wait for error message to appear
        error_element = self.wait_for_element(self.ERROR, condition="visible")
        gettext = error_element.text
        print(gettext)
        return gettext

    @allure.step("Sign in with incorrect booking details: email: {email}, booking number: {booking_num}, day: {day}, month: {month}, year: {year}, iata: {iata}")
    def incorrect_booking(self,email, booking_num:str,day:str, month:str, year:str,iata:str):
        self.main_page.click(self.main_page.ACCEPT)
        self.wait_for_element(self.main_page.SIGN_IN, condition="clickable")
        self.click(self.main_page.SIGN_IN)
        self.wait_for_element(self.INCORRECT_EMAIL, condition="clickable")
        self.click(self.INCORRECT_EMAIL)
        self.wait_for_element(self.BOOKING_NUMBER, condition="visible")
        self.click(self.BOOKING_NUMBER)
        self.fill_text(self.BOOKING_NUMBER,booking_num)

        self.wait_for_element(self.EMAIL_INPUT, condition="visible")
        self.click(self.EMAIL_INPUT)
        self.fill_text(self.EMAIL_INPUT, email)

        self.wait_for_element(self.DAY, condition="visible")
        self.click(self.DAY)
        self.fill_text(self.DAY, day)

        self.wait_for_element(self.MONTH, condition="visible")
        self.click(self.MONTH)
        self.select(self.MONTH, month, by_visible_text=False)

        self.wait_for_element(self.YEAR, condition="visible")
        self.click(self.YEAR)
        self.fill_text(self.YEAR, year)

        self.wait_for_element(self.IATA, condition="visible")
        self.click(self.IATA)
        self.fill_text(self.IATA, iata)

        self.wait_for_element(self.AIRPORT, condition="clickable")
        self.click(self.AIRPORT)

        self.wait_for_element(self.SUMBIT, condition="clickable")
        self.click(self.SUMBIT)

        # Wait for error message to appear
        error_element = self.wait_for_element(self.ERROR2, condition="visible")
        result = error_element.text
        return result
