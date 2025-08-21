import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.main_page import MainPage


class CookiePage(BasePage):
    # raw strings for selectors that contain backslashes/colons/brackets
    PERFORMENCE_ENABLED = (By.CSS_SELECTOR, r'#cookie_consent > div > div > div > section > div.orbit-stack.mb-600.block.space-y-400.space-x-none.w-full > div:nth-child(2) > div.orbit-stack.items-start.content-start.flex-nowrap.grow.shrink.justify-start.flex-col.flex.gap-400.w-full > div.orbit-stack.mb-600.items-start.content-start.flex-nowrap.grow.shrink-0.justify-start.flex-row.inline-flex.gap-400 > label:nth-child(1)')
    ADVERTISMENT_ENABLED = (By.CSS_SELECTOR, r'#cookie_consent > div > div > div > section > div.orbit-stack.mb-600.block.space-y-400.space-x-none.w-full > div:nth-child(3) > div.orbit-stack.items-start.content-start.flex-nowrap.grow.shrink.justify-start.flex-col.flex.gap-400.w-full > div.orbit-stack.mb-600.items-start.content-start.flex-nowrap.grow.shrink-0.justify-start.flex-row.inline-flex.gap-400 > label:nth-child(1) > div.orbit-radio-icon-container.relative.box-border.flex.flex-none.items-center.justify-center.size-icon-medium.rounded-full.duration-fast.scale-100.transition-all.ease-in-out.border-solid.border.active\:scale-95')
    SAVE_BTN = (By.CSS_SELECTOR, r"#cookie_consent > div > div > div > div.orbit-modal-footer.z-overlay.bg-white-normal.px-400.pb-400.box-border.flex.w-full.pt-0.duration-fast.transition-shadow.ease-in-out.sm\:max-lm\:\[\&_\.orbit-button-primitive\]\:h-form-box-normal.sm\:max-lm\:\[\&_\.orbit-button-primitive\]\:text-button-normal.lm\:rounded-b-modal.lm\:justify-end.\[\&_\.orbit-modal-footer-child\:last-of-type\]\:p-0 > div > button.space-x-200.rtl\:space-x-reverse.h-form-box-normal.text-normal.bg-button-secondary-background.hover\:bg-button-secondary-background-hover.active\:bg-button-secondary-background-active.disabled\:bg-button-secondary-background.focus\:bg-button-secondary-background-focus.text-button-secondary-foreground.focus\:text-button-secondary-foreground-focus.active\:text-button-secondary-foreground-active.hover\:text-button-secondary-foreground-hover.disabled\:text-button-secondary-foreground.active\:shadow-button-active-pale.px-button-padding-md.orbit-button-primitive.font-base.duration-fast.group.relative.max-w-full.select-none.items-center.justify-center.border-none.text-center.leading-none.transition-all.\*\:align-middle.\[\&_\.orbit-loading-spinner\]\:stroke-current.w-full.flex-auto.rounded-150.tb\:rounded-100.cursor-pointer.hover\:no-underline.focus\:no-underline.active\:no-underline.flex.font-medium")
    ACCEPT_BTN = (By.CSS_SELECTOR, '[data-test="CookiesPopup-Accept"]')

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(driver, 10)

    @property
    def main_page(self):
        # keep this only for the "Customize" button, which is defined on MainPage
        return MainPage(self.driver)

    def _click_if_clickable(self, locator, timeout=4) -> bool:
        try:
            self._wait.until(EC.element_to_be_clickable(locator)).click()
            return True
        except Exception:
            return False

    @allure.step("Accept cookies if banner is present")
    def accept_if_present(self):
        # try the visible Accept button on the cookie modal
        self._click_if_clickable(self.ACCEPT_BTN, timeout=4)

    @allure.step("Click radio if visible & enabled")
    def click_radio_if_visible(self, locator):
        try:
            elem = self._wait.until(EC.presence_of_element_located(locator))
            if elem.is_displayed() and elem.is_enabled():
                elem.click()
        except Exception as e:
            print(f"Radio element {locator} not clickable: {e}")

    @allure.step("Customize cookies based on user preferences")
    def customize_cookies(self, accept: bool, performence: bool, marketing: bool, save: bool):
        # If accept=True -> click the cookie Accept button here (NOT from MainPage)
        if accept:
            if not self._click_if_clickable(self.ACCEPT_BTN, timeout=6):
                # banner not present — treat as already accepted
                return
            return

        # Otherwise, open the Customize flow (button resides on the page under MainPage)
        self._click_if_clickable(self.main_page.CUSTOMIZE, timeout=6)

        if performence:
            self.scroll_down(200)
            self.click_radio_if_visible(self.PERFORMENCE_ENABLED)

        if marketing:
            self.scroll_down(900)
            self.click_radio_if_visible(self.ADVERTISMENT_ENABLED)

        if save:
            self._click_if_clickable(self.SAVE_BTN, timeout=6)
        else:
            # fall back to Accept if user chose not to save granular changes
            self._click_if_clickable(self.ACCEPT_BTN, timeout=6)

    def get_cookie(self) -> str:
        cookie = self.driver.get_cookie("__kwc_agreed")
        return str(cookie["value"]) if cookie and "value" in cookie else ""
