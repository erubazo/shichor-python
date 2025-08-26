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
    """Wrapper for Selenium operations with explicit, stable & clickable waits (CI-friendly)."""

    def __init__(self, driver: WebDriver, default_timeout: int = 15, poll_frequency: float = 0.2):
        self.driver = driver
        self.default_timeout = default_timeout
        self.poll_frequency = poll_frequency

    # ---------------------------
    # Core wait
    # ---------------------------
    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.default_timeout, poll_frequency=self.poll_frequency)

    # ---------------------------
    # Stable & clickable waits
    # ---------------------------
    def _wait_stable_box(self, element: WebElement, frames: int = 3, interval: float = 0.08) -> bool:
        """
        Wait until the element's bounding box stops moving/resizing for N consecutive checks.
        Helps with CSS transitions/animations in CI.
        """
        last = None
        stable = 0
        checks = max(frames * 10, 10)  # upper bound failsafe
        for _ in range(checks):
            try:
                rect = self.driver.execute_script("""
                    const r = arguments[0].getBoundingClientRect();
                    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)];
                """, element)
            except StaleElementReferenceException:
                stable = 0
                time.sleep(interval)
                continue

            if rect == last:
                stable += 1
                if stable >= frames:
                    return True
            else:
                stable = 0
            last = rect
            time.sleep(interval)
        return False  # not stable, but we tried

    def _not_obscured(self, element: WebElement) -> bool:
        """
        Check that the element is not covered by another element at its center point.
        """
        try:
            cx, cy = self.driver.execute_script("""
                const r = arguments[0].getBoundingClientRect();
                return [Math.floor(r.left + r.width/2), Math.floor(r.top + r.height/2)];
            """, element)
            top_el = self.driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", cx, cy)
            if top_el is None:
                return True
            # allow descendants (e.g., clicking a <span> inside the button)
            return top_el is element or element.contains(top_el)
        except Exception:
            return True  # if check fails, don't block

    def wait_for_clickable_stable(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """
        1) visible, 2) clickable, 3) scrolled to center, 4) stable box, 5) not obscured.
        Returns the element ready for safe clicking/typing.
        """
        wait = self._wait(timeout)
        el = wait.until(EC.visibility_of_element_located(locator))
        el = wait.until(EC.element_to_be_clickable(locator))

        # Center it (avoid sticky headers/footers)
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", el
            )
        except StaleElementReferenceException:
            el = wait.until(EC.visibility_of_element_located(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", el
            )

        # Wait for stability (best-effort)
        self._wait_stable_box(el)

        # Ensure not covered; if covered briefly, re-wait clickable once
        if not self._not_obscured(el):
            el = wait.until(EC.element_to_be_clickable(locator))
            self._wait_stable_box(el)

        return el

    def wait_for_present(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        el = self._wait(timeout).until(EC.visibility_of_element_located(locator))
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", el
            )
            self._wait_stable_box(el)
        except Exception:
            pass
        return el

    def wait_for_all_present(self, locator: Locator, timeout: Optional[int] = None) -> List[WebElement]:
        return self._wait(timeout).until(EC.presence_of_all_elements_located(locator))

    def wait_for_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.invisibility_of_element_located(locator))

    def wait_for_text(self, locator: Locator, text: str, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_page_ready(self, timeout: Optional[int] = None) -> None:
        self._wait(timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ---------------------------
    # Element utilities
    # ---------------------------
    def highlight_element(self, locator_or_element, color: str):
        if hasattr(locator_or_element, "is_displayed"):
            element: WebElement = locator_or_element
        else:
            element = self.wait_for_present(locator_or_element)

        original_style = element.get_attribute("style") or ""
        new_style = f"background-color: {color}; {original_style}"

        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            new_style,
        )
        self.driver.execute_script(
            "var el=arguments[0], s=arguments[1]; setTimeout(function(){ el.setAttribute('style', s); }, 300);",
            element,
            original_style,
        )

    def _safe_click(self, element: WebElement):
        """
        Click with JS fallback for CI flakiness. Assumes element is stable & unobscured.
        """
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                raise

    # ---------------------------
    # Actions with stable waits
    # ---------------------------
    def fill_text(self, locator: Locator, text: str, timeout: Optional[int] = None):
        el = self.wait_for_clickable_stable(locator, timeout)
        self.highlight_element(el, "Yellow")
        for _ in range(2):  # handle one stale refresh
            try:
                el.clear()
                el.send_keys(text)
                return
            except StaleElementReferenceException:
                el = self.wait_for_clickable_stable(locator, timeout)

    def scroll_down(self, amount: int):
        ActionChains(self.driver).scroll_by_amount(0, amount).perform()

    def click(self, locator: Locator, timeout: Optional[int] = None):
        el = self.wait_for_clickable_stable(locator, timeout)
        self.highlight_element(el, "Yellow")
        self._safe_click(el)

    def click_by_offset(self, x_offset: int, y_offset: int, timeout: Optional[int] = None):
        self.wait_for_present((By.TAG_NAME, "body"), timeout)
        ActionChains(self.driver).move_by_offset(x_offset, y_offset).click().perform()

    def scroll_to_element(self, locator: Locator, timeout: Optional[int] = None):
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Yellow")
        ActionChains(self.driver).move_to_element(el).perform()

    def scroll_to_element_iterate(self, items, timeout: Optional[int] = None):
        if isinstance(items, tuple):
            elements = self.wait_for_all_present(items, timeout)
        else:
            elements = items

        for el in elements:
            try:
                # wait until displayed and stable
                self._wait(timeout).until(lambda d: el.is_displayed())
                self._wait_stable_box(el)
            except StaleElementReferenceException:
                continue
            self.highlight_element(el, "Yellow")
            ActionChains(self.driver).move_to_element(el).perform()

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        el = self.wait_for_visible(locator, timeout)
        self.highlight_element(el, "Orange")
        return el.text

    def click_and_hold(self, locator: Locator, timeout: Optional[int] = None):
        el = self.wait_for_clickable_stable(locator, timeout)
        self.highlight_element(el, "Yellow")
        ActionChains(self.driver).click_and_hold(el).perform()

    def select(self, locator: Locator, value: str, by_visible_text: bool = False, timeout: Optional[int] = None):
        el = self.wait_for_clickable_stable(locator, timeout)
        self.highlight_element(el, "Yellow")
        sel = Select(el)
        if by_visible_text:
            sel.select_by_visible_text(value)
        else:
            sel.select_by_value(value)

    def get_value(self, locator: Locator, timeout: Optional[int] = None) -> Optional[str]:
        try:
            el = self.wait_for_visible(locator, timeout)
            return el.get_attribute("value")
        except TimeoutException as e:
            print(f"Timeout getting value from {locator}: {e}")
            return None

    # ---------------------------
    # Navigation helpers
    # ---------------------------
    def open(self, url: str, wait_ready: bool = True, timeout: Optional[int] = None):
        self.driver.get(url)
        if wait_ready:
            self.wait_for_page_ready(timeout)

    def wait_url_contains(self, fragment: str, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.url_contains(fragment))

    def wait_url_to_be(self, url: str, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(EC.url_to_be(url))
