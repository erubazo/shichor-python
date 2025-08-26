# conftest.py
import os
import pytest
import allure
from allure_commons.types import AttachmentType

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

from pages.cookie_page import CookiePage
from pages.currency_page import CurrencyPage
from pages.main_page import MainPage
from pages.signin_page import SignInPage
from utils.config import ConfigReader


def _running_in_ci() -> bool:
    # Works for GitHub Actions and most CIs
    return bool(os.getenv("GITHUB_ACTIONS") or os.getenv("CI"))


@pytest.fixture(scope="session")
def chrome_options() -> Options:
    opts = Options()

    # Make headless behave predictably in CI
    if _running_in_ci():
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    else:
        opts.add_argument("--start-maximized")
        # Keep a fixed size to reduce layout flakiness locally too (optional)
        # opts.add_argument("--window-size=1920,1080")

    # Stable, CI-friendly flags
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-features=Translate,NetworkService,InterestCohort")
    opts.add_argument("--lang=en-US")
    opts.add_experimental_option("prefs", {
        "intl.accept_languages": "en-US,en",
        "profile.default_content_setting_values.images": 1,
        "profile.default_content_setting_values.cookies": 1,
    })

    # Enable browser console logs (attach to Allure on failure)
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # More deterministic load behavior
    opts.page_load_strategy = "normal"  # "eager" if you purposely need faster navigations

    return opts


@pytest.fixture(scope="class")
def setup_driver_class(request, chrome_options):
    """Create one driver per test class, init page objects, navigate to base URL."""
    # Make sure ChromeDriver matches Chrome (works well in runners)
    driver_path = ChromeDriverManager().install()
    service = ChromeService(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Timeouts: prefer explicit waits in tests; keep implicit at 0 for determinism
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    driver.implicitly_wait(0)

    # Attach to class for tests
    request.cls.driver = driver
    request.node.driver = driver  # allow hooks to find it even during setup failures

    # Navigate to base URL from config
    base_url = ConfigReader.read_config("general", "base_url")
    driver.get(base_url)

    # Init page objects
    request.cls.main_page = MainPage(driver)
    request.cls.cookie_page = CookiePage(driver)
    request.cls.currency_page = CurrencyPage(driver)
    request.cls.signin_page = SignInPage(driver)

    yield

    # Teardown
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
        # If we stored it on class (setup_driver_class), fetch from there too
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

            # Browser console logs (if supported)
            try:
                logs = driver.get_log("browser")
                if logs:
                    text = "\n".join(f"[{l.get('level')}] {l.get('message')}" for l in logs)
                    allure.attach(text, name=f"console-{rep.when}", attachment_type=AttachmentType.TEXT)
            except Exception:
                pass
