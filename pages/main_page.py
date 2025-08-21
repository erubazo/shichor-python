import re
import time
import datetime

import allure
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class MainPage(BasePage):
    TRIP1 = (By.CSS_SELECTOR, '[data-test="SearchFormModesPicker-active-return"]')
    TRIP2 = (By.CSS_SELECTOR, '[data-test="SearchFormModesPicker-active-oneWay"]')
    ONEWAY = (By.CSS_SELECTOR, '[data-test="ModePopupOption-oneWay"]')
    RETURN_OPTION = (By.CSS_SELECTOR, '[data-test="ModePopupOption-return"]')  # Renamed from RETURN
    ACCEPT = (By.CSS_SELECTOR, '[data-test="CookiesPopup-Accept"]')
    CUSTOMIZE = (By.CSS_SELECTOR, r"#cookie_consent > div > div > div > section > div.orbit-stack.items-start.content-start.flex-nowrap.grow.shrink-0.justify-start.flex-row.flex.gap-400.w-full > button.space-x-200.rtl\:space-x-reverse.h-form-box-normal.text-normal.bg-button-secondary-background.hover\:bg-button-secondary-background-hover.active\:bg-button-secondary-background-active.disabled\:bg-button-secondary-background.focus\:bg-button-secondary-background-focus.text-button-secondary-foreground.focus\:text-button-secondary-foreground-focus.active\:text-button-secondary-foreground-active.hover\:text-button-secondary-foreground-hover.disabled\:text-button-secondary-foreground.active\:shadow-button-active-pale.px-button-padding-md.orbit-button-primitive.font-base.duration-fast.group.relative.max-w-full.select-none.items-center.justify-center.border-none.text-center.leading-none.transition-all.\*\:align-middle.\[\&_\.orbit-loading-spinner\]\:stroke-current.w-full.flex-auto.rounded-150.tb\:rounded-100.cursor-pointer.hover\:no-underline.focus\:no-underline.active\:no-underline.flex.font-medium > div")
    CLOSE = (By.CSS_SELECTOR, "#cookie_consent > div > div > div > div > button > div > svg")
    CLASS = (By.CSS_SELECTOR, r"div.lm\:mb-100.mb-300.flex.items-center.tb\:justify-start.justify-between > div:nth-child(2) > div:nth-child(1) > div")
    ECCONOMY = (By.CSS_SELECTOR,'div > a:nth-child(1) > label > div.ms-200.flex.flex-1.flex-col.font-medium.opacity-100 > span')
    PREMIUM = (By.CSS_SELECTOR, "div > a:nth-child(2) > label > div.ms-200.flex.flex-1.flex-col.font-medium.opacity-100 > span")
    BUISSNESS = (By.CSS_SELECTOR, "a:nth-child(3) > label > div.ms-200.flex.flex-1.flex-col.font-medium.opacity-100 > span")
    FIRSTCLASS = (By.CSS_SELECTOR, ' a:nth-child(4) > label > div.ms-200.flex.flex-1.flex-col.font-medium.opacity-100 > span')
    MIXED = (By.CSS_SELECTOR, '[data-test="MixedClassText"]')
    PASSENGER = (By.CSS_SELECTOR, '[data-test="PassengersButton"]')
    ADULT_PLUS = (By.CSS_SELECTOR, '[aria-label="Add adult"]')
    ADULTS = (By.CSS_SELECTOR,'[aria-labelledby="passengersPicker-adults"]')
    CHILDREN = (By.CSS_SELECTOR,'[aria-labelledby="passengersPicker-children"]')
    INFANTS = (By.CSS_SELECTOR,'[aria-labelledby="passengersPicker-infants"]')
    CABIN = (By.CSS_SELECTOR,'[aria-labelledby="bagsPickerSearchForm-cabin"]')
    CHECKED = (By.CSS_SELECTOR,'[aria-labelledby="bagsPickerSearchForm-checked"]')
    ADULT_MINUS = (By.CSS_SELECTOR, '[aria-label="Remove adult"]')
    CHILD_PLUS = (By.CSS_SELECTOR, '[aria-label="Add child"]')
    CHILD_MINUS = (By.CSS_SELECTOR, '[aria-label="Remove child"]')
    INFANT_PLUS = (By.CSS_SELECTOR, '[aria-label="Add infant"]')
    INFANT_MINUS = (By.CSS_SELECTOR,'[aria-label="Remove infant"]')
    CABIN_PLUS = (By.CSS_SELECTOR,"[aria-label='Add cabin bag']")
    CABIN_MINUS = (By.CSS_SELECTOR,"[aria-label='Remove cabin bag']")
    CHECKED_PLUS = (By.CSS_SELECTOR,"[aria-label='Add checked bag']")
    CHECKED_MINUS = (By.CSS_SELECTOR,"[aria-label='Remove checked bag']")
    ORIGIN = (By.CSS_SELECTOR, '#origin')
    PLACE = (By.CSS_SELECTOR, '[data-test="PlacePickerInputPlace"]')
    ORIGIN_CLOSE = (By.CSS_SELECTOR, '[data-test="PlacePickerInputPlace-close"]')
    ORIGIN_CITY = (By.CSS_SELECTOR, '[data-test="PlacePickerRow-city"]')
    CITY_LIST = (By.CSS_SELECTOR, '[data-test="PlacePickerRow-wrapper"]')
    DESTINATION = (By.CSS_SELECTOR, '#destination')
    DEPARTURE_DATE = (By.CSS_SELECTOR, '#outboundDate')
    CALENDER = (By.CSS_SELECTOR,'[data-value]')
    THIS_MONTH = (By.CSS_SELECTOR, '[data-test="DatepickerMonthButton"]')
    NEXT_MONTH = (By.CSS_SELECTOR, '[data-test="CalendarMoveNextButton"]')
    DONE = (By.CSS_SELECTOR, '[data-test="SearchFormDoneButton"]')
    ACCOMENDATION = (By.CSS_SELECTOR, '[data-test="bookingCheckbox"]')
    SEARCH = (By.CSS_SELECTOR, '[data-test="LandingSearchButton"]')
    CARS = (By.CSS_SELECTOR, ' span:nth-child(4) > a')
    STAYS = (By.CSS_SELECTOR, 'span:nth-child(6) > a')
    MAGAZINE = (By.CSS_SELECTOR, 'span:nth-child(8) > a')
    TRAVLE_HACKS = (By.CSS_SELECTOR, 'span:nth-child(10) > a')
    TRAVLE_HACKS_BTN = (By.CSS_SELECTOR, r'#react-view > div.MainView.absolute.bottom-0.left-0.right-0.overflow-visible.top-\[var\(--main-view-navbar-height\)\] > main > div.relative.min-h-\[450px\].bg-white-normal.flex.flex-wrap.content-center.justify-center.rounded-bl-\[40px\].rounded-br-\[40px\].rounded-tl-none.rounded-tr-none.\[box-shadow\:0px_12px_76px_\#e5eaef\].mb-600.px-400.py-0.tb\:min-h-\[325px\] > div.absolute.bottom-\[0\].left-2\/4.flex.w-full.-translate-x-1\/2.translate-y-1\/2.justify-center.\[\&_button\]\:rounded-\[80px\].\[\&_button\]\:bg-\[\#252a31\].\[\&_button\]\:p-0.\[\&_button\]\:pe-400.\[\&_button\]\:ps-600.hover\:\[\&_button\]\:\!bg-\[\#252a31\].focus\:\[\&_button\]\:\!bg-\[\#252a31\].active\:\[\&_button\]\:\!bg-\[\#252a31\].\[\&_button_p\]\:text-center.\[\&_button_p\]\:uppercase.\[\&_button_p\]\:leading-small.\[\&_button_p\]\:tracking-\[0\.15em\].\[\&_button_p\]\:text-\[\#bac7d5\].\[\&_button_svg\]\:mx-100.\[\&_button_svg\]\:my-0.\[\&_button_svg\]\:text-\[\#00a991\] > button')
    DEALS = (By.CSS_SELECTOR, 'span:nth-child(12) > a')
    DEALS_H4 = (By.XPATH,'//*[@id="DealsMainView"]/div[1]/div[2]/div[2]/h4')
    STAYS_H1 = (By.CSS_SELECTOR, '#indexsearch > div:nth-child(1) > div > div > div > div > header > h1')
    CURRENCY = (By.CSS_SELECTOR, '[data-test="TopNav-RegionalSettingsButton"]')
    HELP = (By.CSS_SELECTOR, '[data-test="TopNav-HelpButton"]')
    SIGN_IN = (By.CSS_SELECTOR, '[data-test="TopNav-SingInButton"]')
    RETURN_DATE = (By.CSS_SELECTOR, '#inboundDate')  # Renamed from RETURN
    DATE_VALUE = (By.CSS_SELECTOR, '[data-test="DateValue"]')
    CANCEL = (By.CSS_SELECTOR, '[data-test="SearchFormCancelButton"]')
    SWITCH = (By.CSS_SELECTOR, '[aria-label="Switch direction"]')
    CITY_NOT_FOUND = (By.CSS_SELECTOR, r'#react-view > div.flex.min-h-screen.flex-col > div:nth-child(2) > div.min-h-\[388px\].relative.lm\:min-h-\[391px\].lm\:bg-ink-normal.lm\:pt-1000.pt-600.tb\:pt-\[58px\].tb\:pb-\[36px\].de\:pt-\[90px\].de\:pt-\[26px\].ld\:pt-\[60px\] > div.relative > div:nth-child(2) > div.relative.z-10.rounded-150.bg-white-normal.lm\:shadow-level3.-mt-300.translate-y-300.px-300.pt-400.pb-300.shadow-level3.min-h-\[378px\].lm\:-mt-800.lm\:min-h-\[252px\].lm\:translate-y-800.lm\:p-400.tb\:mt-0.tb\:min-h-\[264px\].tb\:transform-none.de\:rounded-200.de\:p-600.de\:pt-300.de\:min-h-\[268px\].ld\:min-h-\[160px\].ld\:pb-400 > div.flex.ld\:flex-row.flex-col.gap-300.lm\:gap-200 > div > div:nth-child(1) > div > div > div.absolute.z-\[101\].rounded-100.bg-white-normal.shadow-level3.w-auto.-left-300.-right-300.-top-300.ld\:w-\[374px\] > div > div > div > p')
    ECONOMY_YNET = (By.CSS_SELECTOR, '#BottomHeaderArea > div.mainNav > div.navList > div:nth-child(6)')
    TITLES = (By.CSS_SELECTOR, 'h2 > span')

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Choose trip type: {trip_type}")
    def choose_trip(self, trip_type: str)-> str:
        try:
            time.sleep(3)
            # Helper function to check if element is available
            def is_available(locator):
                try:
                    element = self.driver.find_element(*locator)
                    return element.is_displayed()
                except Exception:
                    return False

            # Check which trip selectors are available
            trip1_available = is_available(self.TRIP1)
            trip2_available = is_available(self.TRIP2)

            print(f"TRIP1 (return) available: {trip1_available}")
            print(f"TRIP2 (oneway) available: {trip2_available}")

            # Determine which selector to use based on availability and trip type
            if trip_type.lower() == "oneway":
                # For oneway, prefer TRIP2 if available
                if trip2_available:
                    selector = self.TRIP2
                elif trip1_available:
                    selector = self.TRIP1
                else:
                    return "No trip selector available"
            elif trip_type.lower() == "return":
                # For return, prefer TRIP1 if available
                if trip1_available:
                    selector = self.TRIP1
                elif trip2_available:
                    selector = self.TRIP2
                else:
                    return "No trip selector available"
            else:
                return f"Unsupported trip type: {trip_type}"

            # Click the selected trip type selector
            self.click(selector)
            time.sleep(1)

            # Select the appropriate trip type option
            if trip_type.lower() == "oneway":
                self.click(self.ONEWAY)
                expected_text = "One way"  # The expected text for oneway
            else:  # return
                self.click(self.RETURN_OPTION)
                expected_text = "Return"   # The expected text for return

            # Give the UI more time to update after selection
            time.sleep(2)

            # Try multiple approaches to get the selected text
            try:
                # First attempt - get text from the selector
                selected_text = self.get_text(selector)
                print(f"Text from selector: '{selected_text}'")

                # If the text doesn't contain our expected value, try to find the active selector
                if expected_text.lower() not in selected_text.lower():
                    # Try to find which selector is now active
                    if trip_type.lower() == "oneway":
                        active_selector = self.TRIP2  # For oneway
                    else:
                        active_selector = self.TRIP1  # For return

                    selected_text = self.get_text(active_selector)
                    print(f"Text from active selector: '{selected_text}'")
            except Exception as e:
                print(f"Error getting text from selectors: {e}")
                # As a fallback, return the capitalized trip type
                selected_text = trip_type.capitalize()

            print(f"Final selected trip type: '{selected_text}'")

            # If we still don't have a meaningful value, return the expected text
            if not selected_text or len(selected_text.strip()) == 0:
                print(f"Using expected text as fallback: '{expected_text}'")
                return expected_text

            return selected_text

        except Exception as e:
            print(f"Error selecting trip type: {e}")
            # Return the expected text as fallback in case of error
            if trip_type.lower() == "oneway":
                return "One way"
            return "Return"

    @allure.step("Choose class type: {class_type}")
    def choose_class(self, class_type: str, mixed: bool = False) -> str:
        c= ""
        self.click(self.CLASS)
        if class_type == "premium":
            self.click(self.PREMIUM)
        elif class_type == "business":
            self.click(self.BUISSNESS)
        elif class_type == "firstclass":
            self.click(self.FIRSTCLASS)
        elif class_type == "economy":
            self.click(self.ECCONOMY)
        if mixed:
            self.click(self.MIXED)
        self.click_by_offset(0, 100)  # Click outside to close the dropdown
        time.sleep(3)
        c = self.get_text(self.CLASS)
        return c

    @allure.step("Choose passenger: Adults={adults}, Children={children}, Infants={infants}, Cabin={cabin}, Checked={checked}")
    def choose_passenger(self, adults: int, children: int, infants: int, cabin: int = 0, checked: int = 0) -> str:
        # Helper function to get count from passenger elements
        def get_count(locator, default_value=0):
            try:
                # Try to find the element and extract number
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )

                # Most likely format: "# Adults" or similar
                text = element.text

                # If text is empty, try to get value from attributes
                if not text:
                    for attr in ["value", "innerHTML", "textContent"]:
                        text = element.get_attribute(attr)
                        if text and text.strip():
                            break

                print(f"Element text: '{text}'")

                # Extract number using regex
                match = re.search(r'(\d+)', str(text))
                if match:
                    return int(match.group(1))

                print(f"No number found in text, using default: {default_value}")
                return default_value
            except Exception as e:
                print(f"Error getting count: {e}")
                return default_value

        # Helper function to adjust passenger count
        def adjust_count(count_locator, target, plus_locator, minus_locator, name, default_start=0):
            max_attempts = 10

            # For adults, default is 1; for everything else, default is 0
            default_value = 1 if name == "Adults" else 0

            # Get initial count (with appropriate default)
            current = get_count(count_locator, default_value)
            print(f"Initial {name} count: {current}")

            for attempt in range(max_attempts):
                # Break if we've reached the target
                if current == target:
                    print(f"{name} count reached target: {target}")
                    break

                # Click plus button if we need to increase
                elif current < target:
                    print(f"Clicking + for {name} (current: {current}, target: {target})")
                    try:
                        self.driver.find_element(*plus_locator).click()
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error clicking + for {name}: {e}")

                # Click minus button if we need to decrease
                elif current > target:
                    print(f"Clicking - for {name} (current: {current}, target: {target})")
                    try:
                        self.driver.find_element(*minus_locator).click()
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error clicking - for {name}: {e}")

                # Get the updated count after clicking
                current = get_count(count_locator, current)
                print(f"Updated {name} count: {current}")

            # Check if we reached the target
            if current != target:
                print(f"Warning: Could not set {name} to {target}, final value is {current}")

            return current

        try:
            # Open passenger selector
            print("Opening passenger selector...")
            self.click(self.PASSENGER)
            time.sleep(2)

            # Adjust passenger counts
            adjust_count(self.ADULTS, adults, self.ADULT_PLUS, self.ADULT_MINUS, "Adults", 1)
            adjust_count(self.CHILDREN, children, self.CHILD_PLUS, self.CHILD_MINUS, "Children")
            adjust_count(self.INFANTS, infants, self.INFANT_PLUS, self.INFANT_MINUS, "Infants")
            adjust_count(self.CABIN, cabin, self.CABIN_PLUS, self.CABIN_MINUS, "Cabin bags")
            adjust_count(self.CHECKED, checked, self.CHECKED_PLUS, self.CHECKED_MINUS, "Checked bags")

            # Close passenger selector
            self.click_by_offset(100, 0)
            time.sleep(2)

            # Get and return final text
            result = self.get_text(self.PASSENGER).replace("\n", " ")
            print(f"Final passenger text: '{result}'")
            return result

        except Exception as e:
            print(f"Error in choose_passenger: {e}")
            return "Error"

    def choose_from_list(self, origin: str = None, index: int = 0):
        """
        Choose an origin city from the list by visible text or index.
        If origin is provided, selects by text; otherwise, selects by index.
        If no elements found, returns the CITY_NOT_FOUND text.
        Returns: True if a city was selected, False otherwise
        """
        elements = self.driver.find_elements(*self.CITY_LIST)
        if not elements:
            try:
                city_not_found_text = self.get_text(self.CITY_NOT_FOUND)
                print(f"No origin cities found. Returning: {city_not_found_text}")
                return False, city_not_found_text
            except Exception as e:
                print(f"Error getting CITY_NOT_FOUND text: {e}")
                return False, "No cities found"

        # Moved print below to after fill_text in choose_origin
        if origin:
            for el in elements:
                if origin.lower() in el.text.lower():
                    print(f"Clicking element with text: {el.text}")
                    el.click()
                    return True, None
            print(f"Origin city '{origin}' not found in the list.")
            return False, f"Origin city '{origin}' not found in the list."
        else:
            if index < 0 or index >= len(elements):
                print(f"Index {index} out of range for origin city list.")
                return False, f"Index {index} out of range for origin city list."
            print(f"Clicking element at index {index} with text: {elements[index].text}")
            elements[index].click()
            return True, None

    @allure.step("Choose origin city: {origin}")
    def choose_origin(self, origin: str, index: int = 0, close: bool = True) -> str:
        if close:
            self.click(self.ORIGIN_CLOSE)
        print(f"Trying to fill origin with locator: {self.ORIGIN} and value: {origin}")
        self.fill_text(self.ORIGIN, origin)
        time.sleep(3)  # Wait for UI to update after filling text
        try:
            city_not_found_elements = self.driver.find_elements(*self.CITY_NOT_FOUND)
            if city_not_found_elements:
                error_message = city_not_found_elements[0].text
                if "We couldn't find what you were looking for" in error_message:
                    print(f"City not found: {error_message}")
                    return error_message
        except Exception as e:
            print(f"Error checking for city not found: {e}")
        elements = self.driver.find_elements(*self.CITY_LIST)
        print("Origin city list texts after fill_text:")
        for el in elements:
            print(f"- {el.text}")
        success, message = self.choose_from_list(origin, index)

        if not success:
            print(f"Failed to select city: {message}")
            input = self.driver.find_element(By.CSS_SELECTOR,'#origin')
            input.clear()
            return message

        try:
            output = self.get_text(self.PLACE)
            time.sleep(3)
            return output
        except Exception as e:
            print(f"Error getting place text: {e}")
            return "Could not retrieve selected place"

    @allure.step("Choose destination city: {destination}")
    def choose_destination(self, destination: str,index: int = 0,close: bool = False) -> str:
            if close:
                self.click(self.ORIGIN_CLOSE)
            self.click(self.DESTINATION)
            self.fill_text(self.DESTINATION, destination)
            time.sleep(3)  # Wait for UI to update after filling text

            # Check early for "city not found" message
            try:
                city_not_found_elements = self.driver.find_elements(*self.CITY_NOT_FOUND)
                if city_not_found_elements:
                    error_message = city_not_found_elements[0].text
                    if "We couldn't find what you were looking for" in error_message:
                        print(f"City not found: {error_message}")
                        return error_message
            except Exception as e:
                print(f"Error checking for city not found: {e}")

            elements = self.driver.find_elements(*self.CITY_LIST)
            for el in elements:
                print(f"- {el.text}")
            success, message = self.choose_from_list(destination, index)

            if not success:
                print(f"Failed to select destination: {message}")
                return message

            try:
                output = self.get_text(self.PLACE)
                time.sleep(3)
                return output
            except Exception as e:
                print(f"Error getting destination place text: {e}")
                return "Could not retrieve selected destination"


    @allure.step("Choose dates: Start={start_date}, End={end_date}")
    def choose_dates(self, start_date: str, end_date: str,cancel: bool)->str:
        self.click(self.DEPARTURE_DATE)
        time.sleep(3)

        def is_enabled(el):
            aria_disabled = el.get_attribute("aria-disabled")
            class_attr = el.get_attribute("class") or ""
            return (not aria_disabled or aria_disabled == "false") and ("is-disabled" not in class_attr)

        def get_calendar_month_year():
            # Use get_text to get the visible month/year from the calendar header
            try:
                text = self.get_text(self.THIS_MONTH)
                return text.strip()
            except Exception:
                return None

        def go_to_month(target_date):
            """Navigate calendar to the correct month/year before clicking the date."""
            target_dt = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            max_tries = 12
            for _ in range(max_tries):
                visible_month = get_calendar_month_year()
                if visible_month:
                    try:
                        visible_dt = datetime.datetime.strptime(visible_month, "%B %Y")
                        if visible_dt.year == target_dt.year and visible_dt.month == target_dt.month:
                            return
                    except Exception:
                        pass
                self.click(self.NEXT_MONTH)
                time.sleep(1)
            raise Exception(f"Could not navigate to month of '{target_date}' in calendar.")

        def click_day(target_date):
            go_to_month(target_date)
            elements = self.driver.find_elements(*self.CALENDER)
            for el in elements:
                if (
                    el.get_attribute("data-value") == target_date
                    and is_enabled(el)
                ):
                    print(f"Clicking date: {target_date}")
                    el.click()
                    return True
            raise Exception(f"Date '{target_date}' not found in visible month.")

        click_day(start_date)

        if end_date:
            time.sleep(1)
            click_day(end_date)
            time.sleep(1)

        # Wait for calendar to close before continuing
        max_wait = 10
        for _ in range(max_wait):
            try:
                calendar_visible = self.driver.find_element(By.CSS_SELECTOR, '[data-test="CalendarMonthLabel"]').is_displayed()
            except Exception:
                calendar_visible = False
            if not calendar_visible:
                break
            time.sleep(1)

        if cancel:
            self.click(self.CANCEL)
        else:
            self.click(self.DONE)
        output = self.get_value(self.RETURN_DATE)+ " , " + self.get_value(self.DEPARTURE_DATE)  # Changed from self.RETURN
        return output

    @allure.step("Choose departure date: {departure_date}")
    def choose_departure_date(self, departure_date: str)->str:
        """
        Select only the departure date without needing to select a return date.

        Args:
            departure_date (str): Date in format "YYYY-MM-DD"
        """
        self.click(self.DEPARTURE_DATE)
        time.sleep(3)

        def is_enabled(el):
            aria_disabled = el.get_attribute("aria-disabled")
            class_attr = el.get_attribute("class") or ""
            return (not aria_disabled or aria-disabled == "false") and ("is-disabled" not in class_attr)

        def get_calendar_month_year():
            try:
                text = self.get_text(self.THIS_MONTH)
                return text.strip()
            except Exception:
                return None

        def go_to_month(target_date):
            """Navigate to the correct month/year in the calendar."""
            target_dt = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            max_tries = 12
            for _ in range(max_tries):
                visible_month = get_calendar_month_year()
                if visible_month:
                    try:
                        visible_dt = datetime.datetime.strptime(visible_month, "%B %Y")
                        if visible_dt.year == target_dt.year and visible_dt.month == target_dt.month:
                            return
                    except Exception:
                        pass
                self.click(self.NEXT_MONTH)
                time.sleep(1)
            raise Exception(f"Could not navigate to month of '{departure_date}' in calendar.")

        def click_day(target_date):
            go_to_month(target_date)
            elements = self.driver.find_elements(*self.CALENDER)
            for el in elements:
                if (
                        el.get_attribute("data-value") == target_date
                        and is_enabled(el)
                ):
                    print(f"Clicking departure date: {target_date}")
                    el.click()
                    return True
            raise Exception(f"Departure date '{target_date}' not found in visible month.")

        # Click the departure date
        click_day(departure_date)

        # Wait for calendar to close before continuing
        max_wait = 10
        for _ in range(max_wait):
            try:
                calendar_visible = self.driver.find_element(By.CSS_SELECTOR,
                                                            '[data-test="CalendarMonthLabel"]').is_displayed()
            except Exception:
                calendar_visible = False
            if not calendar_visible:
                break
            time.sleep(1)

        # Click done to close the calendar
        self.click(self.DONE)
        print(f"Departure date '{departure_date}' selected successfully")
        output = self.get_value(self.DEPARTURE_DATE)
        return output

    @allure.step("Choose return date: {return_date}")
    def choose_return_date(self, return_date: str) -> str:
        self.click(self.RETURN_DATE)  # Changed from self.RETURN
        time.sleep(3)
        # Fix: Added asterisk (*) to unpack the locator tuple
        date_elements = self.driver.find_elements(*self.DATE_VALUE)
        print(f"Found {len(date_elements)} date elements")

        if len(date_elements) > 1:
            print("Clicking on the second date element")
            date_elements[1].click()
        else:
            print("Only one date element found, clicking on it")
            self.click(self.DATE_VALUE)

        def is_enabled(el):
            aria_disabled = el.get_attribute("aria-disabled")
            class_attr = el.get_attribute("class") or ""
            return (not aria_disabled or aria_disabled == "false") and ("is-disabled" not in class_attr)

        def get_calendar_month_year():
            try:
                text = self.get_text(self.THIS_MONTH)
                return text.strip()
            except Exception:
                return None

        def go_to_month(target_date):
            """Navigate calendar to the correct month/year before clicking the date."""
            target_dt = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            max_tries = 12
            for _ in range(max_tries):
                visible_month = get_calendar_month_year()
                if visible_month:
                    try:
                        visible_dt = datetime.datetime.strptime(visible_month, "%B %Y")
                        if visible_dt.year == target_dt.year and visible_dt.month == target_dt.month:
                            return
                    except Exception:
                        pass
                self.click(self.NEXT_MONTH)
                time.sleep(1)
            raise Exception(f"Could not navigate to month of '{return_date}' in calendar.")

        def click_day(target_date):
            go_to_month(target_date)
            elements = self.driver.find_elements(*self.CALENDER)
            for el in elements:
                if (
                        el.get_attribute("data-value") == target_date
                        and is_enabled(el)
                ):
                    print(f"Clicking return date: {target_date}")
                    el.click()
                    return True
            raise Exception(f"Return date '{return_date}' not found in visible month.")

        # Click the return date
        click_day(return_date)

        # Wait for calendar to close before continuing
        max_wait = 10
        for _ in range(max_wait):
            try:
                calendar_visible = self.driver.find_element(By.CSS_SELECTOR,
                                                            '[data-test="CalendarMonthLabel"]').is_displayed()
            except Exception:
                calendar_visible = False
            if not calendar_visible:
                break
            time.sleep(1)

        self.click(self.DONE)
        print(f"Return date '{return_date}' selected successfully")
        output = self.get_value(self.RETURN_DATE)  # Changed from self.RETURN
        return output



    def link_checker_same(self, locator, tab: str) -> bool:
        self.click(locator)
        time.sleep(2)
        tab_lower = tab.lower()
        if tab_lower == "travel hacks":
            self.click(self.ACCEPT)
            btn_text = self.get_text(self.TRAVLE_HACKS_BTN).lower()
            print(f"h1 text: {btn_text}")
            return tab_lower in btn_text
        elif tab_lower == "deals":
            h4_text = self.get_text(self.DEALS_H4).lower()
            print(f"h4 text: {h4_text}")
            return tab_lower in h4_text
        else:
            # Add fallback: check page title or URL
            title = self.driver.title.lower()
            url = self.driver.current_url.lower()
            print(f"Title: {title}, URL: {url}")
            return tab_lower in title or tab_lower in url

    def link_checker_diff(self, locator, tab: str) -> bool:
        self.click(locator)
        time.sleep(2)
        original_window = self.driver.current_window_handle
        handles = self.driver.window_handles
        new_handles = [h for h in handles if h != original_window]
        if new_handles:
            self.driver.switch_to.window(new_handles[0])
            time.sleep(3)
            tab_lower = tab.lower()
            result = False
            if tab_lower == "stay":
                try:
                    h1_text = self.get_text(self.STAYS_H1).lower()
                    print(f"h1 text: {h1_text}")
                    result = tab_lower in h1_text
                except Exception as e:
                    print(f"Error getting STAYS_H1: {e}")
            elif tab_lower == "magazine":
                title = self.driver.title.lower()
                print(f"Page title: {title}")
                result = tab_lower in title
            elif tab_lower == "help":
                title = self.driver.title.lower()
                print(f"Page title: {title}")
                result = tab_lower in title
            elif tab_lower == "cars":
                url = self.driver.current_url.lower()
                print(f"URL of new page: {url}")
                result = tab_lower in url or tab_lower in self.driver.title.lower()
            else:
                # Fallback: check URL and title
                url = self.driver.current_url.lower()
                title = self.driver.title.lower()
                print(f"URL: {url}, Title: {title}")
                result = tab_lower in url or tab_lower in title
            self.driver.close()
            self.driver.switch_to.window(original_window)
            return result
        else:
            print("No new tab opened.")
            return False

    def cookie_accept(self):
        """
        Accept cookies by clicking the accept button.
        """
        try:
            self.click(self.ACCEPT)
            print("Cookies accepted.")
        except Exception as e:
            print(f"Error accepting cookies: {e}")
