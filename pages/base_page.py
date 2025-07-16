import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select


class BasePage:
    """ Wrapper for selenium operations """

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def highlight_element(self, driver, locator_or_element, color: str):
        """
        Highlights (briefly) a web element by changing its background color.
        Accepts either a locator tuple or a WebElement.

        :param driver: The Selenium WebDriver instance.
        :param locator_or_element: The locator for the element to be highlighted, or the element itself.
        :param color: The color to highlight the element with (e.g., 'red', 'green').
        """
        if hasattr(locator_or_element, "is_displayed"):
            # It's a WebElement
            element = locator_or_element
        else:
            # It's a locator tuple
            element = self.driver.find_element(*locator_or_element)
        original_style = element.get_attribute("style")
        new_style = f"background-color: {color}; {original_style}"
        self.driver.execute_script("""
                        var element = arguments[0];
                        var new_style = arguments[1];
                        setTimeout(function() {
                            element.setAttribute('style', new_style);
                        }, 0);
                    """, element, new_style)
        self.driver.execute_script("""
                var element = arguments[0];
                var originalStyle = arguments[1];
                setTimeout(function() {
                    element.setAttribute('style', originalStyle);
                }, 300);
            """, element, original_style)

    def fill_text(self, locator, text):
        self.highlight_element(self.driver, locator, "Yellow")
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def scroll_down(self, amount: int):
        action = ActionChains(self.driver)
        action.scroll_by_amount(0, amount).perform()
        time.sleep(3)

    def click(self, locator):
        time.sleep(1)
        self.highlight_element(self.driver, locator, "Yellow")
        self.driver.find_element(*locator).click()
        time.sleep(3)

    def click_by_offset(self, x_offset, y_offset):
        self.highlight_element(self.driver, ("xpath", "//body"), "Yellow")
        action = ActionChains(self.driver)
        action.move_by_offset(x_offset, y_offset).click().perform()
        time.sleep(3)

    def scroll_to_element(self, locator):
        self.highlight_element(self.driver, locator, "Yellow")
        element = self.driver.find_element(*locator)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    def scroll_to_element_iterate(self, items):
        """
        Scrolls to each element in a list, or finds elements by locator and scrolls to each.
        :param items: Either a locator tuple or a list of WebElements.
        """
        if isinstance(items, tuple):
            elements = self.driver.find_elements(*items)
        else:
            elements = items
        for el in elements:
            self.highlight_element(self.driver, el, "Yellow")
            action = ActionChains(self.driver)
            action.move_to_element(el).perform()
            time.sleep(1)

    def get_text(self, locator):
        self.highlight_element(self.driver, locator, "Orange")
        return self.driver.find_element(*locator).text

    def click_and_hold(self, locator):
        self.highlight_element(self.driver, locator, "Yellow")
        element = self.driver.find_element(*locator)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    def select(self, locator, value, by_visible_text=False):
        self.highlight_element(self.driver, locator, "Yellow")
        select_element = Select(self.driver.find_element(*locator))
        if by_visible_text:
            select_element.select_by_visible_text(value)
        else:
            select_element.select_by_value(value)

    def get_value(self, locator):
        """
        Get the value of an input field or similar element.
        """
        try:
            element = self.driver.find_element(*locator)
            value = element.get_attribute("value")
            print(f"Value of element {locator}: {value}")
            return value
        except Exception as e:
            print(f"Error getting value from {locator}: {e}")
            return None
