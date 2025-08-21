import time

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.main_page import MainPage

class CookiePage(BasePage):
    PERFORMENCE_ENABLED = (By.CSS_SELECTOR, r'#cookie_consent > div > div > div > section > div.orbit-stack.mb-600.block.space-y-400.space-x-none.w-full > div:nth-child(2) > div.orbit-stack.items-start.content-start.flex-nowrap.grow.shrink.justify-start.flex-col.flex.gap-400.w-full > div.orbit-stack.mb-600.items-start.content-start.flex-nowrap.grow.shrink-0.justify-start.flex-row.inline-flex.gap-400 > label:nth-child(1)')
    ADVERTISMENT_ENABLED = (By.CSS_SELECTOR, r'#cookie_consent > div > div > div > section > div.orbit-stack.mb-600.block.space-y-400.space-x-none.w-full > div:nth-child(3) > div.orbit-stack.items-start.content-start.flex-nowrap.grow.shrink.justify-start.flex-col.flex.gap-400.w-full > div.orbit-stack.mb-600.items-start.content-start.flex-nowrap.grow.shrink-0.justify-start.flex-row.inline-flex.gap-400 > label:nth-child(1) > div.orbit-radio-icon-container.relative.box-border.flex.flex-none.items-center.justify-center.size-icon-medium.rounded-full.duration-fast.scale-100.transition-all.ease-in-out.border-solid.border.active\:scale-95')
    SAVE_BTN = (By.CSS_SELECTOR, r"#cookie_consent > div > div > div > div.orbit-modal-footer.z-overlay.bg-white-normal.px-400.pb-400.box-border.flex.w-full.pt-0.duration-fast.transition-shadow.ease-in-out.sm\:max-lm\:\[\&_\.orbit-button-primitive\]\:h-form-box-normal.sm\:max-lm\:\[\&_\.orbit-button-primitive\]\:text-button-normal.lm\:rounded-b-modal.lm\:justify-end.\[\&_\.orbit-modal-footer-child\:last-of-type\]\:p-0 > div > button.space-x-200.rtl\:space-x-reverse.h-form-box-normal.text-normal.bg-button-secondary-background.hover\:bg-button-secondary-background-hover.active\:bg-button-secondary-background-active.disabled\:bg-button-secondary-background.focus\:bg-button-secondary-background-focus.text-button-secondary-foreground.focus\:text-button-secondary-foreground-focus.active\:text-button-secondary-foreground-active.hover\:text-button-secondary-foreground-hover.disabled\:text-button-secondary-foreground.active\:shadow-button-active-pale.px-button-padding-md.orbit-button-primitive.font-base.duration-fast.group.relative.max-w-full.select-none.items-center.justify-center.border-none.text-center.leading-none.transition-all.\*\:align-middle.\[\&_\.orbit-loading-spinner\]\:stroke-current.w-full.flex-auto.rounded-150.tb\:rounded-100.cursor-pointer.hover\:no-underline.focus\:no-underline.active\:no-underline.flex.font-medium")
    ACCEPT_BTN = (By.CSS_SELECTOR, r"#cookie_consent > div > div > div > div.orbit-modal-footer.z-overlay.bg-white-normal.px-400.pb-400.box-border.flex.w-full.pt-0.duration-fast.transition-shadow.ease-in-out.sm\:max-lm\:\[\&_\.orbit-button-primitive\]\:h-form-box-normal.sm\:max-lm\:\[\&_\.orbit-button-primitive\]\:text-button-normal.lm\:rounded-b-modal.lm\:justify-end.\[\&_\.orbit-modal-footer-child\:last-of-type\]\:p-0 > div > button.space-x-200.rtl\:space-x-reverse.h-form-box-normal.text-normal.bg-button-primary-background.hover\:bg-button-primary-background-hover.active\:bg-button-primary-background-active.disabled\:bg-button-primary-background.focus\:bg-button-primary-background-focus.text-button-primary-foreground.focus\:text-button-primary-foreground-focus.active\:text-button-primary-foreground-active.hover\:text-button-primary-foreground-hover.disabled\:text-button-primary-foreground.active\:shadow-button-active.px-button-padding-md.orbit-button-primitive.font-base.duration-fast.group.relative.max-w-full.select-none.items-center.justify-center.border-none.text-center.leading-none.transition-all.\*\:align-middle.\[\&_\.orbit-loading-spinner\]\:stroke-current.w-full.flex-auto.rounded-150.tb\:rounded-100.cursor-pointer.hover\:no-underline.focus\:no-underline.active\:no-underline.flex.font-medium")

    def __init__(self, driver):
        super().__init__(driver)

    @property
    def main_page(self):
        from pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step("Click on an element if it is displayed and enabled")
    def click_radio_if_visible(self, locator):
        try:
            elem = self.driver.find_element(*locator)
            if elem.is_displayed() and elem.is_enabled():
                elem.click()
            else:
                print(f"Radio element {locator} not displayed or not enabled.")
        except Exception as e:
            print(f"Radio element {locator} not found: {e}")

    @allure.step("Customize cookies based on user preferences")
    def customize_cookies(self, accept: bool, performence: bool, marketing: bool, save: bool):
        main_page= MainPage(self.driver)
        time.sleep(3)
        if accept:
            self.click(main_page.ACCEPT)
        else:
            self.click(main_page.CUSTOMIZE)
            time.sleep(3)
            if performence:
                self.scroll_down(200)
                self.click_radio_if_visible(self.PERFORMENCE_ENABLED)
            if marketing:
                self.scroll_down(900)
                self.click_radio_if_visible(self.ADVERTISMENT_ENABLED)
            if save:
                self.click(self.SAVE_BTN)
            else:
                self.click(self.ACCEPT_BTN)


    def get_cookie(self) -> str:
        cookie = self.driver.get_cookie("__kwc_agreed")
        # Always return the cookie value as a string, even if it's None
        return str(cookie["value"]) if cookie and "value" in cookie else ""
