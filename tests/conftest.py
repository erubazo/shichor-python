# conftest.py
import os
import pytest
import allure
from allure_commons.types import AttachmentType

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _running_in_ci() -> bool:
    # Works for GitHub Actions and most other CIs
    return bool(os.getenv("GITHUB_ACTIONS") or os.getenv("CI"))


@pytest.fixture(scope="session")
def chrome_options() -> Options:
    opts = Options()

    # CI-safe & deterministic
    if _running_in_ci():
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    else:
        # Headed locally; keep a fixed size if you want identical layout:
        # opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--start-maximized")

    # Stability flags
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-features=Translate,NetworkService,InterestCohort")
    opts.add_argument("--lang=en-US")

    # Useful defaults
    opts.add_experimental_option("prefs", {
        "intl.accept_languages": "en-US,en",
        "profile.default_content_setting_values.images": 1,
        "profile.default_content_setting_values.cookies": 1,
    })

    # Browser console logs
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # Page load behavior
    opts.page_load_strategy = "normal"

    return opts


def _wait_page_ready(driver, timeout=60):
    WebDriverWait(driver, timeout, poll_frequency=0.2).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def _dismiss_cookie_banner_if_present(driver, timeout=4):
    """
    Dismiss common consent/cookie banners that block clicks in headless CI.
    Adjust locator to your site if needed.
    """
    accept_locators = [
        (By.CSS_SELECTOR, '[data-test="CookiesPopup-Accept"]'),
        (By.CSS_SELECTOR, 'button#cookie-accept'),
        (By.XPATH, "//button[contains(., 'Accept') or contains(., 'I Agree')]"),
    ]
    for loc in accept_locators:
        try:
            btn = WebDriverWait(driver, timeout, 0.2).until(EC.element_to_be_clickable(loc))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            try:
                btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(driver, 5, 0.2).until(EC.invisibility_of_element_located(loc))
            return
        except Exception:
            continue  # try next locator; silently skip if none exist


@pytest.fixture(scope="class")
def setup_driver_class(request, chrome_options):
    """
    Create one driver per test class, init page objects, navigate to base URL.
    Uses Selenium Manager (no webdriver_manager needed).
    """
    driver = webdriver.Chrome(options=chrome_options)

    # Timeouts: keep implicit at 0 and rely on explicit waits
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    driver.implicitly_wait(0)

    # Make available to tests and hooks (even on setup errors)
    request.cls.driver = driver
    request.node.driver = driver

    # Navigate to base URL from your ConfigReader
    from utils.config import ConfigReader
    base_url = ConfigReader.read_config("general", "base_url")
    driver.get(base_url)

    # Wait for full readiness (helps CI)
    _wait_page_ready(driver)

    # Optional: dismiss cookie banner that appears in clean CI profiles
    _dismiss_cookie_banner_if_present(driver)

    # Init your page objects
    from pages.cookie_page import CookiePage
    from pages.currency_page import CurrencyPage
    from pages.main_page import MainPage
    from pages.signin_page import SignInPage

    request.cls.main_page = MainPage(driver)
    request.cls.cookie_page = CookiePage(driver)
    request.cls.currency_page = CurrencyPage(driver)
    request.cls.signin_page = SignInPage(driver)

    yield

    try:
        driver.quit()
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On failure in setup/call/teardown, attach screenshot, HTML and console logs to Allure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.failed:
        driver = getattr(item, "driver", None)
        if driver is None and hasattr(item, "cls") and hasattr(item.cls, "driver"):
            driver = getattr(item.cls, "driver", None)

        if driver:
            # Screenshot
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot-{rep.when}",
                    attachment_type=AttachmentType.PNG,
                )
            except Exception:
                pass

            # Page source
            try:
                allure.attach(
                    driver.page_source,
                    name=f"page_source-{rep.when}",
                    attachment_type=AttachmentType.HTML,
                )
            except Exception:
                pass

            # Browser console logs
            try:
                logs = driver.get_log("browser")
                if logs:
                    text = "\n".join(f"[{l.get('level')}] {l.get('message')}" for l in logs)
                    allure.attach(text, name=f"console-{rep.when}", attachment_type=AttachmentType.TEXT)
            except Exception:
                pass
