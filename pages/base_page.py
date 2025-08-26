import time
from typing import Tuple, List, Optional

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)


Locator = Tuple[str, str]


class BasePage:
    """Wrapper for Selenium operations with explicit waits and CI-friendly behavior."""

    def __init__(self, driver: WebDriver, default_timeout: int = 15, poll_frequency: float = 0.2):
        self.driver = driver
        self.default_timeout = default_timeout
        self.poll_frequency = poll_frequency

    # ---------------------------
    # Wait helpers
    # ---------------------------
    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.default_timeout, poll_frequency=self.poll_frequency)

    def wait_for_present(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_all_present(self, locator: Locator, timeout: Optional[int] = None) -> List[WebElement]:
        return self._wait(timeout).until(EC.presence_of_all_elements_located(locator))

    def wait_for_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.invisibility_of_element_located(locator))

    def wait_for_text(self, locator: Locator, text: str, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_page_ready(self, timeout: Optional[int] = None) -> None:
        """Wait until document.readyState is 'complete'."""
        self._wait(timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ---------------------------
    # Element utilities
    # ---------------------------
    def highlight_element(self, locator_or_element, color: str):
        """
        Highlights (briefly) a web element by changing its background color.
        Accepts either a locator tuple or a WebElement.
        """
        if hasattr(locator_or_element, "is_displayed"):
            element: WebElement = locator_or_element
        else:
            element = self.wait_for_present(locator_or_element)

        original_style = element.get_attribute("style") or ""
        new_style = f"background-color: {color}; {original_style}"

        self.driver.execute_script(
            """
            var el = arguments[0], newStyle = arguments[1];
            el.setAttribute('style', newStyle);
            """,
            element,
            new_style,
        )
        # quickly revert without a hard sleep
        self.driver.execute_script(
            """
            var el = arguments[0], originalStyle = arguments[1];
            setTimeout(function(){ el.setAttribute('style', originalStyle); }, 300);
            """,
            element,
            original_style,
        )

    def _safe_click(self, element: WebElement, locator_for_debug: Optional[Locator] = None):
        """
        Click with scroll-into-view and JS fallback for CI flakiness.
        """
        try:
            element.click()
            return
        except (ElementClickInterceptedException, ElementNotInteractableException):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
                element.click()
                return
            except Exception:
                # Final JS fallback
                self.driver.execute_script("arguments[0].click();", element)
                return

    # ---------------------------
    # Actions with waits
    # ---------------------------
    def fill_text(self, locator: Locator, text: str, timeout: Optional[int] = None):
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Yellow")
        # handle potential stale updates
        for _ in range(2):
            try:
                el.clear()
                el.send_keys(text)
                return
            except StaleElementReferenceException:
                el = self.wait_for_visible(locator, timeout)

    def scroll_down(self, amount: int):
        # No sleep; let the browser do the work
        ActionChains(self.driver).scroll_by_amount(0, amount).perform()

    def click(self, locator: Locator, timeout: Optional[int] = None):
        el = self.wait_for_clickable(locator, timeout)
        self.highlight_element(el, "Yellow")
        self._safe_click(el, locator_for_debug=locator)

    def click_by_offset(self, x_offset: int, y_offset: int, timeout: Optional[int] = None):
        # Wait until body is present to avoid offset on blank page
        self.wait_for_present((By.TAG_NAME, "body"), timeout)
        ActionChains(self.driver).move_by_offset(x_offset, y_offset).click().perform()

    def scroll_to_element(self, locator: Locator, timeout: Optional[int] = None):
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Yellow")
        ActionChains(self.driver).move_to_element(el).perform()

    def scroll_to_element_iterate(self, items, timeout: Optional[int] = None):
        """
        Scrolls to each element in a list, or finds elements by locator and scrolls to each.
        :param items: Either a locator tuple or a list of WebElements.
        """
        if isinstance(items, tuple):
            elements = self.wait_for_all_present(items, timeout)
        else:
            elements = items

        for el in elements:
            try:
                self._wait(timeout).until(lambda d: el.is_displayed())
            except StaleElementReferenceException:
                # If a provided list goes stale, skip gracefully
                continue
            self.highlight_element(el, "Yellow")
            ActionChains(self.driver).move_to_element(el).perform()

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Orange")
        return el.text

    def click_and_hold(self, locator: Locator, timeout: Optional[int] = None):
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Yellow")
        ActionChains(self.driver).click_and_hold(el).perform()

    def select(self, locator: Locator, value: str, by_visible_text: bool = False, timeout: Optional[int] = None):
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Yellow")
        sel = Select(el)
        if by_visible_text:
            sel.select_by_visible_text(value)
        else:
            sel.select_by_value(value)

    def get_value(self, locator: Locator, timeout: Optional[int] = None) -> Optional[str]:
        try:
            el = self.wait_for_present(locator, timeout)
            value = el.get_attribute("value")
            print(f"Value of element {locator}: {value}")
            return value
        except TimeoutException as e:
            print(f"Timeout getting value from {locator}: {e}")
            return None

    # ---------------------------
    # Navigation helpers useful in CI
    # ---------------------------
    def open(self, url: str, wait_ready: bool = True, timeout: Optional[int] = None):
        self.driver.get(url)
        if wait_ready:
            self.wait_for_page_ready(timeout)

    def wait_url_contains(self, fragment: str, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.url_contains(fragment))

    def wait_url_to_be(self, url: str, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.url_to_be(url))
